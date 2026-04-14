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

    def image(self, img):
        """
        Display a PIL Image on the framebuffer.
        Converts to RGB565 format and writes directly to framebuffer.

        Args:
            img: PIL Image object (will be resized if needed)
        """
        s1 = datetime.now()
        # Resize if necessary
        if img.size != (self.width, self.height):
            img = img.resize((self.width, self.height), Image.LANCZOS)

        # Convert to RGB if not already
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Convert PIL Image to numpy array (height x width x 3)
        rgb_array = np.array(img, dtype=np.uint8)

        # Extract R, G, B channels
        r = rgb_array[:, :, 0].astype(np.uint16)
        g = rgb_array[:, :, 1].astype(np.uint16)
        b = rgb_array[:, :, 2].astype(np.uint16)

        # Convert to RGB565 using vectorized operations
        rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

        # Convert to little-endian bytes
        fb_data = rgb565.astype('<u2').tobytes()

        print(f"logic took {datetime.now() - s1}")

        s = datetime.now()
        # Write to framebuffer
        self.fb_mmap.seek(0)

        self.fb_mmap.write(fb_data)
        print(f"write took {datetime.now() - s}")

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


def make_left_eye_display(fb_device='/dev/fb2'):
    """
    Create a framebuffer display for the left eye.

    Args:
        fb_device: Path to framebuffer device (default: '/dev/fb0')

    Returns:
        FramebufferDisplay instance
    """
    return FramebufferDisplay(fb_device, width=240, height=240)


def make_right_eye_display(fb_device='/dev/fb1'):
    """
    Create a framebuffer display for the right eye.

    Args:
        fb_device: Path to framebuffer device (default: '/dev/fb1')

    Returns:
        FramebufferDisplay instance
    """
    return FramebufferDisplay(fb_device, width=240, height=240)
