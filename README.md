# 🐦 BirdAIYT – Automated Bird Video Creator + AI Facts + YouTube Uploader

BirdAIYT is a fully automated content pipeline that:
- Selects a random bird video based on species
- Crops out timestamp overlays
- Generates an AI-powered bird fact using GPT-4
- Adds the fact as a visual overlay
- Mixes in royalty-free background music
- Uploads the final video to YouTube with a title and description

Perfect for bird lovers, AI tinkerers, and automation enthusiasts.

---

## 🚀 Features

- 🧠 AI-generated species-specific facts using OpenAI
- 🎬 Video cropping, text overlay, and audio mixing via MoviePy + ffmpeg
- 🎶 Random music selection from a local library
- ☁️ YouTube upload with automatic title, description, and tags
- 🕒 Optional: schedule to run daily via cron or task scheduler

---

## 📁 Project Structure
BirdAIYT/

├── main.py # Entry point

├── utils.py # Helper functions

├── fact_generator.py # AI + fallback fact engine

├── video_processor.py # Handles ffmpeg + MoviePy logic
├── youtube_uploader.py # Uses YouTube Data API
├── config.json # API keys (excluded from Git)
├── requirements.txt
├── .gitignore
├── videos/ # Organized by species (e.g., /videos/Cardinal/)
├── music/ # Background .mp3s
├── facts/ # Fallback JSON fact database
├── output/ # Final videos
├── logs/ # Daily logs

yaml
Copy code

---

## 🔧 Installation

### 1. Clone the repo

```bash
git clone https://github.com/bmyers32/BirdAIYT.git
cd BirdAIYT


## 🔒 License

This project is licensed under **no open license**.  
You may **not** copy, distribute, modify, or reuse any part of this codebase without explicit written permission from the author.

© 2025 Breon Myers. All rights reserved.