import pandas as pd
import json
from zhconv import convert

# --- Step 1: Load JSON dataset ---
with open('zh_idiom_meaning.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

df_json = pd.DataFrame(json_data)
df_json = df_json[['idiom', 'en_meaning']]
df_json.rename(columns={'idiom': 'chinese', 'en_meaning': 'english'}, inplace=True)
df_json['source'] = 'JSON'  # mark source

print(f"JSON dataset loaded: {len(df_json)} rows")

# --- Step 2: Load CSV dataset ---
df_csv = pd.read_csv('Chinese_proverbs.csv')
df_csv = df_csv[['in_chinese', 'text']]
df_csv.rename(columns={'in_chinese': 'chinese', 'text': 'english'}, inplace=True)
df_csv['source'] = 'CSV'  # mark source

print(f"CSV dataset loaded: {len(df_csv)} rows")

# --- Step 3: Normalize Chinese characters (Traditional -> Simplified) ---
df_json['chinese'] = df_json['chinese'].apply(lambda x: convert(x, 'zh-cn'))
df_csv['chinese'] = df_csv['chinese'].apply(lambda x: convert(x, 'zh-cn'))

# --- Step 4: Combine datasets ---
df_combined = pd.concat([df_json, df_csv], ignore_index=True)
print(f"Combined dataset: {len(df_combined)} rows")

# --- Step 5: Find and show duplicates ---
duplicates = df_combined[df_combined.duplicated(subset='chinese', keep=False)]
if not duplicates.empty:
    print("\nFound duplicates (before dropping):")
    print(duplicates.sort_values(['chinese', 'source']))
    print(f"Total duplicates found: {len(duplicates)}")
else:
    print("\nNo duplicates found.")

# --- Step 6: Remove duplicates ---
# Keep JSON version if duplicate exists across JSON and CSV
df_combined.sort_values(by='source', inplace=True)  # JSON first, then CSV
df_combined.drop_duplicates(subset='chinese', keep='first', inplace=True)

print(f"Dataset after removing duplicates: {len(df_combined)} rows")

# --- Step 7: Save cleaned dataset ---
df_combined.to_csv('chinese_english_proverbs_cleaned.csv', index=False, encoding='utf-8-sig')

print("\nCleaned dataset saved to 'chinese_english_proverbs_cleaned.csv'")

#results
# JSON dataset loaded: 8643 rows
# CSV dataset loaded: 127 rows
# Combined dataset: 8770 rows

# Found duplicates (before dropping):
#      chinese                                            english
# 48      一干二净                          completely and thoroughly
# 5566    一干二净  completely and thoroughly, leaving nothing behind
# 316     不遗余力            spare no effort; do everything possible
# 7953    不遗余力                   spare no effort, do one's utmost
# 725     前仆后继  succeeding each other in a continuous and unbr...
# 727     前仆后继             successors stepping forward one by one
# 869     反复无常  being unpredictable or changing one's mind fre...
# 4254    反复无常  being inconsistent and unpredictable, changing...
# 924     固执己见  being stubborn and insisting on one's own opin...
# 1085    固执己见            holding onto one's own views stubbornly
# 2583    无济于事                               ineffective, useless
# 4950    无济于事      ineffective or unable to remedy the situation
# 2756    生龙活虎                        full of energy and vitality
# 2751    生龙活虎                        full of energy and vitality
# 2798    疲于奔命  exhausted from running around, busy and overwh...
# 4328    疲于奔命       exhausted from running around and being busy
# 4358    耿耿于怀  holding a grudge in one's heart, unable to let...
# 8640    耿耿于怀                    to bear a grudge in one's heart
# 854     触景生情    being emotionally moved by a scene or situation
# 3599    触景生情  being emotionally moved or stirred by a scene ...
# 5245    青出于蓝                   The student surpasses the master
# 7431    青出于蓝                 The student surpasses the teacher.
# Total duplicates found: 22
# Dataset after removing duplicates: 8759 rows
