# Video Watermarker

This Python script applies a watermark to a video by splitting it into segments, watermarking each segment with a random position, and then concatenating the segments back together. The watermarking process is performed using `FFmpeg`, and the script is designed using an object-oriented approach for maintainability and reusability.

## Features

- Splits a video into segments of random duration.
- Applies a watermark with random positions to each segment. (change position every 5 seconds for 5 second hold within each segment)
- Concatenates the watermarked segments into a final output video.
- Cleans up temporary files after processing.

## Requirements

- Python 3.10 or higher.
- `FFmpeg` installed and added to your system's PATH.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/FireIndex/MicroProjects.git
   ```
2. Navigate to the project directory:

   ```bash
   cd MicroProjects
   cd video-watermarker
   ```

3. Install the required Python libraries (if needed):
   ```bash
   pip install subprocess os random
   ```

## Usage

1. Place the video file you want to watermark in the project directory.

2. Edit the `main.py` file (or run the script directly if using `__main__`):

   ```python
   if __name__ == "__main__":
       input_file = "video.mp4"  # Path to your video file
       watermark_text = "+91 9540297546"  # Text to use as the watermark
       font_file = r"C\:\\Windows\\Fonts\\arial.ttf"  # Path to the font file

       watermarker = VideoWatermarker(input_file, watermark_text, font_file)
       watermarker.process_video()
   ```

3. Run the script:

   ```bash
   python main.py
   ```

4. The watermarked video will be saved as `video_BigW.mp4` in the project directory.

## How It Works

1. **Splitting the Video**:

   - The video is split into segments of random duration (between 4 and 7 seconds) for faster processing and to avoid memory issues with large files.

2. **Applying the Watermark**:

   - Each segment is watermarked using a random position for the watermark text. The position is recalculated every 5 seconds within each segment.

3. **Concatenating Segments**:

   - The watermarked segments are concatenated into a single output video.

4. **Cleanup**:
   - Temporary segment files and intermediate watermarked files are deleted after processing.

## Customization

- **Watermark Text**: Change the `watermark_text` variable in the `main.py` file.
- **Font File**: Update the `font_file` variable to use a different font.
- **Font Size, Color, Frame Rate and Threads**: These can be adjusted in the `VideoWatermarker` class during instantiation.

## License

This project is licensed under the MIT License. See the [LICENSE] file for details.
