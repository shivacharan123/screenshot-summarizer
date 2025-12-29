import pyautogui
from datetime import datetime
import os

# Create screenshots folder if it doesn't exist
os.makedirs("screenshots", exist_ok=True)

# Take screenshot
screenshot = pyautogui.screenshot()

# Save as latest.png
file_path = os.path.join("screenshots", "latest.png")
screenshot.save(file_path)

print(f"Screenshot saved at: {file_path}")
