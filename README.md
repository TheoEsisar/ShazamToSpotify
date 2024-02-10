# Shazam Tagged Songs to Spotify Playlist

## Overview

Shazam Tagged Songs to Spotify Playlist is a Python script designed to automate the creation of Spotify playlists based on a CSV file containing song metadata. It uses the Spotipy library to interact with the Spotify Web API and create a playlist with track IDs fetched from the Spotify database.

## Features

- Searches for Spotify track IDs using song title and artist name.
- Adds tracks to a Spotify playlist in batches.
- Allows uploading a custom thumbnail image to the playlist.

## Prerequisites

- Python  3.x
- `pandas` library for handling CSV files
- `spotipy` library for interacting with the Spotify Web API
- `tqdm` libray to show the progress when getting the Spotify ID for each track

## Installation

1. Clone the repository to your local machine.
2. Create a Python virtual environment (optional but recommended).
3. Activate the virtual environment and install the required libraries using pip:

   ```
   pip install pandas spotipy
   ```

## Retrieve Shazam Library CSV File

Before running the script, you need to obtain the `shazamlibrary.csv` file from your Shazam account. Follow these steps to export your tagged songs:

1. Log in to your Shazam account on the [Shazam website](https://www.shazam.com/).
2. Navigate to the settings or profile section.
3. Look for an option to export your tagged songs or listen history. This option might be labeled something like "Export Tagged Songs," "Listen History," or similar.
4. Click the button to download the CSV file. Save the file to your desired location on your computer.

Once you have the CSV file, place it in the root directory of your project where the Python script expects to find it. Then, you can proceed to run the script as detailed in the usage instructions.

## Usage

Before running the script, ensure you have completed the following setup steps:

1. **Set up a Spotify Developer Account**: Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and sign in or create an account.
2. **Create a Spotify App**: Register a new application and obtain your `CLIENT_ID`, `CLIENT_SECRET`, and set the `REDIRECT_URI` to `http://localhost`.
3. **Environment Variables**: Store your `CLIENT_ID` and `CLIENT_SECRET` as environment variables in your operating system or in a `.env` file.
4. **Install Dependencies**: Ensure all required Python libraries are installed as described in the Installation section.

To run the script:

1. Open a terminal in the project directory.
2. Run the script using the following command:

   ```
   python main.py
   ```

Upon launching the script, you will be prompted to log in to your Spotify account via the browser. Follow the prompts to authorize the application and grant access to modify your public playlists and upload cover images.

## Configuration

The script expects a CSV file named `shazamlibrary.csv` with columns for `Title` and `Artist`. Make sure this file is present in the project directory before running the script.


## License

This project is licensed under the terms of the MIT license. See the LICENSE file for details.

## Acknowledgements

- [Spotipy Documentation](https://spotipy.readthedocs.io/)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)