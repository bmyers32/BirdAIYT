
import subprocess
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

class VideoProcessor:
    def process_video(self, video_path, text_overlay, music_path, output_path):
        try:
            cropped_path = video_path.replace(".mp4", "_cropped.mp4")
            self.crop_top(video_path, cropped_path)

            video = VideoFileClip(cropped_path)
            text = TextClip(text_overlay, fontsize=40, color='white', bg_color='black')
            text = text.set_duration(video.duration).set_pos(("center", "bottom"))
            video = CompositeVideoClip([video, text])

            music = AudioFileClip(music_path).subclip(0, min(video.duration, 60))
            final = video.set_audio(music)
            final.write_videofile(output_path, codec="libx264", audio_codec="aac")

            return output_path
        except Exception as e:
            print(f"Processing error: {e}")
            return None

    def crop_top(self, input_path, output_path, crop_height=50):
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-filter:v", f"crop=in_w:in_h-{crop_height}:0:{crop_height}",
            "-c:a", "copy", output_path
        ]
        subprocess.run(cmd, check=True)
