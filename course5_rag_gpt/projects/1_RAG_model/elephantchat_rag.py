#!/usr/bin/env python3
"""
elephantchat_rag.py (Step 3)

Uses:
- llmlib BM25 retriever (Step 2) to fetch context chunks
- your trained model via `llmlib infer --config ...` to generate an answer

Usage:
  python3 elephantchat_rag.py \
    --config /path/to/config_9.json \
    --index  /path/to/bm25_index.pkl \
    --q "Difference between African and Asian elephants?" \
    --topk 5 \
    --show-context
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from llmlib.data.rag.kb_bm25_retriever import load_index

from rag_utils import (
    _category_from_source,
    _clean_text,
    allowed_categories_for_intent,
    detect_intent,
    coverage_ok,
    extractive_answer,
    history_path_from,
    is_topic_query,
    is_trunk_query,
    looks_bad,
    retrieve_context,
    run_llmlib_infer,
    save_history_for_intent,
    wants_another,
)


def _strip_header(answer: str) -> str:
    lines = [ln for ln in answer.splitlines() if ln.strip()]
    if not lines:
        return answer
    if lines[0].endswith(":") and any(ln.lstrip().startswith("-") for ln in lines[1:]):
        return "\n".join(lines[1:]).strip()
    return answer


def _say_unknown() -> None:
    print("\n🦣 ElephantChat:\nI don’t know based on the provided information.\n")


def _answer_question(args, question: str, show_answer_header: bool = True, show_timing: bool = False) -> None:
    start = time.perf_counter()
    index = load_index(Path(args.index))
    hist_path = history_path_from(Path(__file__))
    ctx = retrieve_context(index, question, topk=args.topk, hist_path=hist_path)

    intent = detect_intent(question)
    if intent != "humor" and is_topic_query(question) and not coverage_ok(question, ctx):
        _say_unknown()
        return
    if not ctx:
        _say_unknown()
        return
    if args.show_context:
        print("\n===== ROUTER =====")
        print(f"intent: {intent}")
        print(f"wants_another: {wants_another(question)}")
        print(f"allowed_categories: {allowed_categories_for_intent(intent) or 'ALL'}")
        if intent == "default" and is_trunk_query(question):
            print("topic_guard: trunk_only_chunks=on")
        print(f"history_file: {hist_path}")

        print("\n===== RETRIEVED CONTEXT =====")
        for i, c in enumerate(ctx, start=1):
            print(f"\n[{i}] {c['id']}  ({_category_from_source(c['source'])})")
            print(_clean_text(c["text"])[:700] + ("..." if len(c["text"]) > 700 else ""))

    max_sents = 1 if intent == "humor" else 5
    baseline, used_chunk_idx, selected_sentences = extractive_answer(ctx, question, max_sentences=max_sents)

    # Ask model to rewrite baseline (not raw context)
    rewrite_prompt = (
        "Rewrite the answer below in 3–5 concise sentences. "
        "Do not add any new facts not present in the answer. "
        "Do not use meta phrases like 'I should' or 'as an AI'.\n\n"
        f"Answer to rewrite:\n{baseline}\n\n"
        "Rewritten answer:"
    )

    if show_answer_header:
        print("\n===== ANSWER =====\n")
    model_ans = run_llmlib_infer(Path(args.config), rewrite_prompt)

    used_chunk = None
    if used_chunk_idx is not None and used_chunk_idx < len(ctx):
        used_chunk = ctx[used_chunk_idx]

    if intent in {"fun_facts", "humor"} and used_chunk:
        save_history_for_intent(
            hist_path,
            intent=intent,
            used_chunk_id=used_chunk.get("id"),
            used_chunk_text=used_chunk["text"],
            selected_sentences=selected_sentences,
        )

    if looks_bad(model_ans):
        # fallback: always correct + coherent
        final_ans = baseline
    else:
        final_ans = model_ans

    if not show_answer_header:
        final_ans = _strip_header(final_ans)

    if not show_answer_header:
        print(f"🦣 ElephantChat:\n {final_ans}")
    else:
        print(final_ans)

    if show_timing:
        elapsed = time.perf_counter() - start
        print(f"{'':>20}⏱ {elapsed:.2f}s")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config",
                    default=str(Path.home() / "PoojaVault/Professional/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/9_extended_data/config_9.json"),
                    help="Path to config_9.json (or whichever)")
    ap.add_argument(
        "--index",
        default=str(Path.home() / "PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/kb_chunks/bm25_index.pkl"),
        help="Path to bm25_index.pkl"
    )
    ap.add_argument("--q", help="User question")
    ap.add_argument("--topk", type=int, default=5, help="Number of context chunks")
    ap.add_argument("--show-context", action="store_true", help="Print retrieved chunks")
    ap.add_argument("--interactive", action="store_true", help="Start a prompt loop for multiple questions")
    args = ap.parse_args()

    if args.interactive:
        print("🦣 ElephantChat — ask me anything about elephants.")
        print("Type 'exit' to quit. Try: 'fun facts', 'a joke', 'elephant trunks', 'baby elephants'.")
        while True:
            q = input("🟩 You: ")
            if not q or q.lower() in {"exit", "quit", "q"}:
                break
            _answer_question(args, q, show_answer_header=False, show_timing=True)
        return 0

    if not args.q:
        ap.error("--q is required unless --interactive is set")

    _answer_question(args, args.q)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
