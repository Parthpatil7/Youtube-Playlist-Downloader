import os
import pytube
import requests
from tqdm import tqdm

# Get the playlist URL
playlist_url = ""

def download_video(video, download_path):
    video_stream = video.streams.get_highest_resolution()
    file_size = video_stream.filesize

    response = requests.get(video_stream.url, stream=True)
    
    with open(download_path, 'wb') as f, tqdm(
            desc=f"Downloading {video.title}",
            total=file_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            dynamic_ncols=True,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            f.write(data)
            progress_bar.update(len(data))
        progress_bar.close()

try:
    # Create a Playlist object
    playlist = pytube.Playlist(playlist_url)

    # Create a directory to store downloaded videos in the current directory
    download_dir = os.getcwd()  # Use the current working directory
    playlist_dir = playlist.title.replace(" ", "_")  # Access title as an attribute
    os.makedirs(playlist_dir, exist_ok=True)
    
    for video in playlist.videos:
        try:
            download_path = os.path.join(download_dir, playlist_dir, f"{video.title}.mp4")
            download_video(video, download_path)
        except Exception as e:
            print(f"Error downloading {video.title}: {str(e)}")

    # Print a success message
    print("All videos downloaded successfully!")

except Exception as e:
    print(f"Error accessing playlist: {str(e)}")
