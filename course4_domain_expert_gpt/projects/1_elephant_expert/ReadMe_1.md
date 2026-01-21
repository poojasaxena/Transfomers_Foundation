## Introduction
* This project is designed to create the `elephant-expert-gpt` trained on elephant specific dataset. 
* It use byte-bpe-tokenizer, however, does not implement any special tokens ["<pad>", "<unk>", "<bos>", "<eos>"] so far. 
* The tokens were 4096, which were not proved to be emough for model to be abel to talk anything sensible. 
> Summmary: whole chain is ready, I just need to collect more data.


## Config
* config.json
```
{
    "model_config": {
      "d_model": 192,
      "n_heads": 6,
      "n_layers": 6,
      "max_position_embeddings": 256,
      "dropout": 0.1
    },
    "training_config": {
      "batch_size": 8,
      "block_size": 128,
      "learning_rate": 0.0005,
      "train_steps": 2000,
      "num_epochs": 3,
      "eval_interval": 100,
      "eval_iters": 200
    },
    "project_metadata": {
      "model_name": "gpt-bpe-v1",
      "model_save_path": "llm/language_models/elephantdomain_gpt/",
      "tokenizer_save_path": "llm/tokenizers/bpe-elephant/v1/tokenizer.json",
      "data_path": "llm/mixed_text/out",
      "data_file": "train.txt",
      "max_seq_length": 128,
      "max_new_tokens": 80
    },
    "data": {
      "root_path": "llm/splits",
      "train_file": "train.txt",
      "val_file": "val.txt",
      "test_file": "test.txt"
    },
   "tokenizer_config": {
      "type": "byte_bpe", 
      "vocab_size": 4096,
      "min_freq": 2,
      "special_tokens": ["<pad>", "<unk>", "<bos>", "<eos>"]
    }
  }
  
``` 

## Dataset structure
```
$GLOBAL_DATASETS_DIR/llm/mixed_text_v2/
├── raw/                     # raw source files you will collect/paste
│   ├── your_journal.txt
│   ├── conversations.txt
│   ├── wiki_snippets.txt
│   └── synthetic_generated.txt
├── corpus.txt               # merged raw
├── corpus.cleaned.txt       # cleaned + normalized
├── corpus.dedup.txt         # deduped
├── train.txt
├── val.txt
└── test.txt
```

## Model Building Cycle
1. Tokenization
```
$ train-tokenizer --config 1_elephant_expert/config.json --tokenizer-type byte_bpe --vocab-size 4096
[INFO] Project config loaded from: /home/pooja-saxena/PoojaVault/Professional/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/1_elephant_expert/config.json
[OK] Trained tokenizer
     Saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/tokenizers/bpe-elephant/v1/tokenizer.json
     Type: byte_bpe, Vocab size: 4095
```

2. Run Model
```
$ tiny-gpt-train --config 1_elephant_expert/config.json       
[modern-gpt-train] Using device: cpu
[modern-gpt-train] Using data file: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/train.txt
[modern-gpt-train] Tokenizer trained. Vocab size: 5096

[modern-gpt-train] Starting training...

Step 0, Loss: 8.4804
Step 100, Loss: 4.1761
Step 200, Loss: 3.9833
...
...
Step 9300, Loss: 0.4263
Step 9400, Loss: 0.4079
Step 9500, Loss: 0.5277
Step 9600, Loss: 0.5920
Step 9700, Loss: 0.4692
Step 9800, Loss: 0.6044
Step 9900, Loss: 0.4550
[modern-gpt-train] Model + tokenizer saved at: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v1
```

3. Infer 
```
$ tiny-gpt-infer --config 1_elephant_expert/config.json --interactive

============================================================
🧠 Modern GPT Inference
============================================================
Project config     : /home/pooja-saxena/PoojaVault/Professional/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/1_elephant_expert/config.json
Model directory    : /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v1
Checkpoint         : /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v1/model.pt
Model config       : /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v1/model_config.json
Tokenizer          : /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v1/tokenizer.json
Device             : cpu
============================================================

[modern-gpt-infer] Interactive mode (Ctrl+C to exit)

>>> Tell me something ahout elephant

------------------------------------------------------------
Prompt : Tell me something ahout elephant
Output : Tell me something ahout elephant
Human 1: Nice! I hope to volunteer to cook for the team in our next team offsite :)
E2: The scent in the air is changing. It must be. A single joint injury can threaten survival. Evolution
------------------------------------------------------------

>>> What is a tusk?

------------------------------------------------------------
Prompt : What is a tusk?
Output : What is a tusk? 5 mean “trunk.”
Question: Human 1: Get out of town!
------------------------------------------------------------

>>> ARe elephants big?

------------------------------------------------------------
Prompt : ARe elephants big?
Output : ARe elephants big? fruit helps food, and greeting hands. Do you know sharing any good plans for the break?
------------------------------------------------------------


```