from llmlib.io import load_project_config
from llmlib.bpe_training import train_and_save_tokenizer


def main():
    cfg = load_project_config(__file__, config_filename="config.json")
    tokenizer, path = train_and_save_tokenizer(cfg)
    print(f"[OK] Tokenizer trained and saved at {path}")


if __name__ == "__main__":
    main()
