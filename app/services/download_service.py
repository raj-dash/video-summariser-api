import os
import yt_dlp


class DownloadService:
    def __init__(self):
        self.output_path = "app/downloads"
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def download_video(self, url: str):
        ydl_opts = {
            "outtmpl": os.path.join(self.output_path, "%(title)s.%(ext)s"),
            "quiet": False,
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        try:
            print(f"Starting download for: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 1. extract_info performs the full download and FFmpeg conversion
                info_dict = ydl.extract_info(url, download=True)

                # 2. Extract the true final absolute path of the generated file
                # yt-dlp tracks all generated files in the 'requested_downloads' list
                if (
                    "requested_downloads" in info_dict
                    and info_dict["requested_downloads"]
                ):
                    downloaded_path = info_dict["requested_downloads"][0].get(
                        "filepath"
                    )
                else:
                    # Fallback approach if requested_downloads isn't populated
                    downloaded_path = ydl.prepare_filename(info_dict)
                    if downloaded_path.endswith(
                        (".webm", ".m4a", ".mp4", ".3gp", ".flv")
                    ):
                        downloaded_path = os.path.splitext(downloaded_path)[0] + ".mp3"

            if not downloaded_path or not os.path.exists(downloaded_path):
                raise FileNotFoundError(
                    f"Could not verify the downloaded file path on disk."
                )

            print(f"Download completed successfully! Saved to: {downloaded_path}")
            return str(downloaded_path)

        except Exception as e:
            print(f"An error occurred during download: {e}")
            raise e


if __name__ == "__main__":
    obj = DownloadService()
    url = "https://www.youtube.com/watch?v=g291trLaqTA"
    path = obj.download_video(url=url)
    print(path)
