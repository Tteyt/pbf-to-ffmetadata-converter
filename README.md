### Purpose

The script performs two main functions:

- Converts a chapter file from the .pbf format (used by PotPlayer) to the ffmetadata format supported by ffmpeg.
- Optionally embeds chapters into an .mp4 video file using ffmpeg.

### Requirements

- Python 3 installed.
- ffmpeg installed (must be available in PATH).

### Usage

1. Convert .pbf to ffmetadata

To simply convert a .pbf file to ffmetadata, run the following command:

`python convert_pbf_to_ffmetadata.py "input.pbf" "output.ffmetadata"`

input.pbf — Path to the .pbf file.
output.ffmetadata — Path to the output ffmetadata file.

2. Convert and Embed Chapters into a Video

To convert .pbf to ffmetadata and immediately embed the chapters into a video, use the --embed flag, and specify the video file and output file:

`python convert_pbf_to_ffmetadata.py "input.pbf" "output.ffmetadata" --embed --video "video.mp4" --output "video_output.mp4"`

    --embed — Flag indicating that chapters should be embedded into the video.
    --video — Path to the .mp4 video file.
    --output — Path to the output video file.

### Examples

Conversion Only:

`python convert_pbf_to_ffmetadata.py "chapters.pbf" "chapters.ffmetadata"`

Conversion and Embedding Chapters:

`python convert_pbf_to_ffmetadata.py "chapters.pbf" "chapters.ffmetadata" --embed --video "input.mp4" --output "output.mp4"`

Notes

- If ffmpeg is not installed or not available in PATH, the script will throw an error.
- If the .pbf file contains binary data, the script may not work. In this case, additional analysis of the file format will be required.
- You can manually modify metadata (e.g., title and artist) in the script code.
