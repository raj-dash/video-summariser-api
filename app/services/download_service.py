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
            "quiet": False,  # Set to True if you want to hide the terminal progress bar
        }

        ydl_opts.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        )

        try:
            print(f"Starting download for: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("Download completed successfully!")

        except Exception as e:
            print(f"An error occurred during download: {e}")


if __name__ == "__main__":
    obj = DownloadService()
    url = "https://www.youtube.com/watch?v=g291trLaqTA"
    obj.download_video(url=url)
