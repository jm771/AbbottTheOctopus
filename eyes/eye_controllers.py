
import busio
import digitalio
from board import SCK, SCK_1, MOSI, MOSI_1, D25, D8, D27, D16, D26, D6


from adafruit_rgb_display.gc9a01a import GC9A01A

def make_left_eye_display():
    # Configuration for CS and DC pins:
    CS_PIN = D8
    DC_PIN = D25
    RST_PIN = D27

    spi = busio.SPI(clock=SCK, MOSI=MOSI)#, baudrate=10_000_000)

    display = GC9A01A(spi, cs=digitalio.DigitalInOut(CS_PIN),
                            dc=digitalio.DigitalInOut(DC_PIN), rst=digitalio.DigitalInOut(RST_PIN))
    
    return display

def make_right_eye_display():
    # Configuration for CS and DC pins:
    CS_PIN = D16
    DC_PIN = D26
    RST_PIN = D6

    spi = busio.SPI(clock=SCK_1, MOSI=MOSI_1)
    display = GC9A01A(spi, cs=digitalio.DigitalInOut(CS_PIN),
                            dc=digitalio.DigitalInOut(DC_PIN), rst=digitalio.DigitalInOut(RST_PIN))
    
    return display
