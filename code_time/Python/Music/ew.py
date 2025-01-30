import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os

# -------------------------------
# Step 1: Load the CSV File
# -------------------------------

def load_csv(file_path):
    """
    Loads the CSV file into a pandas DataFrame.
    
    :param file_path: Path to the CSV file.
    :return: pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded '{file_path}' with {len(df)} entries.")
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        exit()
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty.")
        exit()
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        exit()

# -------------------------------
# Step 2: Remove Duplicates
# -------------------------------

def remove_duplicates(df, threshold=90):
    """
    Removes duplicate songs based on fuzzy matching of 'Song Name' and 'Artist'.
    
    :param df: pandas DataFrame containing the music library.
    :param threshold: Similarity score threshold to consider duplicates.
    :return: DataFrame without duplicates.
    """
    df = df.copy()
    # Create a combined string for matching
    df['combined'] = (df['Song Name'].astype(str) + " " + df['Artist'].astype(str)).str.lower()
    
    unique_songs = []
    duplicates = []
    
    for index, row in df.iterrows():
        song = row['combined']
        if not unique_songs:
            unique_songs.append(song)
            continue
        # Find the best match in unique_songs
        match, score = process.extractOne(song, unique_songs, scorer=fuzz.token_sort_ratio)
        if score < threshold:
            unique_songs.append(song)
        else:
            duplicates.append(index)
    
    print(f"Found {len(duplicates)} duplicate entries out of {len(df)} total songs.")
    df_cleaned = df.drop(duplicates).drop('combined', axis=1)
    return df_cleaned

# -------------------------------
# Step 3: Assign Genres
# -------------------------------

def assign_genres(df):
    """
    Assigns genres to each song. It first tries to assign genres based on a predefined mapping.
    If a song's artist is not in the mapping, it prompts the user to input the genre.
    
    :param df: pandas DataFrame without duplicates.
    :return: DataFrame with an added 'Genre' column.
    """
    df = df.copy()
    df['Genre'] = ''
    
    # Predefined genre mapping (extend this dictionary as needed)
    genre_mapping = {
        'kendrick lamarr': 'Hip-Hop/Rap',
        'mac miller': 'Hip-Hop/Rap',
        'j. cole': 'Hip-Hop/Rap',
        'chance the rapper': 'Hip-Hop/Rap',
        'juice wrld': 'Hip-Hop/Rap',
        'the weeknd': 'R&B',
        'drake': 'Hip-Hop/Rap',
        'asap rocky': 'Hip-Hop/Rap',
        'xxxtentacion': 'Hip-Hop/Rap',
        'lil baby': 'Hip-Hop/Rap',
        'travis scott': 'Hip-Hop/Rap',
        'billie holiday': 'Jazz',
        'kanye west': 'Hip-Hop/Rap',
        'lil uzi vert': 'Hip-Hop/Rap',
        'gorillaz': 'Alternative/Rock',
        'jasmine': 'Jazz',
        'simon & garfunkel': 'Folk/Rock',
        # Add more artists and their genres here
    }
    
    # Function to get genre from mapping or prompt user
    def get_genre(song_name, artist):
        artist_lower = artist.lower()
        if artist_lower in genre_mapping:
            return genre_mapping[artist_lower]
        else:
            genre = input(f"Enter genre for '{song_name}' by {artist} (or press Enter to skip): ").strip()
            return genre
    
    print("\n--- Genre Assignment ---")
    print("Assigning genres based on predefined mapping. For unknown artists, you'll be prompted to enter the genre.\n")
    
    for index, row in df.iterrows():
        song = row['Song Name']
        artist = row['Artist']
        genre = get_genre(song, artist)
        df.at[index, 'Genre'] = genre
    
    print("\nGenre assignment completed.\n")
    return df

# -------------------------------
# Step 4: Export to New CSV
# -------------------------------

def export_csv(df, output_file):
    """
    Exports the DataFrame to a CSV file.
    
    :param df: pandas DataFrame to export.
    :param output_file: Path to the output CSV file.
    """
    try:
        df.to_csv(output_file, index=False)
        print(f"Successfully exported organized library to '{output_file}'.")
    except Exception as e:
        print(f"An error occurred while exporting the file: {e}")

# -------------------------------
# Step 5: Main Function
# -------------------------------

def main():
    # Define input and output file paths
    input_file = 'music_library.csv'  # Replace with your actual input file name
    output_file = 'organized_music_library.csv'  # Desired output file name
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: The input file '{input_file}' does not exist in the current directory.")
        exit()
    
    # Load CSV
    df = load_csv(input_file)
    
    # Remove Duplicates
    df_cleaned = remove_duplicates(df, threshold=90)
    
    # Assign Genres
    df_with_genres = assign_genres(df_cleaned)
    
    # Export to CSV
    export_csv(df_with_genres, output_file)

if __name__ == "__main__":
    main()
