
import os
import random
import logging
from datetime import datetime
from pathlib import Path

from video_processor import VideoProcessor
from fact_generator import FactGenerator
from youtube_uploader import YouTubeUploader
from utils import pick_random_file, load_config

config = load_config("config.json")
logging.basicConfig(
    filename="logs/birdtube.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

species_dirs = list(Path("videos").glob("*"))
if not species_dirs:
    logging.error("No species folders found in /videos")
    exit()

species_folder = random.choice(species_dirs)
species_name = species_folder.name
video_path = pick_random_file(species_folder, exts=[".mp4"])
music_path = pick_random_file("music", exts=[".mp3"])

if not video_path or not music_path:
    logging.error("Missing video or music file.")
    exit()

logging.info(f"Selected {video_path} for species {species_name}")

fact_gen = FactGenerator("facts/facts.json", config["openai_api_key"])
fact_text = fact_gen.get_fact(species_name)
logging.info(f"Generated fact: {fact_text}")

output_path = f"output/{species_name}_{datetime.now().strftime('%Y%m%d')}.mp4"
processor = VideoProcessor()
final_video = processor.process_video(
    video_path=str(video_path),
    text_overlay=fact_text,
    music_path=str(music_path),
    output_path=output_path
)

if not final_video:
    logging.error("Video processing failed.")
    exit()

uploader = YouTubeUploader("client_secrets.json")
video_title = f"Amazing {species_name} Fact 🐦"
video_description = f"Enjoy this fascinating fact about the {species_name}. Daily AI bird facts powered by automation!"

uploader.upload(
    file_path=final_video,
    title=video_title,
    description=video_description,
    tags=["birds", species_name, "nature", "wildlife", "AI"]
)
logging.info("Video uploaded successfully.")
