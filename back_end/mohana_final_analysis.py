# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 18:41:29 2025

@author: mohana
"""

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
filename = r"isc_funding_openai_PROGRAMS.json"
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

#############################################
# Count missing values for both columns
null_counts = {
    "Null full_text": df['full_text'].isna().sum(),
    "Null description": df['description'].isna().sum()
}

# Convert to DataFrame
null_df = pd.DataFrame(list(null_counts.items()), columns=['Category', 'Count'])

# Plot the bar chart
plt.figure(figsize=(6, 5))
ax = sns.barplot(x="Category", y="Count", data=null_df, palette="magma")

# Add count labels on top of each bar
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2, p.get_height()), 
                ha='center', va='bottom', fontsize=12, fontweight='bold')

# Customize labels and title
plt.ylabel("Count")
plt.title("Comparison of Missing full_text and description Entries")
plt.show()

# Print the counts
print(null_df)

#######################################################
# Check if 'program_id' and 'full_text' columns exist
if 'program_id' in df.columns and 'full_text' in df.columns:
    # Filter rows where full_text is null
    null_full_text_df = df[df['full_text'].isna()]
    
    # Print the program IDs with null full_text
    print("Program IDs with null full_text:")
    print(null_full_text_df['program_id'].tolist())  # Convert to list for better readability

    # Optional: Show the full DataFrame rows if needed
    # print(null_full_text_df)
else:
    print("Error: 'program_id' or 'full_text' column not found in the DataFrame.")


########################################################
# Check if required columns exist
if {'program_id', 'full_text', 'program_name'}.issubset(df.columns):
    # Filter rows where program_name is null
    null_program_name_df = df[df['program_name'].isna()][['program_id', 'full_text']]
    
    # Define the output file name
    output_filename = "null_program_name_records.csv"
    
    # Save to CSV
    null_program_name_df.to_csv(output_filename, index=False, encoding='utf-8')
    
    print(f"Filtered data successfully saved to '{output_filename}'.")
else:
    print("Error: One or more required columns ('program_id', 'full_text', 'program_name') are missing in the DataFrame.")

#################################################################
# Define error messages to search for
error_messages = [
    "Your browser does not support JavaScript",
    "Failed accessing Website",
    "403 error",
    "Related Content",
    "You need to enable JavaScript to run this app",
    "We're sorry but inno-centre.com doesn't work properly without JavaScript enabled"
]

# Create an empty dictionary to store counts
error_counts = {}

# Filter the DataFrame for each error message
for error in error_messages:
    count = df[df['full_text'].str.contains(error, na=False, case=False)].shape[0]
    error_counts[error] = count

# Convert to DataFrame for visualization
error_df = pd.DataFrame(list(error_counts.items()), columns=['Error Message', 'Count'])

# Print program IDs for each error type
print("Program IDs with errors in full_text:")
for error in error_messages:
    error_programs = df[df['full_text'].str.contains(error, na=False, case=False)][['program_id', 'full_text']]
    print(f"\nError: {error}")
    print(error_programs)

# Plot the counts as a bar chart
plt.figure(figsize=(10, 5))
ax = sns.barplot(x="Error Message", y="Count", data=error_df, palette="coolwarm")

# Add count labels on top of each bar
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2, p.get_height()), 
                ha='center', va='bottom', fontsize=12, fontweight='bold')

# Customize labels and title
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.ylabel("Count")
plt.title("Occurrences of Errors in full_text")
plt.show()


# Plot the counts as a pie chart
plt.figure(figsize=(8, 8))
plt.pie(error_df['Count'], labels=error_df['Error Message'], autopct='%1.1f%%', 
        startangle=140, colors=sns.color_palette("coolwarm", len(error_df)), wedgeprops={'edgecolor': 'black'})

# Add a title
plt.title("Distribution of Errors in full_text")

# Show the chart
plt.show()

# Create the pie chart
plt.figure(figsize=(10, 8))
colors = sns.color_palette("coolwarm", len(error_df))  # Define distinct colors
wedges, texts, autotexts = plt.pie(error_df['Count'], labels=None, autopct='%1.1f%%', 
                                   startangle=140, colors=colors, wedgeprops={'edgecolor': 'black'})

# Create a legend on the side with corresponding colors
plt.legend(wedges, error_df['Error Message'], title="Error Types", loc="center left", bbox_to_anchor=(1, 0.5))

# Add a title
plt.title("Distribution of Errors in full_text")

# Show the chart
plt.show()



####################################################








# Count missing values in full_text
missing_full_text_count = df['full_text'].isna().sum()
total_count = len(df)

# Create a summary DataFrame
missing_summary = pd.DataFrame({
    "Category": ["Missing full_text", "Available full_text"],
    "Count": [missing_full_text_count, total_count - missing_full_text_count]
})

# Plot missing vs available full_text entries
plt.figure(figsize=(6, 4))
sns.barplot(x="Category", y="Count", data=missing_summary, palette="coolwarm")
plt.xlabel("Full Text Availability")
plt.ylabel("Count")
plt.title("Programs with Missing full_text")
plt.show()

print(f"Total programs: {total_count}")
print(f"Missing full_text entries: {missing_full_text_count}")


##########################################################################

# Check for rows where 'description' is null
null_description_df = df[df['description'].isnull()]

# Count the number of rows with null 'description'
null_description_count = null_description_df.shape[0]

# Print the count
print(f"Number of programs with null 'description': {null_description_count}")

# Plot a bar graph
plt.figure(figsize=(5, 5))
sns.barplot(x=["Null description"], y=[null_description_count], palette='magma')
plt.ylabel("Count")
plt.title("Programs with Null 'description'")
plt.show()

# Preview rows with null 'description'
print(null_description_df)


####################################################
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator

DetectorFactory.seed = 0  # Ensure consistent language detection

# Check if 'full_text' exists
if 'full_text' not in df.columns:
    print("Column 'full_text' not found in the DataFrame.")
else:
    # Detect language for each full_text entry
    def detect_language(text):
        try:
            return detect(text) if pd.notna(text) else 'unknown'
        except:
            return 'unknown'

    df['detected_language'] = df['full_text'].apply(detect_language)

    # Count non-English languages
    non_english_counts = df[df['detected_language'] != 'en']['detected_language'].value_counts()

    # Plot non-English language distribution
    plt.figure(figsize=(10, 5))
    sns.barplot(x=non_english_counts.index, y=non_english_counts.values, palette='plasma')
    plt.xlabel("Languages")
    plt.ylabel("Count")
    plt.title("Programs in Languages Other than English")
    plt.xticks(rotation=45)
    plt.show()

    # Translate non-English text and store in a new column
    def translate_to_english(text, lang):
        if lang != 'en' and lang != 'unknown':
            try:
                return GoogleTranslator(source=lang, target='en').translate(text)
            except Exception as e:
                print(f"Translation error for language {lang}: {e}")
                return text  # Return original if translation fails
        return text  # Return original if already in English

    df['translated_full_text'] = df.apply(
        lambda row: translate_to_english(row['full_text'], row['detected_language']), axis=1
    )

    print("Translation complete. The DataFrame now contains a 'translated_full_text' column.")
