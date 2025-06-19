import pyautogui
import time
import sys

# Check if a number argument was provided
if len(sys.argv) < 2:
    print("Please provide a number of times to paste as an argument")
    sys.exit(1)

try:
    # Get the number of times to paste from command line argument
    paste_count = int(sys.argv[1])

    # Give yourself a few seconds to switch to the target window
    time.sleep(5)

    # Repeat the paste operation the specified number of times
    for _ in range(paste_count):
        # Press Ctrl+V
        pyautogui.hotkey('ctrl', 'v')
        # Press Enter
        pyautogui.press('enter')
        # Small delay between pastes to prevent overwhelming the system
        time.sleep(0.1)

except ValueError:
    print("Please provide a valid number as an argument")