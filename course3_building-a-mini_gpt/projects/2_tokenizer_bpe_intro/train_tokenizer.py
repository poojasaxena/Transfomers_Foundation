# course3_building-a-mini_gpt/projects/2_tokenizer_bpe_intro/train_tokenizer.py

from __future__ import annotations

from pathlib import Path

from llmlib import BPETokenizer, BPETokenizerConfig
from llmlib.io import (
    load_project_config,
    get_data_file_path,
    get_global_model_dir,
    get_tokenizer_path
)


def read_corpus(path: Path) -> list[str]:
    """
    Read non-empty lines from the corpus file.
    """
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def main() -> None:
    # 1) Load this project's config (same pattern as tiny_transformer project)
    cfg = load_project_config(__file__, config_filename="project_config.json")

    # Top-level structure:
    # {
    #   "tokenizer_config": {...},
    #   "project_metadata": {...}
    # }
    tok_cfg = cfg.get("tokenizer_config", {})
    meta = cfg.get("project_metadata", cfg)

    # 2) Resolve data file using existing IO helper
    data_file_path = get_data_file_path(
        cfg
    )  # uses data_path + data_file under GLOBAL_DATASETS_DIR
    texts = read_corpus(data_file_path)

    # 3) Build tokenizer config + train
    tokenizer_config = BPETokenizerConfig(word_end=tok_cfg.get("word_end", "</w>"))

    tokenizer = BPETokenizer.train(
        texts=texts,
        vocab_size=tok_cfg["vocab_size"],
        config=tokenizer_config,
        min_freq=tok_cfg.get("min_freq", 2),
    )

    # 4) Resolve save path using global *model* dir helper
    models_root = get_global_model_dir()  # e.g. ~/.llm_models or $GLOBAL_MODELS_DIR
    rel_path = meta[
        "tokenizer_save_path"
    ]  # e.g. "llm/tokenizers/bpe-greet-v1/tokenizer.json"
    save_path = get_tokenizer_path(cfg)
    tokenizer.save(save_path)


    print(f"[OK] Trained tokenizer '{meta['tokenizer_name']}'")
    print(f"     Vocab size: {len(tokenizer.vocab)}")
    print(f"     # merges:   {len(tokenizer.merges)}")
    print(f"     Saved to:   {save_path.resolve()}")


if __name__ == "__main__":
    main()
