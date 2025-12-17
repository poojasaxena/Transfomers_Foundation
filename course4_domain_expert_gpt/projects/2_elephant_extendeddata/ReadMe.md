## Data Generation
```
$ python src/llmlib/data/run_full_pipeline.py  
=== Step 1: Prepare raw corpus ===
Found raw files: [PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/QA.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/african.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/asian.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/domain.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/fun_info.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/national_day.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/paraphrases.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/reasoning.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/synthetic.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/human/conversations.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/human/synthetic_smalltalk.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/human/user_writing.txt')]
Wrote /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/elephant_human_90_10_corpus.txt | lines: 3851, chars: 491931
=== Step 2: Dedupe and filter corpus ===
Orig: 3851 | Unique: 3851 | Filtered: 3486
=== Step 3: Split corpus ===
Split statistics:
train: {'lines': 3418, 'chars': 309551, 'words': 52407}
val: {'lines': 34, 'chars': 3221, 'words': 552}
test: {'lines': 34, 'chars': 2846, 'words': 492}
=== Step 4: Generate synthetic expansions ===
Wrote 9116 synthetic lines to /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/synthetic_generated.txt
=== Step 5: Corpus statistics ===
train.txt: lines 3418, chars 309551, words 52407
val.txt: lines 34, chars 3221, words 552
test.txt: lines 34, chars 2846, words 492
train.txt: {'lines': 3418, 'chars': 309551, 'words': 52407}
val.txt: {'lines': 34, 'chars': 3221, 'words': 552}
test.txt: {'lines': 34, 'chars': 2846, 'words': 492}
```

## Tokenizer preparation
### 1. Byte_bpe_tokenizer Test
 * to make sure decode/encode works fine
```
$ cd $LLMLIB_ROOT
python -m scripts.tokenization.sanity_byte_bpe_tokenizer
Vocab size: 280
----
INPUT   : hello
IDS     : [2, 270, 3]
DECODED : hello
----
INPUT   : hello elephants
IDS     : [2, 270, 36, 267, 3]
DECODED : hello elephants
----
INPUT   : where elephants live?
IDS     : [2, 274, 36, 267, 36, 279, 3]
DECODED : where elephants live?
----
INPUT   : Elephants live in Africa and Asia.
IDS     : [2, 73, 112, 105, 116, 108, 101, 114, 120, 119, 36, 278, 36, 109, 114, 36, 69, 106, 118, 109, 103, 101, 36, 101, 114, 104, 36, 69, 119, 109, 101, 50, 3]
DECODED : Elephants live in Africa and Asia.
```

### 2. Training Script test
```
$ cd %LLMLIB_ROOT
$ python -m scripts.tokenization.sanity_bpe_training
Text      : Hello elephants!
Token IDs : [2, 1599, 36, 329, 37, 3]
Decoded   : Hello elephants!

```


## Training Pipeline
### 1. Train Tokenizer
```
$ train-tokenizer --config 2_elephant_extendeddata/config.json --tokenizer-type byte_bpe --vocab-size 5096
[INFO] Project config loaded from: /home/pooja-saxena/PoojaVault/Professional/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/2_elephant_extendeddata/config.json
[OK] Trained tokenizer
     Saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/tokenizers/bpe-elephant/v2/tokenizer.json
     Type: byte_bpe, Vocab size: 5096

```

### 2. Train model
```
$ modern-gpt-train --config 2_elephant_extendeddata/config.json --device auto 

2025-12-16 18:40:48,872 | INFO | llmlib.cli.modern_gpt_train_cli | [modern-gpt-train] Using device: cpu
2025-12-16 18:40:48,874 | INFO | llmlib.cli.modern_gpt_train_cli | [modern-gpt-train] Using data file: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/train.txt
2025-12-16 18:40:48,897 | INFO | llmlib.cli.modern_gpt_train_cli | [modern-gpt-train] Tokenizer vocab size: 5096

============================================================
🚀 modern-gpt-train
============================================================
Model Name       : gpt-bpe-v2
Vocabulary Size  : 5096
d_model          : 192
n_heads          : 4
n_layers         : 4
dropout          : 0.1
max_seq_length   : 128
batch_size       : 8
learning_rate    : 0.0005
train_steps      : 10000
============================================================

Step 0, Train Loss: 8.5636, Val Loss: 8.2680
Step 100, Train Loss: 1.8319, Val Loss: 4.4170
...
...
Step 9600, Train Loss: 0.1207, Val Loss: 2.1023
Step 9700, Train Loss: 0.1504, Val Loss: 2.1112
Step 9800, Train Loss: 0.1489, Val Loss: 2.1167
Step 9900, Train Loss: 0.3392, Val Loss: 2.1313

[modern-gpt-train] Model saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v2/model.pt
[modern-gpt-train] Tokenizer saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v2/tokenizer.json


```

### 3. Inference
```
$ modern-gpt-infer  --config 2_elephant_extendeddata/config.json  --device auto  
2025-12-17 14:28:48,679 | INFO | llmlib.cli.modern_gpt_infer_cli | [modern-gpt-infer] Using device: cpu

============================================================
🧠 Modern GPT Inference
============================================================
Project config     : ~/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/2_elephant_extendeddata/config.json
Model directory    : ~/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v2
Checkpoint         : ~/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v2/model.pt
Model config       : ~/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v2/model_config.json
Tokenizer type     : ByteBPETokenizer
Vocab size         : 5096
Special tokens     : ['<pad>', '<unk>', '<bos>', '<eos>']
Device             : cpu
Max sequence len   : 128
Max new tokens     : 80
============================================================

🤖 Interactive ModernGPT Inference
Type your prompts below. Type 'quit', 'exit', or press Ctrl+C to stop.

Enter a prompt: hello
---
Prompt : hello
Output : hello Strange of the U.S. Geological Surated southern Neples in Southern Africa

Enter a prompt: What is an elephant?
---
Prompt : What is an elephant?
Output : What is an elephant? Do you sometimes tell billions lunch

Enter a prompt: tell me somethign about elephant?
---
Prompt : tell me somethign about elephant?
Output : tell me somethign about elephant? In the mountains (Palaeoloxodon cy 14 20 40 14 Palaeoloxodon falconeri, 20 02, 20, 40 6, 206, 20, Mali recy, 40 32 maximus 4,000 BCE and temperatures around 4][4][note height of the 

```