import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import base64
import logging
from tqdm import tqdm

# Setup logging
# Set up logging format
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_datefmt = "%Y-%m-%d %H:%M:%S"

# Set up logging levels
logging.basicConfig(format=log_format, datefmt=log_datefmt, level=logging.INFO)

# Get the root logger
logger = logging.getLogger()

# Create file handler which logs debug messages
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter(log_format, datefmt=log_datefmt)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Enable tqdm progress bar for pandas
tqdm.pandas()

# Constants
CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = "http://localhost:8080/callback"
SCOPE = "playlist-modify-public ugc-image-upload"
LIMIT =  100

def get_spotify_track_id(title, artist):
    """
    Search for a track on Spotify and return its ID.

    Args:
        title (str): The title of the track.
        artist (str): The artist of the track.

    Returns:
        str: The Spotify ID of the track, or None if not found.
    """
    query = f"{title} {artist}"
    results = sp.search(query, limit=1, type='track')
    items = results['tracks']['items']
    return items[0]['id'] if items else None

def add_tracks_to_spotify_playlist(playlist_id, track_uris):
    """
    Add tracks to a Spotify playlist in batches of  100.

    Args:
        playlist_id (str): The ID of the Spotify playlist.
        track_uris (list): List of track URIs to add.
    """
    chunks = [track_uris[i:i + LIMIT] for i in range(0, len(track_uris), LIMIT)]
    for chunk in chunks:
        sp.playlist_add_items(playlist_id, chunk)
        logger.info(f"Added {len(chunk)} tracks to the playlist.")

def add_thumbnail_to_spotify_playlist(image_relative_path, playlist_id):
    """
    Upload an image as a thumbnail to a Spotify playlist.

    Args:
        image_relative_path (str): The relative path to the image file.
        playlist_id (str): The ID of the Spotify playlist.
    """
    try:
        with open(image_relative_path, 'rb') as img_file:
            b64_encoded_img = base64.b64encode(img_file.read()).decode('utf-8')
            sp.playlist_upload_cover_image(playlist_id, b64_encoded_img)
            logger.info(f"Added thumbnail to the playlist.")
    except Exception as e:
        logger.error(f"Failed to upload thumbnail: {e}")



try:
    # Original file path
    original_file_path = 'shazamlibrary.csv'

    # New temporary file path
    temp_file_path = 'shazamlibrary_no_header.csv'

    # Open the original file and read lines
    with open(original_file_path, 'r', encoding='utf-8') as original_file:
        lines = original_file.readlines()

    # Write all lines except the header to the new temporary file
    with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
        temp_file.writelines(lines[1:])

    # Read the CSV file
    df = pd.read_csv(temp_file_path, encoding='utf-8')

    # Authenticate with Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE))

    # Add SpotifyID column with correct value for each track
    df['SpotifyID'] = df.progress_apply(lambda row: get_spotify_track_id(row['Title'], row['Artist']), axis=1)


    # Retrieves info about the user
    results = sp.current_user()
    user_id = results['id']

    # Create the playlist
    playlist = sp.user_playlist_create(user=user_id, name="Shazam Songs", description="Playlist containing all tagged songs from Shazam")
    playlist_id = playlist['id']

    # Add all the tracks to the playlist with their Spotify ID
    track_ids = df['SpotifyID'].tolist()
    add_tracks_to_spotify_playlist(playlist_id, track_ids)

    # Add a thumbnail to the spotify playlist
    add_thumbnail_to_spotify_playlist('logo.png', playlist_id)

    # Remove the temporary file
    os.remove(temp_file_path)
except Exception as e:
    logger.error(f"An error occurred: {e}")
