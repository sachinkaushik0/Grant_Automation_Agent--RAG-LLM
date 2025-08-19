import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Load JSON data, ignoring invalid control characters
with open("/content/sample_data/isc_funding_openai_PROGRAMS.json", "r", encoding="utf-8") as f:
    # The strict=False argument allows json.load to ignore invalid control characters
    data = json.load(f, strict=False) 

# Convert to DataFrame
df = pd.DataFrame(data)
print("\n DATA\n")
print(df.head())
print("\n INFO\n")
print(df.info())
print("\n DESCRIBE\n")
print(df.describe())
print("\n NULL VALUES\n")
print(df.isnull().sum())
print("\n SHAPE ")
print(df.shape)

# Check if there are null values in 'full_text'
null_count = df['full_text'].isnull().sum()

if null_count > 0:
    print(f"There are {null_count} entries with 'full_text = null'.")
else:
    print("No entries with 'full_text = null'.")

# Display basic information
df_info = pd.DataFrame(df.isnull().sum(), columns=['Null Values'])
df_info['Percentage'] = (df_info['Null Values'] / len(df)) * 100

# Visualizing Null Values
plt.figure(figsize=(10, 6))
sns.barplot(x=df_info.index, y=df_info['Null Values'], palette="viridis")
plt.xticks(rotation=90)
plt.ylabel("Count of Null Values")
plt.title("Null Values in Each Column")
plt.show()

# Visualizing Data Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df_info['Percentage'], bins=10, kde=True, color="blue")
plt.xlabel("Percentage of Null Values")
plt.ylabel("Number of Columns")
plt.title("Distribution of Null Values Across Columns")
plt.show()

# Checking null values in 'full_text' and 'description'
null_counts = {
    "full_text": df['full_text'].isnull().sum(),
    "description": df['description'].isnull().sum()
}

# Bar plot for 'full_text' and 'description' null values
plt.figure(figsize=(6, 4))
sns.barplot(x=list(null_counts.keys()), y=list(null_counts.values()), palette="coolwarm")
plt.ylabel("Count of Null Values")
plt.title("Null Values in 'full_text' and 'description' Columns")
plt.show()


# Display null value summary using display() instead of ace_tools
# This will print the DataFrame to the output
display(df_info.style.set_caption("Null Value Summary")) 

# 1) Count and remove entries where both 'full_text' and 'description' are null
null_full_text_description = df[(df['full_text'].isnull()) & (df['description'].isnull())]
count_null_full_text_description = null_full_text_description.shape[0]

# Remove these entries from the DataFrame
df_cleaned = df.drop(null_full_text_description.index)

# 2) Identify and count different languages in the dataset (assuming a 'language' field exists)
if 'language' in df.columns:
    language_counts = df['language'].value_counts()
else:
    language_counts = "No 'language' column found in the dataset."

# 3) Identify program_id with 'full_text' containing the specific JavaScript-related phrase
js_error_phrase = "Your browser does not support JavaScript. Some components may not be visible"
program_ids_with_js_error = df_cleaned[df_cleaned['full_text'].str.contains(js_error_phrase, na=False)][['program_id', 'full_text']]

# Remove these entries from the DataFrame
df_cleaned = df_cleaned[~df_cleaned['full_text'].str.contains(js_error_phrase, na=False)]

# Final cleaned DataFrame shape
cleaned_shape = df_cleaned.shape

# Display results
results = {
    "Count of entries with both 'full_text' and 'description' null": count_null_full_text_description,
    "Language distribution": language_counts,
    "Programs with JavaScript error phrase": program_ids_with_js_error,
    "Shape of cleaned DataFrame": cleaned_shape
}

# Show the program IDs with the JavaScript error phrase
#print("\nPrograms with JavaScript error phrase:\n")
#display(program_ids_with_js_error)

# Display the results in text format
results

!pip install langdetect

from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

# Function to detect language with error handling
def detect_language(text):
    try:
        if pd.notna(text) and isinstance(text, str):
            return detect(text)
        else:
            return "unknown"
    except LangDetectException:
        return "unknown"

# Apply language detection on 'full_text' column
df_cleaned['detected_language'] = df_cleaned['full_text'].apply(detect_language)

# Count occurrences of detected languages
language_counts = df_cleaned['detected_language'].value_counts()

# Remove non-English entries
df_cleaned = df_cleaned[df_cleaned['detected_language'] == "en"]

# Display the updated shape of cleaned DataFrame
cleaned_shape = df_cleaned.shape

# Show detected language distribution
from IPython.display import display
display(language_counts.to_frame().style.set_caption("Detected Language Distribution"))

print(f"Entries removed due to non-English language: {language_counts.sum() - language_counts.get('en', 0)}")
print(f"New shape of cleaned DataFrame: {cleaned_shape}")
