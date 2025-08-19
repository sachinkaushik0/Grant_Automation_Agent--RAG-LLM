import json
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

######################################PRE-PROCESSING##########################################

###################################INITIAL EXPLORATION########################################
def clean_raw_json(filename):
    """ Cleans the raw JSON file by removing invalid control characters. """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            raw_data = f.read()
        
        if not raw_data:
            print("Warning: The file is empty.")
            return None

        # Remove any non-printable ASCII characters except newline (\n)
        cleaned_data = re.sub(r"[^\x20-\x7E\n]", "", raw_data)
        return cleaned_data
    
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

# Load and clean the JSON data
filename = r"C:/Mohana/3422/SEM 4/AI Capstone Project/Repo/Grant_Proposal_Team5/PROGRAMS.json"
raw_data = clean_raw_json(filename)

data = []  # Initialize data to avoid undefined variable error

if raw_data is None:
    print("The file could not be read or cleaned.")
else:
    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError as e:
        print(f"Error loading JSON: {e}")
        
# Create DataFrame from the cleaned data
df = pd.DataFrame(data)

# Print the shape of the DataFrame
print(f"Shape of the DataFrame: {df.shape}")

# Calculate percentage of null values for each column
null_percentage = (df.isnull().sum() / len(df)) * 100

# Plot percentage of null values
plt.figure(figsize=(12, 8))
ax = sns.barplot(x=null_percentage.index, y=null_percentage.values, palette="coolwarm")

# Add vertical labels inside the bars
for index, value in enumerate(null_percentage.values):
    ax.text(index, value / 2, f"{value:.2f}%", ha='center', va='center', rotation=90, fontsize=10, color='white', fontweight='bold')

plt.xticks(rotation=90)
plt.xlabel("Fields")
plt.ylabel("Percentage of Null Values (%)")
plt.title("Percentage of Null Values for Each Field in Dataset")
plt.ylim(0, 100)
plt.show()

#################OTHER LANGUAGE DETECTION##############
from langdetect import detect
# Count the number of non-English grants
non_english_grants = df[~df['full_text'].apply(lambda x: detect(x) == 'en' if pd.notnull(x) else True)]
print(f"Total number of non-English grants: {non_english_grants.shape[0]}")

# Filter out non-English 'full_text' rows
df_cleaned = df[df['full_text'].apply(lambda x: detect(x) == 'en' if pd.notnull(x) else True)]

# Print the shape of the DataFrame after dropping non-English grants
print(f"Shape of the DataFrame after dropping non-English grants: {df_cleaned.shape}")

#####################REMOVE "NONE" PROGRAM_NAME###############
# Count the number of rows where 'program_name' is None or NaN
none_program_name_count = df_cleaned[df_cleaned['program_name'].isnull()].shape[0]
print(f"Number of grants with 'program_name' as None: {none_program_name_count}")

# Drop the rows where 'program_name' is None or NaN
df_cleaned = df_cleaned.dropna(subset=['program_name'])

# Print the shape of the DataFrame after dropping rows with None in 'program_name'
print(f"Shape of the DataFrame after dropping grants with 'program_name' as None: {df_cleaned.shape}")

#########################REMOVE JAVASCRIPT ERROR FROM FULL_TEXT#################
# List of JavaScript error keywords
js_error_keywords = [
    "Your browser does not support JavaScript"
]

# Function to check for exact JavaScript error in full_text
def contains_js_error_exact(text):
    if pd.isnull(text):
        return False
    return text.lower() in [keyword.lower() for keyword in js_error_keywords]

# Count the number of rows where 'full_text' matches exactly any JavaScript error keyword
js_error_exact_count = df_cleaned[df_cleaned['full_text'].apply(contains_js_error_exact)].shape[0]

print(f"Total number of grants with exact JavaScript errors in 'full_text': {js_error_exact_count}")

############################DROP NULL FULL_TEXT ########################################
# Replace 'full_text' with 'description' if 'full_text' is None, and 'description' is not None
df_cleaned['full_text'] = df_cleaned.apply(
    lambda row: row['description'] if pd.isnull(row['full_text']) and pd.notnull(row['description']) else row['full_text'],
    axis=1
)

# Count the number of rows where both 'full_text' and 'description' are None (and will be dropped)
rows_to_drop = df_cleaned[df_cleaned['full_text'].isnull() & df_cleaned['description'].isnull()].shape[0]
print(f"Number of grants where both 'full_text' and 'description' are None and will be dropped: {rows_to_drop}")

# Drop rows where both 'full_text' and 'description' are None
df_cleaned = df_cleaned[~(df_cleaned['full_text'].isnull() & df_cleaned['description'].isnull())]

# Print the shape of the DataFrame after modifications
print(f"Shape of the DataFrame after replacing 'full_text' and dropping rows: {df_cleaned.shape}")

###################################### FETCH ELIGIBILITY ##########################################33


