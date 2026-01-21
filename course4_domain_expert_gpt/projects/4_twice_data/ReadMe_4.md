## Comments
1. Data is good amount 
2. Due to RAM constrained, we decided to relax the model architecture, however inference looks promising than before.
3. But as it look like, we still have room for model complexity, since the training was over in less than two hours. So in next project, we will complex the architecture.

## Data Preparation
```
📊 Key outputs:
   train.txt: 10,844 lines (1.2MB)
   val.txt: 1,355 lines (0.2MB)
   test.txt: 1,355 lines (0.2MB)
```

### Full pipeline
```
$ run-data-pipeline     


🐘 Enhanced Elephant LLM Data Pipeline Starting...
📁 Data directory: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out

=== Step 1: Prepare raw corpus ===
Found raw files: [PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/augmented_corpus.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/QA.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/african.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/asian.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/domain.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/fun_info.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/national_day.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/paraphrases.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/reasoning.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/synthetic.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/human/conversations.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/human/synthetic_smalltalk.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/human/user_writing.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/synthetic_advanced.txt'), PosixPath('/home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/web_scraped_elephants.txt')]
Wrote /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/elephant_human_90_10_corpus.txt | lines: 9142, chars: 987622

=== Step 2: Generate basic synthetic expansions ===
Wrote 20000 synthetic lines to /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/synthetic_generated.txt

=== Step 3: Advanced data generation ===
Running advanced_synth_expand.py...
✅ advanced_synth_expand.py completed successfully
Output: 🤖 Generating synthetic elephant data...
  📝 Generating fact variations...
  💬 Generating conversations...
  ❓ Generating Q&A pairs...
  📖 Generating descriptive passages...
✅ Generated 720 synthetic items
📁 Saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/synthetic_advanced.txt
📊 File size: 140.5 KB

🎉 Synthetic data generation complete!
Generated 720 items in /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/synthetic_advanced.txt
Running web_scrape_elephants.py...
✅ web_scrape_elephants.py completed successfully
Output: 📚 Generating educational facts...
🌐 Scraping Wikipedia content...
📡 Scraping: https://en.wikipedia.org/wiki/Elephant
📡 Scraping: https://en.wikipedia.org/wiki/African_elephant
📡 Scraping: https://en.wikipedia.org/wiki/Asian_elephant
📡 Scraping: https://en.wikipedia.org/wiki/Elephant_behavior
❌ Error scraping https://en.wikipedia.org/wiki/Elephant_behavior: 403 Client Error: Too many requests. Please respect our robot policy https://w.wiki/4wJS. (dd12474) for url: https://en.wikipedia.org/wiki/Elephant_behavior
📡 Scraping: https://en.wikipedia.org/wiki/Elephant_cognition
❌ Error scraping https://en.wikipedia.org/wiki/Elephant_cognition: 403 Client Error: Too many requests. Please respect our robot policy https://w.wiki/4wJS. (dd12474) for url: https://en.wikipedia.org/wiki/Elephant_cognition
✅ Scraped 159 paragraphs from Wikipedia

✅ Scraping complete!
📁 Saved 179 items to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/web_scraped_elephants.txt
📊 File size: 105.7 KB
Running augment_corpus.py...
✅ augment_corpus.py completed successfully
Output: 📖 Reading corpus from: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/elephant_human_90_10_corpus.txt
📝 Found 9574 sentences to augment
  🔄 Creating paraphrases...
  ❓ Generating Q&A pairs...
  🔗 Creating context variations...
✅ Augmentation complete!
📁 Generated 3018 augmented items
📊 Output size: 747.7 KB

🎉 Data augmentation complete!
Input: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/elephant_human_90_10_corpus.txt
Output: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/augmented_corpus.txt
Generated: 3018 augmented items

=== Step 4: Combine all available data sources ===
📄 Found base corpus: elephant_human_90_10_corpus.txt
📄 Found additional data: synthetic_generated.txt
📄 Found additional data in raw/: web_scraped_elephants.txt
📄 Found additional data in raw/: augmented_corpus.txt
📄 Found additional data in raw/: synthetic_advanced.txt
📊 Combining 5 data sources:
  1. elephant_human_90_10_corpus.txt (9,142 lines, 1.0MB)
  2. synthetic_generated.txt (20,000 lines, 2.2MB)
  3. web_scraped_elephants.txt (358 lines, 0.1MB)
  4. augmented_corpus.txt (9,875 lines, 0.7MB)
  5. synthetic_advanced.txt (2,333 lines, 0.1MB)
📖 Processing elephant_human_90_10_corpus.txt...
   Added 9,142 lines
📖 Processing synthetic_generated.txt...
   Added 20,000 lines
📖 Processing web_scraped_elephants.txt...
   Added 179 lines
📖 Processing augmented_corpus.txt...
   Added 6,668 lines
📖 Processing synthetic_advanced.txt...
   Added 1,733 lines
✅ Combined corpus written: 37,722 total lines

=== Step 5: Dedupe and filter combined corpus ===
📊 Deduplication results:
   Original lines: 37,722
   Unique lines: 14,405
   Final filtered: 13,554
   Reduction: 64.1%

=== Step 6: Split corpus ===
📊 Split statistics:
   train: 10,844 lines
   val: 1,355 lines
   test: 1,355 lines

=== Step 7: Final corpus statistics ===
train.txt: lines 10844, chars 1282900, words 208115
val.txt: lines 1355, chars 163283, words 26309
test.txt: lines 1355, chars 155371, words 25217
train.txt: {'lines': 10844, 'chars': 1282900, 'words': 208115}
val.txt: {'lines': 1355, 'chars': 163283, 'words': 26309}
test.txt: {'lines': 1355, 'chars': 155371, 'words': 25217}

=== Step 8: Cleanup intermediate files ===
🗑️  Deleted: corpus_all_sources_combined.txt
🗑️  Deleted: synthetic_generated.txt
🗑️  Deleted: elephant_human_90_10_corpus.txt

🎉 Enhanced pipeline completed successfully!
📁 Final files available in: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out
📊 Key outputs:
   train.txt: 10,844 lines (1.2MB)
   val.txt: 1,355 lines (0.2MB)
   test.txt: 1,355 lines (0.2MB)
```

## Tokenization training
```
$ train-tokenizer --config 4_elephant_twicedata/config.json --tokenizer-type byte_bpe --vocab-size 6144
[INFO] Project config loaded from: /home/pooja-saxena/PoojaVault/Professional/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/4_elephant_twicedata/config.json
[OK] Trained tokenizer
     Saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/tokenizers/bpe-elephant/v4/tokenizer.json
     Type: byte_bpe, Vocab size: 6144
```

## Train Model
```
2025-12-18 10:11:31,325 | INFO | llmlib.cli.modern_gpt_train_cli | [modern-gpt-train] Using device: cpu
2025-12-18 10:11:31,325 | INFO | llmlib.cli.modern_gpt_train_cli | [modern-gpt-train] Using data file: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/train.txt
2025-12-18 10:11:31,355 | INFO | llmlib.cli.modern_gpt_train_cli | [modern-gpt-train] Tokenizer vocab size: 6144
PAD: 0
BOS: 2
EOS: 3

============================================================
🚀 modern-gpt-train
============================================================
Model Name       : gpt-bpe-v4
Vocabulary Size  : 6144
d_model          : 256
n_heads          : 8
n_layers         : 6
dropout          : 0.15
max_seq_length   : 256
batch_size       : 4
learning_rate    : 0.0002
train_steps      : 18000
============================================================

Step 0, Train Loss: 8.8398, Val Loss: 7.9104
Step 1, Train Loss: 8.0866, Val Loss: 7.4456
Step 2, Train Loss: 7.5197, Val Loss: 7.2011
Step 3, Train Loss: 7.2668, Val Loss: 7.0094
Step 4, Train Loss: 6.8149, Val Loss: 6.8692
Step 5, Train Loss: 6.9277, Val Loss: 6.7721
Step 6, Train Loss: 6.8303, Val Loss: 6.6983
Step 7, Train Loss: 6.6118, Val Loss: 6.6384
...
...
Step 16800, Train Loss: 1.1643, Val Loss: 1.7561
Step 17000, Train Loss: 1.5488, Val Loss: 1.7880
Step 17200, Train Loss: 0.7796, Val Loss: 1.7157
Step 17400, Train Loss: 1.6142, Val Loss: 1.7343
Step 17600, Train Loss: 0.8395, Val Loss: 1.7142
Step 17800, Train Loss: 1.3213, Val Loss: 1.7316

[modern-gpt-train] Model saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v4/model.pt
[modern-gpt-train] Tokenizer saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v4/tokenizer.json

```

## Inference
```
 $ modern-gpt-infer  --config 4_elephant_twicedata/config.json
2025-12-18 12:48:48,715 | INFO | llmlib.cli.modern_gpt_infer_cli | [modern-gpt-infer] Using device: cpu

============================================================
🧠 Modern GPT Inference
============================================================
Project config     : ~/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/4_elephant_twicedata/config.json
Model directory    : ~/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v4
Checkpoint         : ~/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v4/model.pt
Model config       : ~/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v4/model_config.json
Tokenizer type     : ByteBPETokenizer
Vocab size         : 6144
Special tokens     : ['<pad>', '<unk>', '<bos>', '<eos>']
Device             : cpu
Max sequence len   : 256
Max new tokens     : 150
============================================================

🤖 Interactive ModernGPT Inference
Type your prompts below. Type 'quit', 'exit', or press Ctrl+C to stop.

Enter a prompt: hello
---
Prompt : hello
Output : helloHuman How's your day going?

Enter a prompt: I am good, how are you?
---
Prompt : I am good, how are you?
Output : I am good, how are you? Trying on the holidays.

Enter a prompt: tell me something about Elephant
---
Prompt : tell me something about Elephant
Output : tell me something about Elephant meat.

Enter a prompt: Elephants are 
---
Prompt : Elephants are
Output : Elephants are capable of surprisingly fast speeds—up to around 25 km/h—though their gait never involves true running; at maximum speed, they maintain at least one foot on the ground additionally, foot health is critical, especially for captive elephants; improper flooring or uneven terrain can lead to abscesses and arthritis

Enter a prompt: asian elephants
---
Prompt : asian elephants
Output : asian elephants and both african elephant species are endangered Additionally, elephants also interact with gentle trunk touches

Enter a prompt: Tell me a funny joke about eLephant
---
Prompt : Tell me a funny joke about eLephant
Output : Tell me a funny joke about eLephant and mud sagicly

Enter a prompt: funny thing about elehants
---
Prompt : funny thing about elehants
Output : funny thing about elehants patterns by crapile, rising, but require moist habitats to have areas had diger.

Enter a prompt: what is tusk
---
Prompt : what is tusk
Output : what is tusk care about?

```