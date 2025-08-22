import os
import random
import logging
import shutil
from datetime import datetime
from pathlib import Path

#from video_processor import VideoProcessor
#from fact_generator import FactGenerator
#from youtube_uploader import YouTubeUploader
from utils import pick_random_file, load_config, load_used_videos, save_used_video, get_unused_videos
from dropbox_sync import DropboxVideoFetcher


def get_available_videos(videos_dir):
    """Get all available video files organized by species."""
    available_videos = {}
    species_dirs = list(Path(videos_dir).glob("*"))

    for species_folder in species_dirs:
        if species_folder.is_dir():
            video_files = list(species_folder.glob("*.mp4"))
            if video_files:
                available_videos[species_folder.name] = video_files

    return available_videos

def archive_video(video_path, archive_dir="archived_videos"):
    """Move used video to archive directory maintaining species structure."""
    video_path = Path(video_path)
    species_name = video_path.parent.name

    archive_species_dir = Path(archive_dir) / species_name
    archive_species_dir.mkdir(parents=True, exist_ok=True)

    archived_path = archive_species_dir / video_path.name
    shutil.move(str(video_path), str(archived_path))
    logging.info(f"Archived video: {video_path} -> {archived_path}")

def main():
    config = load_config("config.json")
    logging.basicConfig(
        filename="logs/birdtube.log",
        level=logging.INFO,
        format="%(asctime)s — %(levelname)s — %(message)s"
    )

    fetcher = DropboxVideoFetcher(
        access_token=config.get("dropbox_access_token"),
        refresh_token=config.get("dropbox_refresh_token"),
        app_key=config.get("dropbox_app_key"),
        app_secret=config.get("dropbox_app_secret"),
        dropbox_root="/BirdVideos",
        local_root="videos",
        modified_within_days=1
    )
    #fetcher.sync_videos()

    # Get all available videos
    available_videos = get_available_videos("videos")
    if not available_videos:
        logging.error("No videos available for processing.")
        return

    # Randomly select a species that has videos
    species_name = random.choice(list(available_videos.keys()))
    Bird_Type = species_name.split("_")[0]
    Bird_Count = species_name.split("_")[1]
    video_path = random.choice(available_videos[species_name])
    logging.info(f"Selected {video_path} for species {species_name}")


if __name__ == "__main__":
    main()