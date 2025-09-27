import cv2
from PIL import Image
import os
import time

# Simple ASCII character set from sparse to dense (original set)
ASCII_CHARS = '@%#*+=-:. '

def get_ascii_char(pixel_brightness, max_brightness=255):
    """Maps a pixel's brightness (0-255) to an ASCII character."""
    
    # Invert the brightness and map it to the index (dark pixels -> dense chars)
    inverted_brightness = max_brightness - pixel_brightness
    index = int((inverted_brightness / max_brightness) * len(ASCII_CHARS))
    index = min(index, len(ASCII_CHARS) - 1)
    
    return ASCII_CHARS[index]


def frame_to_ascii(frame, new_width=100):
    """Converts a single video frame to an ASCII string."""
    
    # 1. Convert OpenCV frame (NumPy array) to PIL Image
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    # 2. Resize and Maintain Aspect Ratio
    width, height = img.size
    aspect_ratio = height / width
    # Use 0.5 to compensate for terminal character height
    new_height = int(new_width * aspect_ratio * 0.5) 
    
    img = img.resize((new_width, new_height))
    
    # 3. Convert to Grayscale
    img = img.convert('L')
    
    # 4. Generate ASCII string
    pixels = img.getdata()
    ascii_frame = "".join([get_ascii_char(pixel) for pixel in pixels])
    
    # 5. Add Newlines to form the frame's rows
    return "\n".join([ascii_frame[i:i + new_width] 
                      for i in range(0, len(ascii_frame), new_width)])


def play_video_as_ascii(video_path, width=100):
    """Reads a video and plays it, timing the frame rate to match the original video's FPS."""
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return

    # --- 🔑 Get Original FPS and Calculate Target Delay ---
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        print("Warning: Could not determine video FPS. Defaulting to 20 FPS.")
        delay = 0.05
    else:
        # The time (in seconds) that each frame should take
        delay = 1 / fps

    print(f"--- Playing video: {video_path} at {fps:.2f} FPS ---")
    print(f"--- ASCII Width: {width} | Target delay per frame: {delay*1000:.2f} ms ---")

    while cap.isOpened():
        # Record the start time of processing the current frame
        frame_start_time = time.time()
        
        # Read a new frame
        ret, frame = cap.read()
        
        if not ret:
            break

        # Convert the frame to ASCII
        ascii_output = frame_to_ascii(frame, width)

        # Clear the terminal screen and print the ASCII frame
        os.system('cls' if os.name == 'nt' else 'clear') 
        print(ascii_output)

        # --- FPS Timing Logic ---
        # 1. Calculate the actual time spent processing and drawing the frame
        time_spent = time.time() - frame_start_time
        
        # 2. Calculate the time remaining to meet the target delay
        time_to_wait = delay - time_spent
        
        # 3. Pause only if processing was faster than the target delay
        if time_to_wait > 0:
            time.sleep(time_to_wait)
        # ------------------------

    cap.release()
    cv2.destroyAllWindows()
    print("\n--- Video playback finished ---")


if __name__ == "__main__":
    VIDEO_FILE = 'Video.mp4' 
    ASCII_WIDTH = 120   
    play_video_as_ascii(VIDEO_FILE, ASCII_WIDTH)