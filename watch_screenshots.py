print("🚀 Script started")

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ocr_utils import extract_text
from llm_utils import summarize_text

SCREENSHOT_DIR = r"C:\Users\shiva\OneDrive\Pictures\Screenshots"

processed_files = set()  # ✅ prevents infinite loop


class ScreenshotHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return

        if not event.src_path.lower().endswith((".png", ".jpg", ".jpeg")):
            return

        # ✅ Ignore already processed screenshots
        if event.src_path in processed_files:
            return

        print(f"\n📸 New Screenshot Detected: {event.src_path}")

        # wait until file is fully written
        time.sleep(2)

        processed_files.add(event.src_path)

        text = extract_text(event.src_path)
        print("\n📝 OCR TEXT (first 500 chars):\n", text[:500])

        summary = summarize_text(text)
        print("\n📌 SUMMARY:\n", summary)
        print("\n" + "=" * 80)


if __name__ == "__main__":
    print("📁 Watching folder:", SCREENSHOT_DIR)
    print("📂 Folder exists:", os.path.exists(SCREENSHOT_DIR))

    if not os.path.exists(SCREENSHOT_DIR):
        print("❌ Screenshot folder does NOT exist")
        exit(1)

    observer = Observer()
    observer.schedule(ScreenshotHandler(), SCREENSHOT_DIR, recursive=False)
    observer.start()

    print("👀 Waiting for screenshots...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
