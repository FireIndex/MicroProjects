import os
import subprocess
import random


class VideoWatermarker:
    def __init__(self, input_file, watermark_text, font_file, font_size=12, font_color="gray@0.8", frame_rate="10", threads="4"):
        self.input_file = input_file
        self.output_file = f"{os.path.splitext(input_file)[0]}_BigW.mp4"
        self.watermark_text = watermark_text
        self.font_file = font_file
        self.font_size = font_size
        self.font_color = font_color
        self.frame_rate = frame_rate
        self.threads = threads
        self.segment_files = []

    @staticmethod
    def get_random_position():
        return random.randint(0, 100)

    def split_video_into_segments(self):
        segment_duration = random.randint(4, 7)
        subprocess.call([
            "ffmpeg", "-i", self.input_file, "-c", "copy", "-map", "0",
            "-segment_time", f"00:{segment_duration}:00", "-f", "segment", "-reset_timestamps", "1",
            f"{os.path.splitext(self.input_file)[0]}S%03d.mp4"
        ])
        self.segment_files = [
            f for f in os.listdir() if f.startswith(os.path.splitext(self.input_file)[0] + "S") and f.endswith('.mp4')
        ]

    def apply_watermark(self):
        for segment_file in self.segment_files:
            watermarked_segment_file = f"{os.path.splitext(segment_file)[0]}_watermarked.mp4"
            base_x = self.get_random_position()
            base_y = self.get_random_position()
            subprocess.call([
                "ffmpeg", "-i", segment_file, "-r", self.frame_rate,
                "-vf", (
                    f"drawtext=fontfile='{self.font_file}':text='{self.watermark_text}':fontsize={str(self.font_size)}:fontcolor='{self.font_color}':"
                    f"x='if(eq(mod(t,5),0),({base_x}/100*W-text_w)*random(1),x)':"
                    f"y='if(eq(mod(t,5),0),({base_y}/100*H-text_h)*random(1),y)'"
                ),
                "-threads", self.threads, "-c:v", "libx264", "-preset", "ultrafast", watermarked_segment_file
            ])

    def concatenate_segments(self):
        with open("segments_watermarked.txt", "w") as f:
            for segment_file in self.segment_files:
                f.write(f"file '{os.path.splitext(segment_file)[0]}_watermarked.mp4'\n")
        subprocess.call([
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", "segments_watermarked.txt",
            "-c", "copy", self.output_file
        ])

    def clean_up(self):
        for segment_file in self.segment_files:
            os.remove(segment_file)
            os.remove(f"{os.path.splitext(segment_file)[0]}_watermarked.mp4")
        os.remove("segments_watermarked.txt")

    def process_video(self):
        self.split_video_into_segments()
        self.apply_watermark()
        self.concatenate_segments()
        self.clean_up()


if __name__ == "__main__":
    input_file = "00x. G Descent.mp4"
    watermark_text = "+91 9577297546"
    font_file = r"C\:\\Windows\\Fonts\\arial.ttf"

    watermarker = VideoWatermarker(input_file, watermark_text, font_file)
    watermarker.process_video()
