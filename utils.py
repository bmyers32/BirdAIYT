
import json
import random
from pathlib import Path

def pick_random_file(folder, exts):
    files = [f for f in Path(folder).glob("*") if f.suffix in exts]
    return random.choice(files) if files else None

def load_config(path):
     with open(path) as f:
        return json.load(f)


def load_used_videos(skip_file="used_videos.json"):
    """Load list of previously used videos."""
    skip_file = Path(skip_file)
    if skip_file.exists():
        with open(skip_file) as f:
            return set(json.load(f))
    return set()


def save_used_video(video_path, skip_file="used_videos.json"):
    """Add video to the used videos list."""
    used_videos = load_used_videos(skip_file)
    used_videos.add(str(video_path))

    with open(skip_file, 'w') as f:
        json.dump(list(used_videos), f, indent=2)


def get_unused_videos(available_videos, skip_file="used_videos.json"):
    """Filter out videos that have been used before."""
    used_videos = load_used_videos(skip_file)
    unused_videos = {}

    for species, videos in available_videos.items():
        unused_species_videos = [v for v in videos if str(v) not in used_videos]
        if unused_species_videos:
            unused_videos[species] = unused_species_videos

    return unused_videos