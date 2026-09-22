## 🎯 Overall Assessment:
1. The inferecne keep repeating some standard lines, figured out it was the leakage from `advanced_synth_expand.py`, it keep generating those lines `Elephants have excellent memories and can remember other elephants for decades.`.
2. Next Project will modify this file and will be trained with more extended data.


## Updates performed compared to earlier project
1. This project removed the bias between validation and train data. 
2. Seperate sanity_check for validation data vs train data is being added, also in llmlib-piepline, so it runs every time pipeline runs.
3. The training data is heavily cleaned for this project, the data used for this training is following:
   ```
   20K	./human
   708K	./elephant
   ```
4. I plan to add more data and have another new project run on extended data to be able to compare the performance.


## How to run pipeline
```
# Validate first (Dry Run)
llmlib train-pipeline --config config.json --dry-run

# TMux Dry Run
llmlib tmux start --config config.json --dry-run

# Unified CLI Dry Run
llmlib train-pipeline --config config.json --dry-run  # Same as #1

# Step 1: Quick validation (interactive, immediate feedback)
llmlib train-pipeline --config config.json --dry-run

# Step 2: If validation passes, start long training in tmux
llmlib tmux start --config config.json --auto-confirm

# Monitor progress (separate terminal)
llmlib tmux monitor

# Attach when needed
llmlib tmux attach session-name
```

### Detailed Steps


1. Start Data Pipeline
```
llmlib-run-data-pipeline --config config_8.json 
🔧 Prefix-cap config: words=12, max=3
🐘 Enhanced Elephant LLM Data Pipeline Starting...
📁 Data directory: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out

=== Pre-step: Cleanup out/ directory ===
🗑️  Deleted: corpus_final_dedup.txt
🗑️  Deleted: test.txt
🗑️  Deleted: web_scraped_elephants.txt
🗑️  Deleted: corpus_all_sources_combined.txt
🗑️  Deleted: synthetic_generated.txt
🗑️  Deleted: train.txt
🗑️  Deleted: val.txt
🗑️  Deleted: elephant_human_90_10_corpus.txt

=== Pre-step: Cleanup old generated files ===
   No generated files to remove

=== Pre-step: Cleanup generated files in raw/ ===
🗑️  Deleted: augmented_corpus.txt
🗑️  Deleted: synthetic_advanced.txt

=== Step 1: Prepare raw corpus ===
Raw input directory: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw
Raw base directories:
  - /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant
  - /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/human
Found raw files: 173
  1. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/bush_evolution_and_anatomy_001.txt
  2. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/bush_evolution_and_anatomy_002.txt
  3. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/bush_evolution_and_anatomy_003.txt
  4. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/bush_evolution_and_anatomy_004.txt
  5. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/bush_overview_001.txt
  6. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/bush_social_and_communication_001.txt
  7. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/climate_impacts_002.txt
  8. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/climate_impacts_003.txt
  9. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/climate_variability_001.txt
  10. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/cognition_tools_problem_solving_001.txt
  11. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/cognition_tools_problem_solving_002.txt
  12. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/conservation_cites_and_trade_001.txt
  13. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/conservation_conflict_dynamics_001.txt
  14. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/conservation_corridors_connectivity_001.txt
  15. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/conservation_economics_001.txt
  16. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/conservation_landscape_planning_001.txt
  17. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/conservation_monitoring_001.txt
  18. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/conservation_policy_001.txt
  19. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/conservation_policy_002.txt
  20. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/conservation_tradeoffs_001.txt
  ... and 153 more
Wrote /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/elephant_human_90_10_corpus.txt | lines: 132, chars: 135936
Removed by clean_doc(): 41 | empty chunks: 0

=== Step 2: Generate basic synthetic expansions ===
Wrote 251 synthetic lines to /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/synthetic_generated.txt

=== Step 3: Advanced data generation ===
Running advanced_synth_expand.py...
✅ advanced_synth_expand.py completed successfully
Output: ✅ Wrote 690 synthetic lines to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/synthetic_advanced.txt
Running web_scrape_elephants.py...
✅ web_scrape_elephants.py completed successfully
Output: 📡 Fetching Wikipedia extract: Elephant
   ✅ got 516 clean lines from 'Elephant'
📡 Fetching Wikipedia extract: African elephant
   ✅ got 187 clean lines from 'African elephant'
📡 Fetching Wikipedia extract: Asian elephant
   ✅ got 288 clean lines from 'Asian elephant'

✅ Scraping complete!
📁 Saved 997 lines to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/web_scraped_elephants.txt
📊 File size: 109.6 KB
Running augment_corpus.py...
✅ augment_corpus.py completed successfully
Output: 📖 Reading corpus from: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/elephant_human_90_10_corpus.txt
📝 Found 1236 sentences to augment
  🔄 Creating paraphrases...
  🧩 Creating declarative helper lines...
  🔗 Creating context variations...
✅ Augmentation complete!
📁 Generated 1110 augmented lines
📊 Output size: 197.3 KB

🎉 Data augmentation complete!
Input:  /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/elephant_human_90_10_corpus.txt
Output: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/augmented_corpus.txt
Lines:  1110

=== Step 4: Combine all available data sources ===
📄 Found base corpus: elephant_human_90_10_corpus.txt
📄 Found additional data: synthetic_generated.txt
📄 Found additional data: web_scraped_elephants.txt
📄 Found additional data in raw/: augmented_corpus.txt
📄 Found additional data in raw/: synthetic_advanced.txt
📊 Combining 5 data sources:
  1. elephant_human_90_10_corpus.txt (132 lines, 0.1MB)
  2. synthetic_generated.txt (251 lines, 0.3MB)
  3. web_scraped_elephants.txt (997 lines, 0.1MB)
  4. augmented_corpus.txt (1,110 lines, 0.2MB)
  5. synthetic_advanced.txt (690 lines, 0.1MB)
📖 Processing elephant_human_90_10_corpus.txt...
   Added 132 lines
📖 Processing synthetic_generated.txt...
   Added 251 lines
📖 Processing web_scraped_elephants.txt...
   Added 997 lines
📖 Processing augmented_corpus.txt...
   Added 1,110 lines
📖 Processing synthetic_advanced.txt...
   Added 690 lines
✅ Combined corpus written: 3,180 total lines

=== Step 5: Dedupe and filter combined corpus ===
🔧 Token-cap uses tokenizer encode()
[clean] removed: 191/3,180 (6.01%)
[clean] kept:   2,989/3,180
[clean] DROP REASONS: [('too_many_tokens', 108), ('short_question', 72), ('stitched_roles', 11)]
[dedupe] removed: 388 | unique: 2,601
[prefix-cap] cap=3 words=12 dropped: 12 kept: 2589
[ngram-cap] n=3 cap=30 dropped: 185 kept: 2404
📊 Deduplication results:
   Original lines: 3,180
   Unique lines: 2,404
   Final filtered: 2,404
   Reduction: 24.4%

=== Step 6: Split corpus ===
📊 Split statistics:
   train: 1,924 lines
   val: 240 lines
   test: 240 lines

=== Step 7: Final corpus statistics ===
train.txt: lines 1924, chars 361098, words 53740
val.txt: lines 240, chars 42407, words 6306
test.txt: lines 240, chars 40933, words 6236
train.txt: {'lines': 1924, 'chars': 361098, 'words': 53740}
val.txt: {'lines': 240, 'chars': 42407, 'words': 6306}
test.txt: {'lines': 240, 'chars': 40933, 'words': 6236}

=== Step 8: Cleanup skipped (use --cleanup to enable) ===

🎉 Enhanced pipeline completed successfully!
📁 Final files available in: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out
📊 Key outputs:
   train.txt: 1,924 lines (0.3MB)
   val.txt: 240 lines (0.0MB)
   test.txt: 240 lines (0.0MB)
 ~/Poo/Pr/L/N/Transfomers_Foundation/course4/p/8_improved_batchstream  main !10 ?9  llmlib-data-checks --config config_8.json --health-check 

============================================================
🔬 DATA SANITY CHECKS
============================================================

🔍 Checking train/validation overlap...
📊 Train lines: 1924 (unique: 1924)
📊 Val lines: 240 (unique: 240)
⚠️  Exact overlap unique lines: 0
📈 Overlap % of validation (unique): 0.00%
✅ No overlap detected - good data separation!

📏 Token length analysis for TRAIN...
📊 TRAIN: lines=1924
📊 TRAIN: token_len mean=67.9, median=54.0, p90=110.0, p99=367.0, max=506

📏 Token length analysis for VAL...
📊 VAL: lines=240
📊 VAL: token_len mean=64.5, median=53.0, p90=101.2, p99=268.2, max=413

📐 Sequence length configuration: max_seq_length = 512
✂️  Training sequences that will be truncated: 0/1924 (0.0%)
✂️  Validation sequences that will be truncated: 0/240 (0.0%)
============================================================
✅ Data sanity checks completed!
============================================================


FILE SUMMARY
------------
file       lines_total  lines_nonempty  empty%  chars_mean  words_mean  words_median  short%(<3)  exact_dup%  norm_dup%
---------  -----------  --------------  ------  ----------  ----------  ------------  ----------  ----------  ---------
train.txt  1924         1924            0.00%   187.7       28.4        23.0          0.16%       0.00%       0.00%    
val.txt    240          240             0.00%   176.7       26.7        22.5          0.00%       0.00%       0.00%    

TRAIN: TOP PREFIXES (first 6 words)
-----------------------------------
prefix                                                        count  pct  
------------------------------------------------------------  -----  -----
elephant intelligence continues to interest researchers       9      0.47%
elephant herds are often led by                               8      0.42%
in the african savanna, elephants roam                        7      0.36%
in forest ecosystems, elephants act as                        5      0.26%
conservation efforts for elephants face complex               5      0.26%
asian elephants inhabit dense forests and                     5      0.26%
elephants greet each other by flapping                        3      0.16%
efforts to reduce elephant mortality often                    3      0.16%
an elephant molar weighs as much                              3      0.16%
observations across multiple populations suggest that         3      0.16%
elephants’ trunks are simultaneously vacuum cleaners,         3      0.16%
adult savanna elephants often weigh between                   3      0.16%
elephants are generalist herbivores capable of                3      0.16%
weather strongly shapes elephant behavior. during             3      0.16%
future challenges for elephant conservation lie               3      0.16%
demographic imbalance can alter social dynamics.              3      0.16%
elephants treat mud like a spa                                3      0.16%
during the winter, elephants primarily eat                    3      0.16%
elephants are one of the few                                  3      0.16%
monitoring elephant populations requires balancing precision  3      0.16%
elephant health is influenced by nutrition,                   3      0.16%
technological advances have reshaped elephant research        3      0.16%
seasonal changes alter how elephants interact                 3      0.16%
human–elephant conflict often emerges gradually rather        3      0.16%
their movements often follow seasonal patterns,               3      0.16%
adult african elephants often weigh between                   3      0.16%
movement patterns in elephants reflect a                      3      0.16%
elephant populations depend on large, connected               3      0.16%
elephant diet. poaching for ivory remains                     3      0.16%
research on elephants increasingly considers ethical          3      0.16%

TRAIN: TEMPLATE PREFIX HITS (chat/Q/A scaffolding)
--------------------------------------------------
prefix  count  pct
------  -----  ---

TRAIN: template-scaffold lines overall: 0.00%

TRAIN: DISCOURSE MARKERS (anywhere / at start)
----------------------------------------------
marker       count_any  count_start  pct_lines_any
-----------  ---------  -----------  -------------
however      22         0            1.14%        
therefore    12         0            0.62%        
for example  2          0            0.10%        

TRAIN: NOISE SIGNATURES
-----------------------
signature           count  pct_lines
------------------  -----  ---------
bracket_cite_lines  0      0.00%    
url_lines           0      0.00%    
redacted_lines      0      0.00%    
bulletish_lines     0      0.00%    

TRAIN: TOP BIGRAMS (word-level)
-------------------------------
bigram                count  pct_of_all_bigrams
--------------------  -----  ------------------
of the                201    0.381%            
elephants are         197    0.374%            
in the                152    0.288%            
asian elephants       132    0.250%            
rather than           112    0.212%            
elephants have        100    0.190%            
african elephants     100    0.190%            
an elephant           91     0.173%            
long term             86     0.163%            
as a                  78     0.148%            
elephants can         66     0.125%            
elephant populations  57     0.108%            
the african           57     0.108%            
the trunk             56     0.106%            
they are              55     0.104%            
in some               55     0.104%            
by the                53     0.101%            
elephant s            53     0.101%            
and the               52     0.099%            
to the                52     0.099%            
elephants were        48     0.091%            
from the              47     0.089%            
and can               47     0.089%            
with the              47     0.089%            
can be                46     0.087%            
role in               46     0.087%            
their trunks          45     0.085%            
asian elephant        45     0.085%            
forest elephants      45     0.085%            
of elephants          44     0.083%            

TRAIN: TOP TRIGRAMS (word-level)
--------------------------------
trigram                   count  pct_of_all_trigrams
------------------------  -----  -------------------
an elephant s             38     0.075%             
africa and asia           33     0.065%             
the asian elephant        31     0.061%             
other large mammals       26     0.051%             
elephants have excellent  26     0.051%             
have excellent memories   26     0.051%             
excellent memories and    26     0.051%             
memories and can          26     0.051%             
and can remember          26     0.051%             
can remember other        26     0.051%             
remember other elephants  26     0.051%             
other elephants for       26     0.051%             
elephants for decades     26     0.051%             
in the wild               26     0.051%             
in africa and             25     0.049%             
african forest elephant   24     0.047%             
asian elephants have      24     0.047%             
a crucial role            24     0.047%             
crucial role in           24     0.047%             
poaching for ivory        24     0.047%             
found in africa           24     0.047%             
to elephant populations   23     0.045%             
african elephants are     23     0.045%             
researchers study this    23     0.045%             
study this using          23     0.045%             
this using long           23     0.045%             
using long term           23     0.045%             
long term field           23     0.045%             
term field observation    23     0.045%             
field observation and     23     0.045%             

VAL: TOP PREFIXES (first 6 words)
---------------------------------
prefix                                                            count  pct  
----------------------------------------------------------------  -----  -----
elephants are intelligent animals with strong                     2      0.83%
asian elephants live across a wide                                2      0.83%
elephants are often described as majestic,                        2      0.83%
feeding choices vary with resource availability.                  2      0.83%
instead of replacing individual teeth, elephants                  1      0.42%
it is reported that war elephants                                 1      0.42%
the convention on the conservation of                             1      0.42%
asian elephants were always more common                           1      0.42%
traditional reserve boundaries rarely align with                  1      0.42%
these traces aligned closely with older                           1      0.42%
researchers note that a group of                                  1      0.42%
population structure in elephants reflects historical             1      0.42%
compared with african elephants, asian elephants                  1      0.42%
researchers note that movement resumed only                       1      0.42%
these traits underscore the evolutionary convergence              1      0.42%
a well-coated elephant looks like it’s                            1      0.42%
elephants are not just inhabitants of                             1      0.42%
eia (in the usa) reports etc                                      1      0.42%
sleeping occurs at night while the                                1      0.42%
forest elephants typically live 60–70 years                       1      0.42%
bibcode:2004ecoec..48...93b. doi:10.1016/j.ecolecon.2003.01.001.  1      0.42%
war elephants were also employed in                               1      0.42%
in 1989, the convention on international                          1      0.42%
national elephant day (thailand)                                  1      0.42%
instead, they combine memory, body control,                       1      0.42%
because elephants require vast areas of                           1      0.42%
the demand for elephant skin has                                  1      0.42%
these animals do not reproduce well                               1      0.42%
researchers note that this mechanism is                           1      0.42%
in some african folklore, elephants are                           1      0.42%

VAL: TEMPLATE PREFIX HITS (chat/Q/A scaffolding)
------------------------------------------------
prefix  count  pct
------  -----  ---

VAL: template-scaffold lines overall: 0.00%

VAL: DISCOURSE MARKERS (anywhere / at start)
--------------------------------------------
marker   count_any  count_start  pct_lines_any
-------  ---------  -----------  -------------
however  1          0            0.42%        

VAL: NOISE SIGNATURES
---------------------
signature           count  pct_lines
------------------  -----  ---------
bracket_cite_lines  0      0.00%    
url_lines           0      0.00%    
redacted_lines      0      0.00%    
bulletish_lines     0      0.00%    

VAL: TOP BIGRAMS (word-level)
-----------------------------
bigram                count  pct_of_all_bigrams
--------------------  -----  ------------------
elephants are         24     0.389%            
in the                23     0.373%            
asian elephants       23     0.373%            
rather than           22     0.356%            
of the                22     0.356%            
african elephants     12     0.194%            
elephants have        12     0.194%            
with the              11     0.178%            
long term             11     0.178%            
in some               11     0.178%            
over time             9      0.146%            
the wild              9      0.146%            
elephant populations  9      0.146%            
to the                9      0.146%            
can vary              8      0.130%            
african and           8      0.130%            
and asian             8      0.130%            
as a                  8      0.130%            
the herd              7      0.113%            
through the           7      0.113%            
the trunk             7      0.113%            
the details           7      0.113%            
details can           7      0.113%            
vary across           7      0.113%            
across regions        7      0.113%            
regions and           7      0.113%            
and between           7      0.113%            
between african       7      0.113%            
elephants can         7      0.113%            
role in               7      0.113%            

VAL: TOP TRIGRAMS (word-level)
------------------------------
trigram                count  pct_of_all_trigrams
---------------------  -----  -------------------
in the wild            8      0.135%             
african and asian      8      0.135%             
and asian elephants    8      0.135%             
the details can        7      0.118%             
details can vary       7      0.118%             
can vary across        7      0.118%             
vary across regions    7      0.118%             
across regions and     7      0.118%             
regions and between    7      0.118%             
and between african    7      0.118%             
between african and    7      0.118%             
60 70 years            6      0.101%             
70 years in            6      0.101%             
years in the           6      0.101%             
live 60 70             5      0.084%             
play a crucial         5      0.084%             
a crucial role         5      0.084%             
crucial role in        5      0.084%             
the asian elephant     5      0.084%             
researchers note that  4      0.067%             
asian elephants are    4      0.067%             
poaching for ivory     4      0.067%             
elephants play a       4      0.067%             
role in their          4      0.067%             
in their ecosystem     4      0.067%             
their ecosystem as     4      0.067%             
ecosystem as a         4      0.067%             
as a keystone          4      0.067%             
a keystone species     4      0.067%             
in ways that           4      0.067%             

VAL∩TRAIN overlap (normalized exact): 0/240 = 0.00%

RED FLAGS (rule-of-thumb)
------------------------
- normalized duplicates > ~2–5% is worth fixing (your report shows norm_dup%)
- short lines > ~30% (below 3 words) usually hurts generation coherence
- any single prefix > ~1% means strong template dominance (promotes loops)
- lots of chat prefixes (Human:, Q:, A:) means your 'cleaned of Q/A templates' is still leaking
✅ Data sanity checks completed!
```
2. Training Pipeline

```
llmlib-train-pipeline --config config_8.json
✅ Config loaded: .../course4_domain_expert_gpt/projects/8_improved_batchstream/config_8.json
00:24 | I | 🤖 Starting Robust LLM Training Pipeline
00:24 | I | 📅 Started at: 2026-01-28 14:00:24
00:24 | I | 🖥️  Host: pooja-saxena-ThinkPad-L13-Yoga-Gen-4
00:24 | I | 💾 Available space: 88.0 GB
00:24 | I | 🔧 GLOBAL_DATASETS_DIR: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets
00:24 | I | 🔧 GLOBAL_MODELS_DIR: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models
00:24 | W | ⚠️  nvidia-smi not available
🔍 === DRY RUN: Validating all paths and dependencies ===
✅ Config file: .../course4_domain_expert_gpt/projects/8_improved_batchstream/config_8.json
✅ Tokenizer EXISTS: $WORKBENCH_ROOT/Models/llm/tokenizers/bpe-elephant/v4/tokenizer.json
📁 Model directory EXISTS: $WORKBENCH_ROOT/Models/llm/language_models/elephantdomain_gpt
✅ Training data EXISTS: $WORKBENCH_ROOT/Datasets/llm/mixed_text/out/train.txt (1,924 lines)
✅ Validation data EXISTS: $WORKBENCH_ROOT/Datasets/llm/mixed_text/out/val.txt (240 lines)
🆕 Fresh training (no resume_from specified)

🎯 Execution Plan:
   1️⃣ Skip tokenizer training (already exists)
   2️⃣ Train new model from scratch → $WORKBENCH_ROOT/Models/llm/language_models/elephantdomain_gpt
   3️⃣ Test inference with sample prompt

⏱️  Estimated time: 4-6 hours for model training
🔄 Max retries: 3
⏰ Timeout: 8 hours

🤔 Do you want to proceed with training? (y/n): y
00:41 | I | 🔒 Skipping system sleep prevention (skip-sudo flag or sudo requires password)
00:41 | I | 💡 You can manually prevent sleep with: sudo systemctl mask sleep.target
00:41 | I | 🚀 Starting training pipeline...
00:41 | I | ==================================================
00:41 | I | ✅ Tokenizer already exists, skipping training
00:41 | I | 🧠 Step 2: Starting robust model training...
00:41 | I | 💡 Training will auto-retry up to 3 times if it fails
00:41 | I | ⏱️  Max training time: 8 hours with timeout
00:41 | I | 🔄 Training attempt 1/3...

============================================================
🔬 DATA SANITY CHECKS
============================================================

🔍 Checking train/validation overlap...
📊 Train lines: 1924 (unique: 1924)
📊 Val lines: 240 (unique: 240)
⚠️  Exact overlap unique lines: 0
📈 Overlap % of validation (unique): 0.00%
✅ No overlap detected - good data separation!

📏 Token length analysis for TRAIN...
📊 TRAIN: lines=1924
📊 TRAIN: token_len mean=67.9, median=54.0, p90=110.0, p99=367.0, max=506

📏 Token length analysis for VAL...
📊 VAL: lines=240
📊 VAL: token_len mean=64.5, median=53.0, p90=101.2, p99=268.2, max=413

📐 Sequence length configuration: max_seq_length = 512
✂️  Training sequences that will be truncated: 0/1924 (0.0%)
✂️  Validation sequences that will be truncated: 0/240 (0.0%)
============================================================
✅ Data sanity checks completed!
============================================================

02:10 | I | [modern-gpt-train] Using device: cpu
02:10 | I | [modern-gpt-train] Using data file: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/train.txt
02:10 | I | [modern-gpt-train] Tokenizer vocab size: 6144
PAD: 0
BOS: 2
EOS: 3

============================================================
🚀 modern-gpt-train
============================================================
Model Name       : gpt-bpe-v8
Vocabulary Size  : 6144
d_model          : 384
n_heads          : 12
n_layers         : 12
dropout          : 0.15
max_seq_length   : 512
batch_size       : 8
learning_rate    : 0.0001
train_steps      : 2000
LR Scheduler     : {'type': 'cosine', 'min_lr': 1e-05, 'num_cycles': 0.5}
============================================================

03:27 | I | [modern-gpt-train] No resume_from specified - starting fresh training
[modern-gpt-train] Initial val=8.8440 (best_val=8.8440)
Steps/sec: 0.097
Step 200, LR: 1.00e-04, Train Loss: 3.8427, Val Loss: 4.1583
[modern-gpt-train] New best saved at step 200 (val=4.1583)
Steps/sec: 0.108
Step 400, LR: 9.73e-05, Train Loss: 3.5553, Val Loss: 3.7733
[modern-gpt-train] New best saved at step 400 (val=3.7733)
Steps/sec: 0.103
Step 600, LR: 8.95e-05, Train Loss: 3.1128, Val Loss: 3.4765
[modern-gpt-train] New best saved at step 600 (val=3.4765)
Steps/sec: 0.093
Step 800, LR: 7.75e-05, Train Loss: 2.8051, Val Loss: 3.1793
[modern-gpt-train] New best saved at step 800 (val=3.1793)
Steps/sec: 0.095
Step 1000, LR: 6.28e-05, Train Loss: 2.3751, Val Loss: 2.9307
[modern-gpt-train] New best saved at step 1000 (val=2.9307)
Steps/sec: 0.101
Step 1200, LR: 4.72e-05, Train Loss: 2.1588, Val Loss: 2.7772
[modern-gpt-train] New best saved at step 1200 (val=2.7772)
Steps/sec: 0.101
Step 1400, LR: 3.25e-05, Train Loss: 1.9978, Val Loss: 2.6814
[modern-gpt-train] New best saved at step 1400 (val=2.6814)
Steps/sec: 0.102
Step 1600, LR: 2.05e-05, Train Loss: 1.7861, Val Loss: 2.6108
[modern-gpt-train] New best saved at step 1600 (val=2.6108)
Steps/sec: 0.103
Step 1800, LR: 1.27e-05, Train Loss: 1.6832, Val Loss: 2.5605
[modern-gpt-train] New best saved at step 1800 (val=2.5605)
Steps/sec: 0.105
Step 2000, LR: 1.00e-05, Train Loss: 1.5680, Val Loss: 2.5426
[modern-gpt-train] New best saved at step 2000 (val=2.5426)
[modern-gpt-train] Training complete. Best val=2.5426 at step 2000.

[modern-gpt-train] Model saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v8/model.pt
[modern-gpt-train] Tokenizer saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v8/tokenizer.json
[modern-gpt-train] Updated config saved to: /home/pooja-saxena/PoojaVault/Professional/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/8_improved_batchstream/config_8.json
35:17 | I | ✅ Model training completed successfully!
```

3. Inference
```
lmlib infer --config config_8.json
54:59 | I | [modern-gpt-infer] Using device: cpu

============================================================
🧠 Modern GPT Inference
============================================================
Project config     : ~/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/8_improved_batchstream/config_8.json
Model directory    : ~/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v8
Checkpoint         : ~/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v8/model.pt
Model config       : ~/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v8/model_config.json
Tokenizer type     : ByteBPETokenizer
Vocab size         : 6144
Special tokens     : ['<pad>', '<unk>', '<bos>', '<eos>']
Device             : cpu
Max sequence len   : 512
Max new tokens     : 120
============================================================

🤖 Interactive ModernGPT Inference
Type your prompts below. Type 'quit', 'exit', or press Ctrl+C to stop.

Enter a prompt: african elephants
---
Prompt : african elephants
Output :  are often led by an experienced matriarch. Elephants have excellent memories and can remember other elephants for decades. Elephants live in matriarchal societies led across the oldest female.

Enter a prompt: Tusks are
---
Prompt : Tusks are
Output :  typically led by the African bush elephant is the largest living on the wild.

Enter a prompt: Baby elephant
---
Prompt : Baby elephant
Output :  are called calves and weigh about 250 pounds at birth. Elephants have excellent memories and can remember other elephants for decades.

Enter a prompt: Sex
---
Prompt : Sex
Output : Elephant conservation are often led by an experienced matriarch. Elephants have excellent memories and can remember other elephants for decades. Elephants live in matriarchal societies led across other animals and forests.

Enter a prompt: 


```
