from llmlib.tokenization.training.bpe_training import train_and_save_tokenizer
from llmlib.tokenization.byte_bpe_tokenizer import ByteBPETokenizer

tok, path = train_and_save_tokenizer(
    project_config,
    tokenizer_class=ByteBPETokenizer,
    vocab_size=8000,
    seed=42
)
