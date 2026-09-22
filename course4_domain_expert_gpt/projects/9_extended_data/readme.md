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
llmlib-run-data-pipeline --config config_9.json; 
DEBUG require_domain: False
🔧 Prefix-cap config: words=12, max=3
🔧 Template-cap config: words=10, max=3
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
Found raw files: 452
  1. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/anatomy/ANATOMY_0001.txt
  2. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/anatomy/ANATOMY_0002.txt
  3. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/anatomy/ANATOMY_0003.txt
  4. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/anatomy/ANATOMY_0004.txt
  5. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/anatomy/ANATOMY_0005.txt
  6. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/anatomy/ANATOMY_0006.txt
  7. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/anatomy/ANATOMY_0007.txt
  8. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/anatomy/ANATOMY_0008.txt
  9. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/anatomy/ANATOMY_0009.txt
  10. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/anatomy/ANATOMY_0010.txt
  11. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/anatomy/ANATOMY_0011.txt
  12. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/anatomy/ANATOMY_0012.txt
  13. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/basic_overview/elephant_basic_facts_distilled_001.txt
  14. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/basic_overview/elephant_basic_facts_distilled_002.txt
  15. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/basic_overview/elephant_basic_overview_synthesis_001.txt
  16. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/basic_overview/elephant_species_overview_001.txt
  17. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/climate_impact/climate_impacts_002.txt
  18. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/climate_impact/climate_impacts_003.txt
  19. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/climate_impact/climate_variability_001.txt
  20. /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/elephant/documents/communication/COMMUNICATION_0001.txt
  ... and 432 more
Wrote /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/elephant_human_90_10_corpus.txt | lines: 513, chars: 230354
Removed by clean_doc(): 45 | empty chunks: 0

=== Step 2: Generate basic synthetic expansions ===
Wrote 921 synthetic lines to /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/synthetic_generated.txt

=== Step 3: Advanced data generation ===
Running advanced_synth_expand.py...
✅ advanced_synth_expand.py completed successfully
Output: ✅ Wrote 433 synthetic lines to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/synthetic_advanced.txt
Running web_scrape_elephants.py...
✅ web_scrape_elephants.py completed successfully
Output: 📡 Fetching Wikipedia extract: Elephant
   ✅ got 516 clean lines from 'Elephant'

✅ Scraping complete!
📁 Saved 300 lines to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/web_scraped_elephants.txt
📊 File size: 31.1 KB
Running augment_corpus.py...
✅ augment_corpus.py completed successfully
Output: 📖 Reading corpus from: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/elephant_human_90_10_corpus.txt
📝 Found 2388 sentences to augment
  🔄 Creating paraphrases...
  🧩 Creating declarative helper lines...
  🔗 Creating context variations...
✅ Augmentation complete!
📁 Generated 951 augmented lines
📊 Output size: 149.7 KB

🎉 Data augmentation complete!
Input:  /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/elephant_human_90_10_corpus.txt
Output: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/raw/augmented_corpus.txt
Lines:  951

=== Step 4: Combine all available data sources ===
📄 Found base corpus: elephant_human_90_10_corpus.txt
📄 Found additional data: synthetic_generated.txt
📄 Found additional data: web_scraped_elephants.txt
📄 Found additional data in raw/: augmented_corpus.txt
📄 Found additional data in raw/: synthetic_advanced.txt
📊 Combining 5 data sources:
  1. elephant_human_90_10_corpus.txt (513 lines, 0.2MB)
  2. synthetic_generated.txt (921 lines, 0.4MB)
  3. web_scraped_elephants.txt (300 lines, 0.0MB)
  4. augmented_corpus.txt (951 lines, 0.1MB)
  5. synthetic_advanced.txt (433 lines, 0.0MB)
📖 Processing elephant_human_90_10_corpus.txt...
   Added 513 lines
📖 Processing synthetic_generated.txt...
   Added 921 lines
📖 Processing web_scraped_elephants.txt...
   Added 300 lines
📖 Processing augmented_corpus.txt...
   Added 951 lines
📖 Processing synthetic_advanced.txt...
   Added 433 lines
✅ Combined corpus written: 3,118 total lines

=== Step 5: Dedupe and filter combined corpus ===
🔧 Token-cap uses tokenizer encode()
[clean] removed: 440/3,118 (14.11%)
[clean] kept:   2,678/3,118
[clean] DROP REASONS: [('too_short', 401), ('short_question', 38), ('stitched_roles', 1)]
[dedupe] removed: 743 | unique: 1,935
[prefix-cap] cap=3 words=12 dropped: 3 kept: 1932
[template-cap] cap=3 words=10 dropped: 0 kept: 1932 empty_key: 0
[ngram-cap] n=3 cap=50 dropped: 93 kept: 1839
📊 Deduplication results:
   Original lines: 3,118
   Unique lines: 1,839
   Final filtered: 1,839
   Reduction: 41.0%

=== Step 6: Split corpus ===
📊 Split statistics:
   train: 1,473 lines
   val: 183 lines
   test: 183 lines

=== Step 7: Final corpus statistics ===
train.txt: lines 1473, chars 450210, words 64806
val.txt: lines 183, chars 57230, words 8227
test.txt: lines 183, chars 54471, words 7678
train.txt: {'lines': 1473, 'chars': 450210, 'words': 64806}
val.txt: {'lines': 183, 'chars': 57230, 'words': 8227}
test.txt: {'lines': 183, 'chars': 54471, 'words': 7678}

=== Step 8: Cleanup skipped (use --cleanup to enable) ===

🎉 Enhanced pipeline completed successfully!
📁 Final files available in: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out
📊 Key outputs:
   train.txt: 1,473 lines (0.4MB)
   val.txt: 183 lines (0.1MB)
   test.txt: 183 lines (0.1MB)
   
llmlib-data-checks --config config_9.json --health-check

============================================================
🔬 DATA SANITY CHECKS
============================================================

🔍 Checking train/validation overlap...
📊 Train lines: 1473 (unique: 1473)
📊 Val lines: 183 (unique: 183)
⚠️  Exact overlap unique lines: 0
📈 Overlap % of validation (unique): 0.00%
✅ No overlap detected - good data separation!

📏 Token length analysis for TRAIN...
📊 TRAIN: lines=1473
📊 TRAIN: token_len mean=110.5, median=81.0, p90=240.8, p99=418.0, max=459

📏 Token length analysis for VAL...
📊 VAL: lines=183
📊 VAL: token_len mean=113.4, median=82.0, p90=261.8, p99=429.0, max=469

📐 Sequence length configuration: max_seq_length = 512
✂️  Training sequences that will be truncated: 0/1473 (0.0%)
✂️  Validation sequences that will be truncated: 0/183 (0.0%)
============================================================
✅ Data sanity checks completed!
============================================================


FILE SUMMARY
------------
file       lines_total  lines_nonempty  empty%  chars_mean  words_mean  words_median  short%(<3)  exact_dup%  norm_dup%
---------  -----------  --------------  ------  ----------  ----------  ------------  ----------  ----------  ---------
train.txt  1473         1473            0.00%   305.6       44.6        32.0          0.00%       0.00%       0.00%    
val.txt    183          183             0.00%   312.7       45.6        32.0          0.00%       0.00%       0.00%    

TRAIN: TOP PREFIXES (first 6 words)
-----------------------------------
prefix                                                           count  pct  
---------------------------------------------------------------  -----  -----
if the user asks about elephant                                  5      0.34%
elephant societies are structured around long-term               4      0.27%
during the wet season, elephants may                             4      0.27%
elephants greet each other by flapping                           4      0.27%
in forest mosaics, elephants may adjust                          4      0.27%
during the summer, elephants may shift                           4      0.27%
an elephant’s size can give the                                  4      0.27%
if the user asks for a                                           4      0.27%
an elephant’s daily behavior reflects constant                   3      0.20%
disease dynamics are gaining attention in                        3      0.20%
if the user asks me to                                           3      0.20%
in protected areas, elephants may adjust                         3      0.20%
mitigation strategies aimed at reducing crop                     3      0.20%
gender roles affect how conflict is                              3      0.20%
some old stories claimed elephants were                          3      0.20%
do not “run” in the way                                          3      0.20%
in riverine habitats, elephants may adjust                       3      0.20%
local perceptions of elephants are shaped                        3      0.20%
in savanna landscapes, elephants may adjust                      3      0.20%
tusks are elongated incisors that grow                           3      0.20%
foot structure in elephants combines rigidity                    3      0.20%
problem-solving strategies differ among individuals, indicating  3      0.20%
elephants are large mammals that give                            3      0.20%
humans regularly express emotions in conversation,               3      0.20%
elephant tusks are enlarged incisor teeth                        3      0.20%
beyond thailand, concern for elephants has                       3      0.20%
elephant society is complex, stable, and                         3      0.20%
early studies of elephants focused heavily                       3      0.20%
tioning items to access food—suggesting a                        3      0.20%
when unsure, i can say “i’m                                      3      0.20%

TRAIN: TEMPLATE PREFIX HITS (chat/Q/A scaffolding)
--------------------------------------------------
prefix  count  pct
------  -----  ---

TRAIN: template-scaffold lines overall: 0.00%

TRAIN: DISCOURSE MARKERS (anywhere / at start)
----------------------------------------------
marker         count_any  count_start  pct_lines_any
-------------  ---------  -----------  -------------
therefore      42         0            2.85%        
for example    15         0            1.02%        
however        9          0            0.61%        
in conclusion  1          0            0.07%        

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
bigram           count  pct_of_all_bigrams
---------------  -----  ------------------
rather than      207    0.322%            
i should         189    0.294%            
of the           163    0.254%            
long term        118    0.184%            
elephants are    115    0.179%            
in the           93     0.145%            
the user         74     0.115%            
an elephant      73     0.114%            
depends on       70     0.109%            
in some          67     0.104%            
and social       67     0.104%            
asian elephants  65     0.101%            
as a             61     0.095%            
such as          58     0.090%            
over time        55     0.086%            
i can            53     0.082%            
and season       52     0.081%            
to be            52     0.081%            
of elephant      52     0.081%            
habitat and      51     0.079%            
if the           51     0.079%            
vary by          50     0.078%            
elephants have   49     0.076%            
and the          49     0.076%            
by habitat       48     0.075%            
elephants may    48     0.075%            
this can         47     0.073%            
elephants can    47     0.073%            
the trunk        47     0.073%            
in elephants     46     0.072%            

TRAIN: TOP TRIGRAMS (word-level)
--------------------------------
trigram                  count  pct_of_all_trigrams
-----------------------  -----  -------------------
habitat and season       51     0.081%             
vary by habitat          47     0.075%             
by habitat and           47     0.075%             
this can vary            45     0.072%             
can vary by              45     0.072%             
if the user              44     0.070%             
the user asks            41     0.065%             
on age and               37     0.059%             
depends on age           36     0.057%             
and local conditions     36     0.057%             
this depends on          34     0.054%             
age and local            34     0.054%             
an elephant s            28     0.045%             
in response to           26     0.041%             
tend to be               23     0.037%             
in some populations      23     0.037%             
as much as               23     0.037%             
user asks for            20     0.032%             
evidence indicates that  20     0.032%             
the african forest       19     0.030%             
i should not             19     0.030%             
i should avoid           19     0.030%             
african forest elephant  18     0.029%             
as well as               18     0.029%             
movement patterns in     17     0.027%             
over long distances      17     0.027%             
when the user            16     0.025%             
in some regions          16     0.025%             
i should keep            16     0.025%             
and asian elephants      16     0.025%             

VAL: TOP PREFIXES (first 6 words)
---------------------------------
prefix                                                      count  pct  
----------------------------------------------------------  -----  -----
not all elephants have tusks; some                          2      1.09%
cmmunity responses to elephants evolve with                 2      1.09%
age distribution within elephant populations reflects       1      0.55%
when asked about elephant-human conflict,: when             1      0.55%
a small model needs practice saying                         1      0.55%
aunts, sisters, and older siblings help                     1      0.55%
elephant communication relies heavily on signals            1      0.55%
professional recognition appears briefly. someone recalls   1      0.55%
social networks influence disease transmission patterns.    1      0.55%
acoustic monitoring provides insights into communication:   1      0.55%
learning a new programming language becomes                 1      0.55%
th, marked by elevated testosterone levels,                 1      0.55%
african bush elephants in particular have                   1      0.55%
the herd followed this route without                        1      0.55%
these calls help elephants coordinate movement,             1      0.55%
as agriculture, infrastructure, and urban areas             1      0.55%
public perception shapes conservation outcomes indirectly.  1      0.55%
forest responses unfold over long periods,                  1      0.55%
if the user’s request is: if                                1      0.55%
asian males can have tusks as                               1      0.55%
if the user provides an output                              1      0.55%
poaching pressure may reshape this, with                    1      0.55%
a workspace does not need to                                1      0.55%
elephants’ trunks are simultaneously — elephants’           1      0.55%
asian elephant calves enter the world                       1      0.55%
together, tusks and molars illustrate how                   1      0.55%
i can offer a brief general                                 1      0.55%
when the user asks “why,” i                                 1      0.55%
at mount elgon, elephants dig through                       1      0.55%
family units can merge temporarily into                     1      0.55%

VAL: TEMPLATE PREFIX HITS (chat/Q/A scaffolding)
------------------------------------------------
prefix  count  pct
------  -----  ---

VAL: template-scaffold lines overall: 0.00%

VAL: DISCOURSE MARKERS (anywhere / at start)
--------------------------------------------
marker       count_any  count_start  pct_lines_any
-----------  ---------  -----------  -------------
therefore    3          0            1.64%        
for example  2          0            1.09%        
however      1          0            0.55%        

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
bigram            count  pct_of_all_bigrams
----------------  -----  ------------------
i should          24     0.294%            
rather than       23     0.282%            
of the            17     0.208%            
elephants are     16     0.196%            
in the            15     0.184%            
the trunk         14     0.172%            
depends on        12     0.147%            
and social        12     0.147%            
asian elephants   10     0.123%            
the user          10     0.123%            
as a              9      0.110%            
long term         9      0.110%            
and the           8      0.098%            
is not            8      0.098%            
on the            8      0.098%            
elephants to      8      0.098%            
age and           8      0.098%            
and local         8      0.098%            
elephants have    8      0.098%            
social structure  7      0.086%            
it is             7      0.086%            
over long         7      0.086%            
if the            7      0.086%            
with the          7      0.086%            
over time         7      0.086%            
this depends      7      0.086%            
on age            7      0.086%            
local conditions  7      0.086%            
elephant s        7      0.086%            
of their          7      0.086%            

VAL: TOP TRIGRAMS (word-level)
------------------------------
trigram                          count  pct_of_all_trigrams
-------------------------------  -----  -------------------
this depends on                  7      0.088%             
depends on age                   7      0.088%             
on age and                       7      0.088%             
age and local                    7      0.088%             
and local conditions             7      0.088%             
i should avoid                   6      0.075%             
if the user                      6      0.075%             
the trunk is                     5      0.063%             
food and water                   4      0.050%             
in response to                   4      0.050%             
world elephant day               4      0.050%             
not all elephants                4      0.050%             
low frequency calls              3      0.038%             
the user s                       3      0.038%             
trunk is not                     3      0.038%             
the user asks                    3      0.038%             
elephants to move                3      0.038%             
the expansion of                 3      0.038%             
expansion of cross               3      0.038%             
of cross border                  3      0.038%             
cross border conservation        3      0.038%             
border conservation initiatives  3      0.038%             
asian elephants are              3      0.038%             
human elephant conflict          3      0.038%             
features of the                  3      0.038%             
the elephant s                   3      0.038%             
elephants visit these            3      0.038%             
visit these sites                3      0.038%             
these sites to                   3      0.038%             
sites to supplement              3      0.038%             

VAL∩TRAIN overlap (normalized exact): 0/183 = 0.00%

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
llmlib train-pipeline --config config_9.json
✅ Config loaded: .../course4_domain_expert_gpt/projects/9_extended_data/config_9.json
01:56 | I | 🤖 Starting Robust LLM Training Pipeline
01:56 | I | 📅 Started at: 2026-02-03 11:01:56
01:56 | I | 🖥️  Host: pooja-saxena-ThinkPad-L13-Yoga-Gen-4
01:56 | I | 💾 Available space: 85.0 GB
01:56 | I | 🔧 GLOBAL_DATASETS_DIR: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets
01:56 | I | 🔧 GLOBAL_MODELS_DIR: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models
01:56 | W | ⚠️  nvidia-smi not available
🔍 === DRY RUN: Validating all paths and dependencies ===
✅ Config file: .../course4_domain_expert_gpt/projects/9_extended_data/config_9.json
✅ Tokenizer EXISTS: $WORKBENCH_ROOT/Models/llm/tokenizers/bpe-elephant/v4/tokenizer.json
📁 Model directory EXISTS: $WORKBENCH_ROOT/Models/llm/language_models/elephantdomain_gpt
✅ Training data EXISTS: $WORKBENCH_ROOT/Datasets/llm/mixed_text/out/train.txt (1,473 lines)
✅ Validation data EXISTS: $WORKBENCH_ROOT/Datasets/llm/mixed_text/out/val.txt (183 lines)
🆕 Fresh training (no resume_from specified)

🎯 Execution Plan:
   1️⃣ Skip tokenizer training (already exists)
   2️⃣ Train new model from scratch → $WORKBENCH_ROOT/Models/llm/language_models/elephantdomain_gpt
   3️⃣ Test inference with sample prompt

⏱️  Estimated time: 4-6 hours for model training
🔄 Max retries: 3
⏰ Timeout: 8 hours

🤔 Do you want to proceed with training? (y/n): y
02:11 | I | 🔒 Skipping system sleep prevention (skip-sudo flag or sudo requires password)
02:11 | I | 💡 You can manually prevent sleep with: sudo systemctl mask sleep.target
02:11 | I | 🚀 Starting training pipeline...
02:11 | I | ==================================================
02:11 | I | ✅ Tokenizer already exists, skipping training
02:11 | I | 🧠 Step 2: Starting robust model training...
02:11 | I | 💡 Training will auto-retry up to 3 times if it fails
02:11 | I | ⏱️  Max training time: 8 hours with timeout
02:11 | I | 🔄 Training attempt 1/3...

============================================================
🔬 DATA SANITY CHECKS
============================================================

🔍 Checking train/validation overlap...
📊 Train lines: 1473 (unique: 1473)
📊 Val lines: 183 (unique: 183)
⚠️  Exact overlap unique lines: 0
📈 Overlap % of validation (unique): 0.00%
✅ No overlap detected - good data separation!

📏 Token length analysis for TRAIN...
📊 TRAIN: lines=1473
📊 TRAIN: token_len mean=110.5, median=81.0, p90=240.8, p99=418.0, max=459

📏 Token length analysis for VAL...
📊 VAL: lines=183
📊 VAL: token_len mean=113.4, median=82.0, p90=261.8, p99=429.0, max=469

📐 Sequence length configuration: max_seq_length = 512
✂️  Training sequences that will be truncated: 0/1473 (0.0%)
✂️  Validation sequences that will be truncated: 0/183 (0.0%)
============================================================
✅ Data sanity checks completed!
============================================================

04:14 | I | [modern-gpt-train] Using device: cpu
04:14 | I | [modern-gpt-train] Using data file: /home/pooja-saxena/PoojaVault/Professional/Workbench/Datasets/llm/mixed_text/out/train.txt
04:14 | I | [modern-gpt-train] Tokenizer vocab size: 6144
PAD: 0
BOS: 2
EOS: 3

============================================================
🚀 modern-gpt-train
============================================================
Model Name       : gpt-bpe-v9
Vocabulary Size  : 6144
d_model          : 384
n_heads          : 12
n_layers         : 12
dropout          : 0.15
max_seq_length   : 512
batch_size       : 8
learning_rate    : 0.0008
train_steps      : 900
LR Scheduler     : {'type': 'cosine', 'min_lr': 1e-05, 'num_cycles': 0.5}
============================================================

06:26 | I | [modern-gpt-train] No resume_from specified - starting fresh training
[modern-gpt-train] Initial val=8.7480 (best_val=8.7480)
Steps/sec: 0.092
Step 100, LR: 7.99e-04, Train Loss: 4.0362, Val Loss: 4.1769
[modern-gpt-train] New best saved at step 100 (val=4.1769)
Steps/sec: 0.102
Step 200, LR: 7.59e-04, Train Loss: 3.6574, Val Loss: 3.7988
[modern-gpt-train] New best saved at step 200 (val=3.7988)
Steps/sec: 0.100
Step 300, LR: 6.68e-04, Train Loss: 3.1335, Val Loss: 3.5088
[modern-gpt-train] New best saved at step 300 (val=3.5088)
Steps/sec: 0.102
Step 400, LR: 5.39e-04, Train Loss: 2.5691, Val Loss: 3.1228
[modern-gpt-train] New best saved at step 400 (val=3.1228)
Steps/sec: 0.102
Step 500, LR: 3.90e-04, Train Loss: 2.0983, Val Loss: 2.7157
[modern-gpt-train] New best saved at step 500 (val=2.7157)
Steps/sec: 0.102
Step 600, LR: 2.43e-04, Train Loss: 1.5509, Val Loss: 2.3408
[modern-gpt-train] New best saved at step 600 (val=2.3408)
Steps/sec: 0.099
Step 700, LR: 1.20e-04, Train Loss: 1.3051, Val Loss: 2.0307
[modern-gpt-train] New best saved at step 700 (val=2.0307)
Steps/sec: 0.101
Step 800, LR: 3.86e-05, Train Loss: 1.0758, Val Loss: 1.8776
[modern-gpt-train] New best saved at step 800 (val=1.8776)
Steps/sec: 0.098
Step 900, LR: 1.00e-05, Train Loss: 1.0763, Val Loss: 1.8230
[modern-gpt-train] New best saved at step 900 (val=1.8230)
[modern-gpt-train] Training complete. Best val=1.8230 at step 900.

[modern-gpt-train] Model saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v9/model.pt
[modern-gpt-train] Tokenizer saved to: /home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v9/tokenizer.json
[modern-gpt-train] Updated config saved to: /home/pooja-saxena/PoojaVault/Professional/Learning/NLP_and_LLMs/Transfomers_Foundation/course4_domain_expert_gpt/projects/9_extended_data/config_9.json
37:37 | I | ✅ Model training completed successfully!
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
