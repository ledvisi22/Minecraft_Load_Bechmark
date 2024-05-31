import time
import subprocess
from pynput import mouse
import psutil

def get_front_window_title():
    script = 'název_okna.applescript'
    result = subprocess.run(['osascript', script], capture_output=True, text=True)
    return result.stdout.strip()

def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        return False  # Stop listener

def get_cpu_ram_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    return cpu_usage, ram_usage

def main():
    print("VAROVANI: Ihned po vypsani verze do loadingu!")
    ver = input("Minecraft version (example: 1.20.6): ")

    # Wait for left mouse click
    print("Waiting for left mouse click...")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    # Measure time to find Minecraft window
    start = time.time()
    target_window_title = f"Minecraft {ver} - Singleplayer"
    print(f"Looking for window titled '{target_window_title}'...")

    while True:
        current_window_title = get_front_window_title()
        if target_window_title in current_window_title:
            break
        cpu_usage, ram_usage = get_cpu_ram_usage()
        print(f"CPU Usage: {cpu_usage}%, RAM Usage: {ram_usage}%")
        time.sleep(1)

    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")
    print("Done")

if __name__ == "__main__":
    main()
