import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ocr_utils import extract_text
from llm_utils import summarize_text

SCREENSHOT_DIR = r"C:\Users\shiva\OneDrive\Pictures\Screenshots"

class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        if not event.src_path.lower().endswith((".png", ".jpg", ".jpeg")):
            return

        print(f"\n📸 New Screenshot Detected: {event.src_path}")

        text = extract_text(event.src_path)
        print("\n📝 Extracted Text (OCR):\n", text[:500], "...")

        summary = summarize_text(text)
        print("\n📌 SUMMARY:\n", summary)
        print("\n" + "="*80)

if __name__ == "__main__":
    print("👀 Watching for new screenshots...")
    observer = Observer()
    observer.schedule(ScreenshotHandler(), SCREENSHOT_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
