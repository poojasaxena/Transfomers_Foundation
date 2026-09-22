### rag_utils.py
from __future__ import annotations

import json
import hashlib
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from llmlib.data.rag.kb_bm25_retriever import bm25_score_query, diversify_by_source

HUMOR_CUES = [
    "that’s right",
    "that's right",
    "if an elephant could talk",
    "it would probably say",
    "fear me",
    "zookeepers like to joke",
    "it’s a joke",
    "cinder-elephant",
    "ear-mail",
    "mouse",
    "glass slippers",
]


SYSTEM_PROMPT = (
    "You are ElephantChat, a helpful assistant.\n"
    "Answer using only the information in CONTEXT.\n"
    "Be concise and factual (3–6 sentences or up to 5 bullets).\n"
    "If the answer is not contained in the context, say:\n"
    '"I don\'t know based on the provided information."\n'
)

BAD_OUTPUT_PATTERNS = [
    r"\bi should\b",
    r"\bas an ai\b",
    r"\btask\b",
    r"\bavoid\b.*\bquestion\b",
]

BAD_DESC_TERMS = ["infanticide", "aggressive", "musth", "agonistic", "bones", "death", "fight", "sparring"]

FUN_FACT_STYLE_PENALTY_CUES = [
    "from an elephant’s point of view",
    "from an elephant's point of view",
    "it’s basically",
    "it's basically",
    "it’s like",
    "it's like",
    "would probably",
    "if an elephant could",
    "less “",  # your “less attack” style
    'less "',
]


def history_path_from(script_path: Path) -> Path:
    return script_path.with_name(".elephantchat_history.json")


def _fingerprint(text: str) -> str:
    # deterministic hash of normalized first 240 chars
    s = " ".join(text.lower().split())
    return hashlib.sha1(s[:240].encode("utf-8")).hexdigest()


def _clean_text(t: str) -> str:
    # Remove your corpus markers (optional but helps)
    t = t.replace("<doc>", "").replace("</doc>", "")
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _sentence_fingerprints(text: str) -> List[str]:
    sents = re.split(r"(?<=[.!?])\s+", _clean_text(text))
    sents = [s.strip() for s in sents if s.strip()]
    return [_fingerprint(s) for s in sents]


def extract_joke_units(text: str) -> List[str]:
    """
    Pull simple Q→A joke units from a chunk, e.g.
    'Why ...? They ... .'  or  'What ...? ... .'
    Deterministic regex, no ML.
    """
    t = _clean_text(text)

    # Match: question ending with ? followed by 1–2 short answer sentences.
    # Keep it conservative so we don't grab random prose.
    pat = re.compile(
        r"((?:Why|What|How|Have you ever|Did you ever|Did you know)\b[^?]{10,200}\?"
        r"(?:\s+[^.?!]{3,200}[.!]){1,2})",
        re.IGNORECASE,
    )
    return [m.group(1).strip() for m in pat.finditer(t)]


def trunk_chunk_score(c: Dict[str, Any]) -> int:
    t = _clean_text(c["text"]).lower()
    # score chunks that actually explain trunk function/anatomy
    keys = [
        "trunk",
        "proboscis",
        "nose",
        "upper lip",
        "muscle",
        "fascicle",
        "smell",
        "breath",
        "breathing",
        "grasp",
        "manipulat",
        "water",
        "drink",
        "touch",
        "tactile",
        "sensory",
        "sound",
        "vocal",
    ]
    score = 0
    for k in keys:
        if k in t:
            score += 1

    # deterministic de-prioritization for trunk query
    if "pleural" in t or "lungs" in t:
        score -= 2
    if "tusk" in t and "trunk" in t:
        score -= 1  # tusk+trunk is relevant but not central

    return score


def compare_chunk_score(c: Dict[str, Any]) -> int:
    t = _clean_text(c["text"]).lower()
    score = 0
    if "african" in t and "asian" in t:
        score += 3
    for k in ["difference", "differ", "whereas", "while", "versus", "vs", "contrast", "compared"]:
        if k in t:
            score += 2
    # de-prioritize tangential cultural content
    if "cultural" in t or "religious" in t:
        score -= 2
    return score


def load_history(hist_path: Path) -> Dict[str, Any]:
    if not hist_path.exists():
        return {"fun_facts": [], "humor": []}
    try:
        return json.loads(hist_path.read_text(encoding="utf-8"))
    except Exception:
        return {"fun_facts": [], "humor": []}


def save_history(hist_path: Path, hist: Dict[str, Any]) -> None:
    hist_path.write_text(json.dumps(hist, ensure_ascii=False, indent=2), encoding="utf-8")


def strip_catchphrases(s: str) -> str:
    return re.sub(r"^\s*(that['’]s right[:\-]?\s*)", "", s, flags=re.I).strip()


def is_short_description_query(q: str) -> bool:
    ql = q.lower()
    return "short" in ql and ("description" in ql or "describe" in ql)


def wants_another(q: str) -> bool:
    ql = q.lower()
    return any(p in ql for p in ["another", "one more", "a different", "different one"])


def is_topic_query(q: str) -> bool:
    ql = q.lower().strip()
    # short noun-phrase style prompts (no wh-words)
    return len(ql.split()) <= 5 and not any(
        w in ql for w in ["what", "why", "how", "when", "where", "difference", "compare"]
    )


def is_definition_query(q: str) -> bool:
    ql = q.lower().strip()
    return ("what is" in ql or "what are" in ql or "define" in ql or "explain" in ql) and "elephant" in ql


def topic_words(q: str) -> List[str]:
    ql = q.lower()
    toks = re.findall(r"[a-z]+", ql)
    stop = {"tell", "me", "about", "some", "something", "facts", "fact", "joke", "fun", "on", "of", "the", "a", "an", "elephant", "elephants"}
    toks = [t for t in toks if t not in stop and len(t) > 2]
    # keep up to 2 key words to avoid being too strict
    return toks[:2]


def coverage_ok(question: str, ctx: List[Dict[str, Any]]) -> bool:
    keys = topic_words(question)
    if not keys:
        return True
    text = " ".join(_clean_text(c["text"]).lower() for c in ctx[:5])
    return any(k in text for k in keys)


def detect_intent(q: str) -> str:
    ql = q.lower()

    # joke intent
    if any(p in ql for p in ["joke", "make me laugh", "tell me a joke", "pun", "one-liner"]):
        return "humor"

    # fun fact intent
    if any(p in ql for p in ["fun fact", "funny fact", "tell me a fun fact", "did you know"]):
        return "fun_facts"

    # neutral facts intent (not necessarily "fun")
    if any(p in ql for p in ["facts about", "tell me facts", "tell me a fact", "some facts", "give me facts"]):
        return "facts"

    return "default"

def wants_multiple_facts(q: str) -> bool:
    ql = q.lower()
    return ("fun facts" in ql) or ("facts" in ql and "fun" in ql) or ("some fun facts" in ql)


def allowed_categories_for_intent(intent: str):
    if intent == "humor":
        return {"humor"}
    if intent == "fun_facts":
        return {"fun_facts"}
    if intent == "facts":
        return {"basic_overview", "anatomy", "diet", "ecology", "social_life", "communication", "evolution", "mixed"}
    return None  # allow all


def _category_from_source(source: str) -> str:
    parts = Path(source).parts
    if "documents" in parts:
        i = parts.index("documents")
        if i + 1 < len(parts):
            return parts[i + 1]
    return "unknown"


def should_exclude_category(intent: str, category: str) -> bool:
    # In default mode, humor is usually noise.
    if intent == "default" and category == "humor":
        return True
    return False

def is_trunk_query(q: str) -> bool:
    ql = q.lower()
    return any(w in ql for w in ["trunk", "proboscis"])


def is_tail_query(q: str) -> bool:
    return "tail" in q.lower()


def is_size_query(q: str) -> bool:
    ql = q.lower()
    return any(w in ql for w in ["size", "big", "bigger", "how large", "weight", "height", "tall"])


def is_reproduction_query(q: str) -> bool:
    ql = q.lower()
    return any(w in ql for w in [
        "reproduce",
        "reproduction",
        "mate",
        "mating",
        "breed",
        "breeding",
        "pregnant",
        "pregnancy",
        "gestation",
        "birth",
        "give birth",
        "calf",
        "calves",
        "musth",
    ])


def is_communication_query(q: str) -> bool:
    ql = q.lower()
    return any(w in ql for w in [
        "communicate",
        "communication",
        "talk",
        "signal",
        "signals",
        "rumble",
        "vocal",
        "vocalization",
        "infrasound",
        "sound",
        "seismic",
        "vibration",
        "chemical",
        "scent",
    ])


def is_comparison_query(q: str) -> bool:
    ql = q.lower()
    return any(w in ql for w in ["difference", "different", "compare", "comparison", "versus", "vs"])


def is_calf_query(q: str) -> bool:
    ql = q.lower()
    return any(w in ql for w in ["baby elephant", "baby elephants", "calf", "calves", "newborn", "juvenile"])


def category_boost_order(chunks: List[Dict[str, Any]], question: str, topk: int) -> List[Dict[str, Any]]:
    def cat(c):
        return _category_from_source(c["source"])

    intent = detect_intent(question)

    if intent == "humor":
        preferred = {"humor"}
    elif intent == "fun_facts":
        preferred = {"fun_facts"}
    elif intent == "facts":
        preferred = {"basic_overview", "anatomy", "diet", "ecology", "social_life", "communication", "evolution", "mixed"}
    elif intent == "default" and is_comparison_query(question):
        preferred = {"basic_overview", "anatomy", "mixed"}
        pref = [c for c in chunks if cat(c) in preferred]
        rest = [c for c in chunks if cat(c) not in preferred]
        rest_non_social = [c for c in rest if cat(c) != "social_life"]
        rest_social = [c for c in rest if cat(c) == "social_life"]
        return (pref + rest_non_social + rest_social)[:topk]
    elif intent == "default" and is_trunk_query(question):
        preferred = {"anatomy", "communication", "basic_overview", "evolution", "mixed"}
    elif intent == "default" and is_tail_query(question):
        preferred = {"anatomy", "basic_overview", "communication", "ecology", "mixed"}
    elif intent == "default" and is_size_query(question):
        preferred = {"basic_overview", "anatomy", "research", "mixed"}
    elif intent == "default" and is_definition_query(question):
        preferred = {"basic_overview", "anatomy", "social_life", "ecology", "mixed"}
    elif intent == "default" and is_reproduction_query(question):
        preferred = {"research", "social_life", "communication", "basic_overview", "ecology", "mixed"}
    elif intent == "default" and is_communication_query(question):
        preferred = {"communication", "social_life", "research", "mixed"}
    elif intent == "default" and is_calf_query(question):
        preferred = {"research", "instruction_style", "social_life", "basic_overview", "anatomy", "communication", "ecology", "mixed"}
    elif is_single_species_traits_query(question):
        preferred = {
            "basic_overview",
            "anatomy",
            "diet",
            "ecology",
            "social_life",
            "communication",
            "evolution",
            "living_condition",
            "mixed",
        }
    else:
        # default: prefer factual categories; keep humor at the end (or removed already)
        preferred = {
            "anatomy",
            "communication",
            "diet",
            "ecology",
            "social_life",
            "evolution",
            "basic_overview",
            "mixed",
        }
        pref = [c for c in chunks if cat(c) in preferred]
        rest = [c for c in chunks if cat(c) not in preferred]
        return (pref + rest)[:topk]

    pref = [c for c in chunks if cat(c) in preferred]
    rest = [c for c in chunks if cat(c) not in preferred]
    return (pref + rest)[:topk]


def rewrite_query_for_retrieval(question: str) -> str:
    intent = detect_intent(question)
    if intent == "humor":
        return question + " humor joke why what how"
    if intent == "fun_facts":
        return question + " fun facts"
    if intent == "facts":
        return question + " anatomy diet habitat social life size trunk ears communication"

    # NEW: trunk topical expansion (default)
    if intent == "default" and is_trunk_query(question):
        return question + " trunk anatomy muscles breathing smell grasp siphon water tool"

    # NEW: tail topical expansion (default)
    if intent == "default" and is_tail_query(question):
        return question + " tail function swat flies signaling communication"

    # NEW: size topical expansion (default)
    if intent == "default" and is_size_query(question):
        return question + " size weight height shoulder height mass tonnes meters adult"

    if intent == "default" and is_definition_query(question):
        return question + " description overview characteristics habitat social behavior"

    if intent == "default" and is_reproduction_query(question):
        return question + " reproduction mating breeding gestation pregnancy calf birth musth estrus hormone"

    if intent == "default" and is_communication_query(question):
        return question + " communication rumble infrasound vocalization seismic vibration chemical scent urine dung temporal gland"

    # NEW: calf/baby topical expansion (default)
    if intent == "default" and is_calf_query(question):
        return question + " calf calves newborn juvenile mother nursing milk suckle herd care allomother babysit play learning"

    if is_single_species_traits_query(question):
        return question + " description appearance size ears tusks trunk habitat range"
    return question

def looks_bad(answer: str) -> bool:
    a = answer.strip().lower()
    if len(a) < 20:
        return True
    for pat in BAD_OUTPUT_PATTERNS:
        if re.search(pat, a):
            return True
    # too few elephant keywords is a strong signal it's nonsense
    kw = ["elephant", "african", "asian", "tusk", "trunk", "ears"]
    if sum(1 for k in kw if k in a) == 0:
        return True
    return False


def is_single_species_traits_query(q: str) -> bool:
    ql = q.lower()
    has_asian = "asian" in ql
    has_african = "african" in ql
    wants_compare = any(w in ql for w in ["difference", "different", "compare", "comparison", "versus", "vs"])
    wants_traits = any(w in ql for w in ["traits", "characteristics", "features", "describe", "description", "about"])
    return has_asian and wants_traits and (not wants_compare) and (not has_african)


def extractive_answer(
    context_chunks: List[Dict[str, Any]],
    question: str,
    max_sentences: int = 5) -> Tuple[str, Optional[int], List[str]]:
    """
    Query-aware baseline: select top sentences that best match the question.
    Keeps answers on-topic (prevents random extra facts).
    """
    q = question.lower()
    intent = detect_intent(question)
    q_terms = set(re.findall(r"[a-z0-9']+", q))

    fun_facts_mode = (intent == "fun_facts")
    fact_cap = 2 if fun_facts_mode and not wants_multiple_facts(question) else (5 if fun_facts_mode else max_sentences)

    # drop very common glue words
    stop = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "if",
        "then",
        "than",
        "so",
        "of",
        "to",
        "in",
        "on",
        "for",
        "with",
        "as",
        "at",
        "by",
        "from",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
    }
    q_terms = {t for t in q_terms if t not in stop and len(t) > 2}
    trunk_mode = intent == "default" and is_trunk_query(question)
    compare_mode = intent == "default" and is_comparison_query(question)
    calf_mode = intent == "default" and is_calf_query(question)
    tail_mode = intent == "default" and is_tail_query(question)
    size_mode = intent == "default" and is_size_query(question)
    repro_mode = intent == "default" and is_reproduction_query(question)
    comm_mode = intent == "default" and is_communication_query(question)
    definition_mode = intent == "default" and is_definition_query(question)

    def tail_chunk_score(c: Dict[str, Any]) -> int:
        t = _clean_text(c["text"]).lower()
        keys = ["tail", "swat", "flies", "insect", "balance", "signal", "communicat", "brush", "switch"]
        return sum(1 for k in keys if k in t)

    indexed_chunks = list(enumerate(context_chunks))  # (orig_idx, chunk)

    chosen_chunks = indexed_chunks
    if trunk_mode:
        # pick the 2–3 most trunk-informative chunks
        chosen_chunks = sorted(indexed_chunks, key=lambda x: trunk_chunk_score(x[1]), reverse=True)[:3]
    elif tail_mode:
        # pick the 2–3 most tail-informative chunks
        chosen_chunks = sorted(indexed_chunks, key=lambda x: tail_chunk_score(x[1]), reverse=True)[:3]
    elif compare_mode:
        # pick the 2–3 most comparison-informative chunks
        chosen_chunks = sorted(indexed_chunks, key=lambda x: compare_chunk_score(x[1]), reverse=True)[:3]

    # --- HUMOR MODE: prefer full joke units (Q + punchline) ---
    if intent == "humor":
        # build joke units from chosen chunks
        joke_units: List[Dict[str, Any]] = []
        for orig_idx, c in enumerate(context_chunks[:5]):
            for ju in extract_joke_units(c["text"]):
                joke_units.append({"joke": ju, "chunk_idx": orig_idx})

        # If we found any, pick the best one deterministically
        if joke_units:
            q_terms2 = set(re.findall(r"[a-z0-9']+", question.lower()))
            stop2 = stop  # reuse your stop set
            q_terms2 = {t for t in q_terms2 if t not in stop2 and len(t) > 2}

            def joke_score(j: str) -> int:
                st = set(re.findall(r"[a-z0-9']+", j.lower()))
                st = {t for t in st if t not in stop2 and len(t) > 2}
                score = len(q_terms2 & st)

                # small bonus if it mentions baby/calf when user asked
                if any(w in question.lower() for w in ["baby", "calf", "calves"]):
                    if any(w in j.lower() for w in ["baby", "calf", "calves"]):
                        score += 2
                return score

            best = max(joke_units, key=lambda x: joke_score(x["joke"]))
            header = "Here’s a joke:"
            return f"{header}\n- {best['joke']}", best["chunk_idx"], [best["joke"]]

    # Collect candidate sentences from top 3 chunks (enough)
    candidates: List[Dict[str, Any]] = []
    def is_joke_style(s: str) -> bool:
        sl = s.strip().lower()
        return (
            sl.startswith(("why ", "what ", "how ", "knock ", "did you"))
            or "?" in s
        )
    for local_idx, (orig_idx, c) in enumerate(chosen_chunks[:3]):
        text = _clean_text(c["text"])
        sents = re.split(r"(?<=[.!?])\s+", text)
        # Merge tiny fragments into the previous sentence (prevents broken quotes like “Fear me.”)
        merged = []
        for s in sents:
            if merged and len(s) < 20:
                merged[-1] = merged[-1].rstrip() + " " + s.lstrip()
            else:
                merged.append(s)
        sents = merged
        if intent != "humor":
            sents2 = [s for s in sents if not any(cue in s.lower() for cue in HUMOR_CUES)]
            sents = sents2 or sents
        for s in sents:
            s = s.strip()
            if definition_mode:
                sl = s.lower()
                if "elephant" not in sl:
                    continue
            if tail_mode:
                sl = s.lower()
                if "tail" not in sl:
                    continue
            if size_mode:
                sl = s.lower()
                if not any(t in sl for t in ["kg", "kilogram", "ton", "tons", "meter", "metre", "cm", "height", "tall", "weigh", "weight", "mass", "shoulder"]):
                    continue
            if repro_mode:
                sl = s.lower()
                if not any(t in sl for t in ["reproduce", "reproduction", "mating", "mate", "gestation", "pregnancy", "birth", "calving", "musth", "estrus", "cycle"]):
                    continue
            if comm_mode:
                sl = s.lower()
                if not any(t in sl for t in ["communicat", "signal", "vocal", "rumble", "sound", "call", "vibration", "seismic", "infrasound"]):
                    continue
            if calf_mode:
                sl = s.lower()
                calf_terms = ["calf", "calves", "newborn", "juvenile", "mother", "nursing", "milk", "suckle", "herd", "allomother", "play"]
                if not any(t in sl for t in calf_terms):
                    continue
            # Avoid deictic continuation sentences that become redundant as bullets
            if trunk_mode:
                sl = s.lower()
                if sl.startswith(("this structure", "this", "these", "such")) and (
                    "trunk" not in sl and "proboscis" not in sl
                ):
                    continue
            if tail_mode:
                sl = s.lower()
                if sl.startswith(("this structure", "this", "these", "such")) and "tail" not in sl:
                    continue
            if compare_mode:
                sl = s.lower()
                if sl.startswith(("this difference", "this", "these", "such")) and not (
                    "african" in sl and "asian" in sl
                ):
                    continue
                if "cultural" in sl or "religious" in sl:
                    continue
                if ("african" not in sl and "asian" not in sl) and not any(
                    w in sl for w in ["difference", "differ", "whereas", "while", "versus", "vs", "contrast", "compared"]
                ):
                    continue
            if len(s) > 25:
                candidates.append({"sent": s, "chunk_idx": orig_idx})

    if intent == "humor":
        candidates = [c for c in candidates if not c["sent"].strip().startswith(("Fear", "That’s", "That's"))]

    if is_short_description_query(question):
        filtered = [c for c in candidates if not any(t in c["sent"].lower() for t in BAD_DESC_TERMS)]
        candidates = filtered or candidates

    # If user asks for Asian-only traits (not comparison), drop comparison sentences
    if is_single_species_traits_query(question):
        filtered = []
        for c in candidates:
            sl = c["sent"].lower()
            if sl.startswith("african elephants"):
                continue
            if "african" in sl and "asian" in sl:
                continue
            if any(w in sl for w in ["differ", "difference", "while asian", "while african"]):
                continue
            if any(p in sl for p in [
                "both species",
                "each species",
                "in each species",
                "while differing",
                "also vary",
            ]):
                continue

            filtered.append(c)
        candidates = filtered or candidates

    if compare_mode:
        filtered = []
        for c in candidates:
            sl = c["sent"].lower()
            if "three species" in sl or "sole surviving" in sl or "family elephantidae" in sl:
                continue
            if "both species" in sl and not any(
                w in sl for w in ["difference", "differ", "whereas", "while", "versus", "vs", "contrast", "compared"]
            ):
                continue
            if ("african" in sl or "asian" in sl) and (
                ("african" in sl and "asian" in sl)
                or any(w in sl for w in ["difference", "differ", "whereas", "while", "versus", "vs", "contrast", "compared"])
            ):
                filtered.append(c)
        candidates = filtered or candidates

    if intent == "humor":
        joke_candidates = [c for c in candidates if is_joke_style(c["sent"])]
        if joke_candidates:
            candidates = joke_candidates

    def _calf_topic(text: str) -> Optional[str]:
        sl = text.lower()
        if any(t in sl for t in ["gestation", "pregnan", "born after", "birth again"]):
            return "gestation"
        if any(t in sl for t in ["weigh", "kg", "kilogram", "cm", "meter", "tall", "height"]):
            return "size"
        if any(t in sl for t in ["stand", "walk", "hours", "days", "mobility", "uncoordinated"]):
            return "mobility"
        if any(t in sl for t in ["vision", "smell", "hearing", "touch"]):
            return "senses"
        if any(t in sl for t in ["milk", "nursing", "suckle"]):
            return "nursing"
        if "play" in sl:
            return "play"
        if any(t in sl for t in ["mother", "herd", "allomother", "alloparent"]):
            return "care"
        return None

    def sent_score(s: str) -> int:
        st = set(re.findall(r"[a-z0-9']+", s.lower()))
        st = {t for t in st if t not in stop and len(t) > 2}
        score = len(q_terms & st)

        if fun_facts_mode:
            sl = s.lower()

            # Prefer concrete, factual elephant sentences
            factual_bonus_terms = [
                "trunk",
                "muscle",
                "ears",
                "rumble",
                "mud",
                "dust",
                "bath",
                "cool",
                "insect",
                "low-frequency",
                "vibration",
                "communicat",
            ]
            if any(t in sl for t in factual_bonus_terms):
                score += 2

            # Penalize “cute narrator voice” framing
            if any(cue in sl for cue in FUN_FACT_STYLE_PENALTY_CUES):
                score -= 2

        if calf_mode:
            sl = s.lower()
            calf_bonus_terms = ["calf", "calves", "newborn", "juvenile", "mother", "nursing", "milk", "suckle", "allomother", "play", "gestation", "birth", "pregnancy"]
            if any(t in sl for t in calf_bonus_terms):
                topic = _calf_topic(s)
                if topic in {"size", "mobility", "senses", "nursing", "play", "care"}:
                    score += 3
                elif topic == "gestation":
                    score += 1
                else:
                    score += 2
            if any(t in sl for t in ["conservation", "population", "ecosystem", "ecological", "coexistence"]):
                score -= 3

        # NEW: trunk relevance bonus
        if trunk_mode and ("trunk" in st or "proboscis" in st):
            score += 3

        # NEW: tail relevance bonus
        if tail_mode and "tail" in st:
            score += 3
        if tail_mode and "tail" not in st:
            score -= 4

        if size_mode:
            sl = s.lower()
            if any(t in sl for t in ["kg", "kilogram", "ton", "tons", "meter", "metre", "cm", "height", "tall", "weigh", "weight", "mass", "shoulder"]):
                score += 3
            else:
                score -= 2

        if repro_mode:
            sl = s.lower()
            if any(t in sl for t in ["reproduce", "reproduction", "mating", "mate", "gestation", "pregnancy", "birth", "calving", "musth", "estrus", "cycle"]):
                score += 3
            if any(t in sl for t in ["tusk", "conflict", "habitat", "forest", "savanna"]):
                score -= 2

        if comm_mode:
            sl = s.lower()
            if any(t in sl for t in ["communicat", "signal", "vocal", "rumble", "sound", "call", "vibration", "seismic", "infrasound"]):
                score += 3
            if any(t in sl for t in ["tusk", "habitat", "forest", "savanna"]):
                score -= 2

        # NEW: comparison relevance bonus
        if compare_mode:
            if "african" in st and "asian" in st:
                score += 3
            if any(w in st for w in ["difference", "differ", "whereas", "while", "versus", "vs", "contrast", "compared"]):
                score += 2
            if ("african" in st) ^ ("asian" in st):
                score -= 1
            if ("african" not in st and "asian" not in st) and not any(
                w in st for w in ["difference", "differ", "whereas", "while", "versus", "vs", "contrast", "compared"]
            ):
                score -= 2

        # small penalty: tusk-heavy sentences when user asked about trunk
        if trunk_mode and "tusk" in st and "trunk" not in st:
            score -= 4

        return score

    ranked = sorted(((sent_score(c["sent"]), c) for c in candidates), key=lambda x: x[0], reverse=True)
    ranked = [c for score, c in ranked if score > 0]

    # Fallback: if overlap scoring fails (rare), revert to first sentences
    if not ranked:
        ranked = candidates

    def _sent_key(s: str) -> str:
        toks = re.findall(r"[a-z0-9']+", s.lower())
        toks = [t for t in toks if t not in stop and len(t) > 2]
        # keep top few tokens as a crude semantic key
        return " ".join(sorted(set(toks))[:12])

    # Keep unique-ish sentences (avoid near duplicates)
    out: List[str] = []
    selected_raw: List[str] = []
    selected_chunk_idxs: List[int] = []
    used_chunk_idx: Optional[int] = None
    seen = set()
    saw_allomother = False
    seen_calf_topics = set()
    for c in ranked:
        s = c["sent"]
        s2 = s
        topic = None
        if detect_intent(question) == "fun_facts":
            s2 = strip_catchphrases(s2)

        if calf_mode:
            sl = s2.lower()
            if "allomother" in sl and saw_allomother:
                continue
            topic = _calf_topic(s2)

            if topic and topic in seen_calf_topics:
                continue

        key2 = _sent_key(s2)
        if key2 in seen:
            continue
        seen.add(key2)

        if s2.lower().startswith("african elephants typically have two"):
            s2 = "Trunk tip: " + s2
        out.append(s2)
        selected_raw.append(s)
        selected_chunk_idxs.append(c["chunk_idx"])
        if calf_mode and "allomother" in s2.lower():
            saw_allomother = True
        if calf_mode:
            if topic:
                seen_calf_topics.add(topic)

        if fun_facts_mode:
            out = out[:fact_cap]
            selected_raw = selected_raw[:fact_cap]


        if len(out) >= max_sentences:
            break

    # Light formatting for readability
    bullets = "\n".join(f"- {s}" for s in out)

    if selected_chunk_idxs:
        used_chunk_idx = Counter(selected_chunk_idxs).most_common(1)[0][0]

    if not out and tail_mode:
        return "I don't know based on the provided information. (No context mentions: tail)", None, []
    if not out and size_mode:
        return "I don't know based on the provided information. (No context mentions: size)", None, []

    if fun_facts_mode:
        header = (
            "Here are a few fun elephant facts:"
            if wants_multiple_facts(question)
            else "Here’s a fun elephant fact:"
        )
    elif is_short_description_query(question):
        header = "Short description:"
    elif is_single_species_traits_query(question):
        header = "Here are a few quick traits:"
    else:
        header = "Here’s what I found:"

    return f"{header}\n{bullets}", used_chunk_idx, selected_raw


def retrieve_context(index: Dict[str, Any], question: str, topk: int, hist_path: Path) -> List[Dict[str, Any]]:
    intent = detect_intent(question)
    retrieval_q = rewrite_query_for_retrieval(question)

    ranked = bm25_score_query(index, retrieval_q, topk=topk * 50)
    ranked = diversify_by_source(index, ranked, topk=topk * 10, max_per_source=1)

    chunks = index["chunks"]
    allow = allowed_categories_for_intent(intent)

    # Hard filter by allowed category
    filtered = []
    for doc_id, score in ranked:
        c = chunks[doc_id]
        cat = _category_from_source(c["source"])
        # Hard allow-list when routed
        if allow is not None and cat not in allow:
            continue

        # Soft exclude-list in default
        if should_exclude_category(intent, cat):
            continue
        filtered.append((doc_id, score))

    # take extra before final trimming (we may filter later for "another")
    ctx = [chunks[doc_id] for doc_id, _score in filtered][: topk * 3]

    def _has_any(text: str, words: List[str]) -> bool:
        tl = _clean_text(text).lower()
        return any(w in tl for w in words)

    if intent == "default" and is_reproduction_query(question):
        must = ["gestation", "pregnan", "mating", "mate", "birth", "calf", "musth", "estrus"]
        ctx2 = [c for c in ctx if _has_any(c["text"], must)]
        ctx = ctx2

    if intent == "default" and is_communication_query(question):
        must = ["communicat", "rumble", "infrasound", "vocal", "seismic", "vibration", "scent", "urine", "dung", "temporal"]
        ctx2 = [c for c in ctx if _has_any(c["text"], must)]
        ctx = ctx2

    # ... after ctx computed (topk*3)
    if intent in {"fun_facts", "humor"} and wants_another(question):
        hist = load_history(hist_path)
        seen_chunks = set(hist.get(intent, []))
        seen_sents = set(hist.get(f"{intent}_sentences", []))
        seen_ids = set(hist.get(f"{intent}_ids", []))
        last_id = (hist.get(f"{intent}_last_id") or "").strip()

        # Prefer not to repeat the immediately previous chunk
        if last_id:
            ctx_no_last = [c for c in ctx if (c.get("id") or "").strip() != last_id]
            if ctx_no_last:
                ctx = ctx_no_last

        # filter out previously used chunks
        ctx2 = []
        ctx_ids_only = []
        for c in ctx:
            cid = (c.get("id") or "").strip()
            if cid and cid in seen_ids:
                continue
            ctx_ids_only.append(c)
            if _fingerprint(c["text"]) in seen_chunks:
                continue
            if seen_sents:
                sent_fps = set(_sentence_fingerprints(c["text"]))
                overlap = len(sent_fps & seen_sents)
                if overlap >= 2:
                    continue
            ctx2.append(c)

        # if everything got filtered, fallback to id-only filter before original ctx
        if ctx2:
            ctx = ctx2
        elif seen_ids and ctx_ids_only:
            ctx = ctx_ids_only

    # If user asks about trunks in default mode, require trunk/proboscis presence
    if intent == "default" and is_trunk_query(question):
        ctx2 = []
        for c in ctx:
            tl = _clean_text(c["text"]).lower()
            if "trunk" in tl or "proboscis" in tl:
                ctx2.append(c)
        ctx = ctx2 or ctx

    # Optional reorder for traits, then cut back to topk
    ctx = category_boost_order(ctx, question, topk=topk)

    return ctx


def build_prompt(context_chunks: List[Dict[str, Any]], question: str) -> str:
    ctx_lines = []
    for c in context_chunks:
        cat = _category_from_source(c["source"])
        ctx_lines.append(f"[{cat}] {_clean_text(c['text'])}")

    context_block = "\n".join(ctx_lines)

    return (
        "Instruction: Answer the question using ONLY the context. "
        "If the context does not contain the answer, say: "
        '"I don\'t know based on the provided information."\n\n'
        f"Context:\n{context_block}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )


def run_llmlib_infer(config_path: Path, prompt: str) -> str:
    """
    `llmlib infer` is interactive. We feed:
      <prompt>\nexit\n

    We must parse the output that corresponds to the FIRST prompt,
    not any later outputs (e.g., from 'exit').
    """
    cmd = ["llmlib", "infer", "--config", str(config_path)]
    proc = subprocess.run(
        cmd,
        input=prompt + "\nexit\n",
        text=True,
        capture_output=True,
    )

    stdout = proc.stdout or ""
    stderr = proc.stderr or ""

    if proc.returncode != 0:
        return f"[llmlib infer failed]\n{stderr}\n\n[stdout]\n{stdout}"

    # Strategy:
    # 1) Find the first "Output :" after our first prompt was entered.
    # In llmlib infer logs, it usually prints:
    #   Prompt : <your prompt>
    #   Output : <generation>
    #
    # We'll extract the FIRST Output block we see.
    m = re.search(r"Output\s*:\s*(.*)", stdout)
    if m:
        return m.group(1).strip()

    # Fallback: show last lines for debugging
    return "[Could not parse Output block]\n" + "\n".join(stdout.splitlines()[-80:])


def save_history_for_intent(
    hist_path: Path,
    intent: str,
    used_chunk_id: Optional[str],
    used_chunk_text: str,
    selected_sentences: List[str],) -> None:
    hist = load_history(hist_path)
    hist.setdefault(intent, [])
    hist.setdefault(f"{intent}_ids", [])
    hist.setdefault(f"{intent}_sentences", [])
    if used_chunk_id:
        cleaned_id = used_chunk_id.strip()
        hist[f"{intent}_ids"].append(cleaned_id)
        hist[f"{intent}_last_id"] = cleaned_id
    hist[intent].append(_fingerprint(used_chunk_text))
    hist[f"{intent}_sentences"].extend(_fingerprint(s) for s in selected_sentences)
    hist[f"{intent}_ids"] = hist[f"{intent}_ids"][-80:]
    hist[intent] = hist[intent][-80:]  # keep last N
    hist[f"{intent}_sentences"] = hist[f"{intent}_sentences"][-300:]
    save_history(hist_path, hist)
