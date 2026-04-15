"""
Framebuffer-based eye display controllers.
This version uses Linux framebuffer devices instead of direct SPI communication.
Requires the gc9a01-configurable overlay to be loaded and configured.
"""

from datetime import datetime

from PIL import Image
import mmap
import struct
import os
import numpy as np

class FramebufferDisplay:
    """
    A display class that mimics the Adafruit GC9A01A interface but writes to a framebuffer device.
    """
    def __init__(self, fb_device, width=240, height=240):
        """
        Initialize framebuffer display.

        Args:
            fb_device: Path to framebuffer device (e.g., '/dev/fb0', '/dev/fb1')
            width: Display width in pixels
            height: Display height in pixels
        """
        self.fb_device = fb_device
        self.width = width
        self.height = height

        # Open framebuffer device
        self.fb_fd = os.open(fb_device, os.O_RDWR)

        # Calculate framebuffer size (RGB565 = 2 bytes per pixel)
        self.fb_size = width * height * 2

        # Memory map the framebuffer
        self.fb_mmap = mmap.mmap(self.fb_fd, self.fb_size,
                                  mmap.MAP_SHARED,
                                  mmap.PROT_READ | mmap.PROT_WRITE)

    def image(self, img, offset_x=0, offset_y=0):
        """
        Display a PIL Image on the framebuffer.
        Only updates the pixels covered by the image at the given offset.

        Args:
            img: PIL Image object (any size)
            offset_x: X offset in pixels (default: 0)
            offset_y: Y offset in pixels (default: 0)
        """
        s1 = datetime.now()

        # Convert to RGB if not already
        if img.mode != 'RGB':
            img = img.convert('RGB')

        img_width, img_height = img.size

        # Convert PIL Image to numpy array (height x width x 3)
        rgb_array = np.array(img, dtype=np.uint8)

        # Extract R, G, B channels
        r = rgb_array[:, :, 0].astype(np.uint16)
        g = rgb_array[:, :, 1].astype(np.uint16)
        b = rgb_array[:, :, 2].astype(np.uint16)

        # Convert to RGB565 using vectorized operations
        img_rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

        # Calculate bounds (clip to display size)
        x_start = max(0, offset_x)
        y_start = max(0, offset_y)
        x_end = min(offset_x + img_width, self.width)
        y_end = min(offset_y + img_height, self.height)

        # Check if image is within bounds
        if x_start >= self.width or y_start >= self.height or x_end <= 0 or y_end <= 0:
            return  # Image is completely out of bounds

        # Calculate source region from image (handle negative offsets)
        src_x_start = max(0, -offset_x)
        src_y_start = max(0, -offset_y)
        src_x_end = src_x_start + (x_end - x_start)
        src_y_end = src_y_start + (y_end - y_start)

        # Extract the region to write
        region_rgb565 = img_rgb565[src_y_start:src_y_end, src_x_start:src_x_end]

        # Write each row to the framebuffer at the correct position
        bytes_per_pixel = 2
        row_bytes = (x_end - x_start) * bytes_per_pixel

        for row_idx, fb_y in enumerate(range(y_start, y_end)):
            # Calculate framebuffer offset for this row
            fb_offset = (fb_y * self.width + x_start) * bytes_per_pixel

            # Convert row to bytes
            row_data = region_rgb565[row_idx].astype('<u2').tobytes()

            # Write this row to framebuffer
            self.fb_mmap.seek(fb_offset)
            self.fb_mmap.write(row_data)

        # print(f"logic took {datetime.now() - s1}")

    def fill(self, color=0):
        """
        Fill the entire display with a single color.

        Args:
            color: RGB565 color value (16-bit integer) or RGB tuple
        """
        if isinstance(color, tuple):
            # Convert RGB tuple to RGB565
            r, g, b = color
            color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

        # Fill buffer with color
        fb_data = struct.pack('<H', color) * (self.width * self.height)

        # Write to framebuffer
        self.fb_mmap.seek(0)
        self.fb_mmap.write(fb_data)

    def close(self):
        """Clean up resources."""
        if hasattr(self, 'fb_mmap'):
            self.fb_mmap.close()
        if hasattr(self, 'fb_fd'):
            os.close(self.fb_fd)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class StubDisplay:
    """No-op display for running without hardware."""
    def image(self, img, offset_x=0, offset_y=0):
        pass

    def fill(self, color=0):
        pass

    def close(self):
        pass


def make_left_eye_display(fb_device='/dev/fb2'):
    try:
        return FramebufferDisplay(fb_device, width=240, height=240)
    except (FileNotFoundError, OSError):
        print(f"No framebuffer at {fb_device}, using stub left eye display")
        return StubDisplay()


def make_right_eye_display(fb_device='/dev/fb1'):
    try:
        return FramebufferDisplay(fb_device, width=240, height=240)
    except (FileNotFoundError, OSError):
        print(f"No framebuffer at {fb_device}, using stub right eye display")
        return StubDisplay()
