## Training the Model
```
$ modern-gpt-train --config 3_elephant_improved/config.json --device auto
2025-12-17 14:48:14,684 | INFO | llmlib.cli.modern_gpt_train_cli | [modern-gpt-train] Using device: cpu
2025-12-17 14:48:14,684 | INFO | llmlib.cli.modern_gpt_train_cli | [modern-gpt-train] Using data file: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/train.txt
2025-12-17 14:48:14,695 | INFO | llmlib.cli.modern_gpt_train_cli | [modern-gpt-train] Tokenizer vocab size: 5096
PAD: 0
BOS: 2
EOS: 3
 
============================================================
🚀 modern-gpt-train
============================================================
Model Name       : gpt-bpe-v3
Vocabulary Size  : 5096
d_model          : 256
n_heads          : 8
n_layers         : 6
dropout          : 0.1
max_seq_length   : 256
batch_size       : 12
learning_rate    : 0.0003
train_steps      : 12000
============================================================

Step 0, Train Loss: 8.4482, Val Loss: 7.4214
Step 1, Train Loss: 7.5056, Val Loss: 6.9914
Step 2, Train Loss: 6.9601, Val Loss: 6.7810
Step 3, Train Loss: 6.7072, Val Loss: 6.6456
....
....
Step 9600, Train Loss: 0.5091, Val Loss: 2.0390
Step 9800, Train Loss: 0.3749, Val Loss: 2.0675
Step 10000, Train Loss: 0.5459, Val Loss: 2.1864
Step 10200, Train Loss: 0.3641, Val Loss: 2.0128
Step 10400, Train Loss: 0.3836, Val Loss: 2.1541
Step 10600, Train Loss: 0.2920, Val Loss: 2.1308
Step 10800, Train Loss: 0.4287, Val Loss: 2.1547
Step 11000, Train Loss: 0.4984, Val Loss: 2.0674
Step 11200, Train Loss: 0.2843, Val Loss: 2.0555
Step 11400, Train Loss: 0.3689, Val Loss: 2.0405
Step 11600, Train Loss: 0.4153, Val Loss: 2.1907
Step 11800, Train Loss: 0.3988, Val Loss: 2.1849

[modern-gpt-train] Model saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v3/model.pt
[modern-gpt-train] Tokenizer saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v3/tokenizer.json
```

## Inference
```
$ $modern-gpt-infer  --config 3_elephant_improved/config.json
2025-12-17 17:52:07,502 | INFO | llmlib.cli.modern_gpt_infer_cli | [modern-gpt-infer] Using device: cpu

============================================================
🧠 Modern GPT Inference
============================================================
Project config     : ~/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/3_elephant_improved/config.json
Model directory    : ~/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v3
Checkpoint         : ~/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v3/model.pt
Model config       : ~/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v3/model_config.json
Tokenizer type     : ByteBPETokenizer
Vocab size         : 5096
Special tokens     : ['<pad>', '<unk>', '<bos>', '<eos>']
Device             : cpu
Max sequence len   : 256
Max new tokens     : 120
============================================================

🤖 Interactive ModernGPT Inference
Type your prompts below. Type 'quit', 'exit', or press Ctrl+C to stop.

Enter a prompt: Hello
---
Prompt : Hello
Output : Hellofetous

Enter a prompt: What is Tusk?
---
Prompt : What is Tusk?
Output : What is Tusk? polostril gitiles as well?

Enter a prompt: Tell me something about elephant?
---
Prompt : Tell me something about elephant?
Output : Tell me something about elephant? They might eat things that cannot other, almost too low for many day because they flopise because they also can hear this low sareusnack at accidentally around sounds — but too many nabed the ground.

Enter a prompt: Where do african elephant found?
---
Prompt : Where do african elephant found?
Output : Where do african elephant found?” You can run about 1 ses.

Enter a prompt: Elephants are
---
Prompt : Elephants are
Output : Elephants are among the largest land animal land animal. They and ear er alated each other by certain ears and take more vices

Enter a prompt: Elephants eat
---
Prompt : Elephants eat
Output : Elephants eat grasses, leaves, and fruit. They and separated in the "shiny and Har).
```


## 📈 Overall Assessment
Score: 6/10

✅ Training infrastructure works perfectly
✅ Model architecture scales properly
⚠️ Overfitting is the main issue
⚠️ Generation quality needs improvement

## Requirement
1. Collect more data