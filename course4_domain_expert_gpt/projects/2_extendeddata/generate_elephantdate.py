import random
from pathlib import Path

OUTPUT_FILE = Path("QA_generated.txt")

subjects = [
    "elephants",
    "African elephants",
    "Asian elephants",
    "baby elephants",
]

facts = [
    ("are mammals", "They give birth to live young."),
    ("have trunks", "Trunks help them eat, drink, and communicate."),
    ("are intelligent", "They can solve problems and remember places."),
    ("are herbivores", "They eat grass, leaves, and fruit."),
    ("live in groups", "Herds provide safety and learning."),
]

why_reasons = [
    ("Why do elephants flap their ears?",
     "They flap their ears to cool down."),
    ("Why do elephants migrate?",
     "They migrate to find food and water."),
    ("Why are elephants endangered?",
     "Poaching and habitat loss threaten them."),
]

def generate_factual_qas(n=200):
    qas = []
    for _ in range(n):
        s = random.choice(subjects)
        f, a = random.choice(facts)
        q = f"What do you know about {s}?"
        ans = f"{s.capitalize()} {f}. {a}"
        qas.append((q, ans))
    return qas

def generate_reasoning_qas(n=100):
    return random.choices(why_reasons, k=n)

def main():
    all_qas = []
    all_qas.extend(generate_factual_qas(300))
    all_qas.extend(generate_reasoning_qas(200))

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for q, a in all_qas:
            f.write(f"Q: {q}\n")
            f.write(f"A: {a}\n\n")

    print(f"Generated {len(all_qas)} QA pairs → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
