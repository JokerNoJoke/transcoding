import os
import subprocess

ffmpeg_path = os.path.join("ffmpeg-7.1", "bin", "ffmpeg").replace(os.sep, "/")


def transcoding_video_to_dash(input_file: str, output_dir: str) -> str:
    """
    Transcode video to DASH format with multiple resolutions using FFmpeg.

    Args:
        input_file: Path to input video file
        output_dir: Directory to store output files

    Returns:
        str: Path to the generated DASH manifest file

    Raises:
        Exception: If FFmpeg transcoding fails
    """
    # Prepare output path
    manifest_path = os.path.join(output_dir, "manifest.mpd").replace(os.sep, "/")

    # Build FFmpeg command with optimal settings for different resolutions
    cmd = [
        ffmpeg_path,
        "-i",
        input_file,
        # "-vf scale=-2:1080 -c:a copy -c:v libx264 -b:v 5M -map 0:v:0",
        # "-vf scale=-2:720 -c:a copy -c:v libx264 -b:v 2.5M -map 0:v:0",
        "-vf scale=-2:480 -c:a copy -c:v libx264 -b:v 1M -map 0:a:0 -map 0:v:0",
        "-f dash -seg_duration 4",
        manifest_path,
    ]

    try:
        # Execute FFmpeg
        subprocess.run(cmd, check=True, capture_output=True)

        print(f"Transcoding completed. Manifest file saved at: {manifest_path}")
        return manifest_path

    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg transcoding failed: {e.stderr.decode()}")
    except Exception as e:
        raise Exception(f"Error during transcoding: {str(e)}")
