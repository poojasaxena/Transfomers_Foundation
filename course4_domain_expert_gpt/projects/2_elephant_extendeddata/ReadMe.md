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

## Training Pipeline
### 1. Train Tokenizer
```
$ train-tokenizer --config 2_elephant_extendeddata/config.json --tokenizer-type byte_bpe --vocab-size 5096

[INFO] Project config loaded from: /home/pooja-saxena/PoojaVault/Professional/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/2_elephant_extendeddata/config.json
[OK] Trained tokenizer
     Saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/tokenizers/bpe-elephant/v2/tokenizer.json
     Type: byte_bpe, Vocab size: 5095
```

### 2. Train model
```
$ modern-gpt-train --config 2_elephant_extendeddata/config.json --device auto
[modern-gpt-train] Using device: cpu
[modern-gpt-train] Using data file: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/train.txt
[modern-gpt-train] Tokenizer trained. Vocab size: 4095

[modern-gpt-train] Starting training...

Step 0, Loss: 8.3709
Step 100, Loss: 7.6240
Step 200, Loss: 7.1993
Step 300, Loss: 6.4322
Step 400, Loss: 5.6664
Step 500, Loss: 5.1051
Step 600, Loss: 4.9881
Step 700, Loss: 4.5660
Step 800, Loss: 4.3746
Step 900, Loss: 3.7866
Step 1000, Loss: 3.5305
Step 1100, Loss: 3.3930
Step 1200, Loss: 2.8852
Step 1300, Loss: 2.7882
Step 1400, Loss: 2.6945
Step 1500, Loss: 2.4182
Step 1600, Loss: 2.2802
Step 1700, Loss: 1.9161
Step 1800, Loss: 1.4340
Step 1900, Loss: 1.6183
Step 2000, Loss: 1.4268
Step 2100, Loss: 1.3202
Step 2200, Loss: 1.2081
Step 2300, Loss: 0.9820
Step 2400, Loss: 0.9922
Step 2500, Loss: 1.0590
Step 2600, Loss: 0.9157
Step 2700, Loss: 0.8373
Step 2800, Loss: 0.8654
Step 2900, Loss: 0.7950
[modern-gpt-train] Model + tokenizer saved at: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v2
```

### 3. Inference
```
$ modern-gpt-infer  --config 2_elephant_extendeddata/config.json  --device auto --interactive

============================================================
🧠 Modern GPT Inference
============================================================
Project config     : /home/pooja-saxena/PoojaVault/Professional/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/2_elephant_extendeddata/config.json
Model directory    : /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v2
Checkpoint         : /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v2/model.pt
Model config       : /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v2/model_config.json
Tokenizer          : /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v2/tokenizer.json
Device             : cpu
============================================================

[modern-gpt-infer] Interactive mode (Ctrl+C to exit)

>>> hi therer

------------------------------------------------------------
Prompt : hi therer
Output : ht5vvCCM
------------------------------------------------------------

>>> how are you?

------------------------------------------------------------
Prompt : how are you?
Output : ?ctlmni-Ke
------------------------------------------------------------

>>> where elephants live?

------------------------------------------------------------
Prompt : where elephants live?
Output : e?Ys
------------------------------------------------------------


```