
-----

# ASCII Video Player 🎬 (FPS Synchronized)

A simple and efficient Python script that plays any local video file as high-clarity **ASCII art** directly in your terminal, with the playback speed synchronized to the original video's **Frames Per Second (FPS)**.

## Features ✨

  * **FPS Synchronization:** The playback speed (delay between frames) is automatically calculated and enforced to match the original video's FPS.
  * **High Clarity:** Uses an optimized character set and automatic contrast enhancement (`ImageOps.autocontrast`) to ensure the ASCII output is as clear as possible.
  * **Dynamic Resolution:** Supports customizable ASCII character width to maximize detail based on your terminal size.
  * **Cross-Platform:** Uses standard Python libraries compatible with Windows, macOS, and Linux.

## Requirements 🛠️

You need **Python 3** and the following libraries. The core functions rely on **OpenCV** for video handling and **Pillow** for image processing.

Install them using pip:

```bash
pip install opencv-python pillow numpy
```

## How to Run 🚀

1.  **Prepare Files:** Place your video file (e.g., `my_movie.mp4`) in the same directory as the Python script (**`ascii_video_player.py`**).

2.  **Edit Script:** Open **`ascii_video_player.py`** and modify the following line in the `if __name__ == "__main__":` block to match your video file's name:

    ```python
    VIDEO_FILE = 'my_movie.mp4' 
    ```

3.  **Adjust Width:** For the best results, maximize your terminal window and adjust the `ASCII_WIDTH` variable to the highest value that **does not** cause the text to wrap:

    ```python
    ASCII_WIDTH = 200  # Adjust this value (e.g., 150-300)
    ```

4.  **Execute:** Run the script from your terminal:

    ```bash
    python ascii_video_player.py
    ```

## How FPS Synchronization Works ⏱️

The script ensures consistent playback timing using the following steps for every frame:

1.  **Target Delay:** It reads the original video's FPS (e.g., 24 FPS) and calculates the exact time each frame *should* take: **`Target Delay = 1 / FPS`** ($\approx 0.0416$ seconds for 24 FPS).
2.  **Measure Processing Time:** It measures how long it takes to process the frame (read, convert to ASCII, and print to the terminal).
3.  **Pause:** It subtracts the processing time from the target delay. If the result is positive, it uses `time.sleep()` to pause for the remaining duration.

This guarantees that the total time taken for each frame equals the target delay, keeping the ASCII video speed identical to the source video.
