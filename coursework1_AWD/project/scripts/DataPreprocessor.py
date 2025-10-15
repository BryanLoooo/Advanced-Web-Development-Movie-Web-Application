import pandas as pd

# File paths to CSV files
movies_file = 'C:\\AdvancedWebDevelopment Mid Term Project\\midTermProj_AWD\\project\\scripts\\Movies.csv'
genres_file = 'C:\\AdvancedWebDevelopment Mid Term Project\\midTermProj_AWD\\project\\scripts\\Genres.csv'
stars_file = 'C:\\AdvancedWebDevelopment Mid Term Project\\midTermProj_AWD\\project\\scripts\\Stars.csv'
directors_file = 'C:\\AdvancedWebDevelopment Mid Term Project\\midTermProj_AWD\\project\\scripts\\Directors.csv'

# Load CSV files into pandas DataFrames
movies_df = pd.read_csv(movies_file)
genres_df = pd.read_csv(genres_file)
stars_df = pd.read_csv(stars_file)
directors_df = pd.read_csv(directors_file)

# Display initial data for inspection
print("Initial Datasets:")
print("Movies:", movies_df.head(), sep="\n")
print("Genres:", genres_df.head(), sep="\n")
print("Stars:", stars_df.head(), sep="\n")
print("Directors:", directors_df.head(), sep="\n")

# Define cleaning and preprocessing functions
def clean_runtime(value):
    """Clean runtime values and convert to integer."""
    try:
        value = str(value).replace(' min', '').replace(',', '').strip()
        return int(value)
    except ValueError:
        return 0  # Default runtime for invalid or missing values

def clean_votes(value):
    """Clean votes values and convert to integer."""
    try:
        value = str(value).replace(',', '').replace('$', '').strip()
        if 'M' in value:
            return int(float(value.replace('M', '')) * 1_000_000)
        elif 'K' in value:
            return int(float(value.replace('K', '')) * 1_000)
        return int(value)
    except ValueError:
        return 0  # Default votes for invalid or missing values

# Preprocess Movies.csv data
movies_df['runtime'] = movies_df['runtime'].apply(clean_runtime)
movies_df['votes'] = movies_df['votes'].apply(clean_votes)
movies_df['rating'] = movies_df['rating'].fillna(0).astype(float)  # Fill missing ratings with 0
movies_df.fillna('NULL', inplace=True)  # Replace other missing values with "NULL"
movies_df.drop_duplicates(inplace=True)  # Remove duplicate rows

# Preprocess Genres.csv data
genres_df['genre'] = genres_df['genre'].str.strip().fillna('NULL')  # Replace missing genres with "NULL"
genres_df.drop_duplicates(inplace=True)  # Remove duplicate rows
genres_df = genres_df[genres_df['genre'] != 'NULL']  # Remove rows still marked as "NULL"

# Preprocess Stars.csv data
stars_df['stars'] = stars_df['stars'].str.strip().fillna('NULL')  # Replace missing stars with "NULL"
stars_df.drop_duplicates(inplace=True)  # Remove duplicate rows
stars_df = stars_df[stars_df['stars'] != 'NULL']  # Remove rows still marked as "NULL"

# Preprocess Directors.csv data
directors_df['director'] = directors_df['director'].str.strip().fillna('NULL')  # Replace missing directors with "NULL"
directors_df.drop_duplicates(inplace=True)  # Remove duplicate rows
directors_df = directors_df[directors_df['director'] != 'NULL']  # Remove rows still marked as "NULL"

# Save cleaned data to new CSV files
movies_df.to_csv('cleaned_Movies.csv', index=False)
genres_df.to_csv('cleaned_Genres.csv', index=False)
stars_df.to_csv('cleaned_Stars.csv', index=False)
directors_df.to_csv('cleaned_Directors.csv', index=False)

print("\nPreprocessing complete. Cleaned files saved:")
print(" - cleaned_Movies.csv")
print(" - cleaned_Genres.csv")
print(" - cleaned_Stars.csv")
print(" - cleaned_Directors.csv")