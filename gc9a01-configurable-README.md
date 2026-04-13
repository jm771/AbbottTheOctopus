# GC9A01 Configurable Overlay

This is a modified version of the GC9A01 display overlay that allows configurable GPIO pins.

## Compilation

Compile the overlay:
```bash
dtc -@ -I dts -O dtb -o gc9a01-configurable.dtbo gc9a01-configurable.dts
```

Install it:
```bash
sudo cp gc9a01-configurable.dtbo /boot/overlays/
# Or on newer systems:
sudo cp gc9a01-configurable.dtbo /boot/firmware/overlays/
```

## Usage

### Default Configuration (same as original)

Add to `/boot/config.txt` (or `/boot/firmware/config.txt`):
```
dtoverlay=gc9a01-configurable
```

Default pins:
- DC (Data/Command): GPIO 25
- RST (Reset): GPIO 27
- LED (Backlight): GPIO 18

### Custom GPIO Pins

```
dtoverlay=gc9a01-configurable,dc_gpio=24,reset_gpio=23,led_gpio=12
```

### Disable Backlight Control

To disable the backlight GPIO entirely (useful if you have always-on backlight or external control):
```
dtoverlay=gc9a01-configurable,led_gpio=255
```

Setting `led_gpio=255` removes the `led-gpios` property from the device tree, effectively disabling it.

### All Available Parameters

```
dtoverlay=gc9a01-configurable,param=value
```

**SPI Interface Selection:**
- `spi` - SPI interface to use: 0=SPI0 (default), 1=SPI1

**Display Parameters:**
- `speed` - SPI bus speed (default: 40000000)
- `rotate` - Display rotation: 0, 90, 180, 270 (default: 0)
- `width` - Display width in pixels (default: 240)
- `height` - Display height in pixels (default: 240)
- `fps` - Frame rate (default: 50)
- `debug` - Debug level 0-7 (default: 0)

**GPIO Parameters:**
- `dc_gpio` - Data/Command GPIO pin (default: 25)
- `reset_gpio` - Reset GPIO pin (default: 27)
- `led_gpio` - Backlight GPIO pin (default: 18, use 255 to disable)

**Polarity Parameters:**
- `dc_polarity` - DC pin polarity: 0=active high, 1=active low (default: 0)
- `reset_polarity` - Reset pin polarity: 0=active high, 1=active low (default: 1)
- `led_polarity` - LED pin polarity: 0=active high, 1=active low (default: 0)

## Examples

### Example 1: Two displays on SPI0 and SPI1
```
# In /boot/config.txt:

# Left eye on SPI0 (default)
dtoverlay=gc9a01-configurable,dc_gpio=25,reset_gpio=27,led_gpio=255

# Right eye on SPI1 with different GPIOs
dtoverlay=gc9a01-configurable,spi=1,dc_gpio=26,reset_gpio=6,led_gpio=255
```
This creates `/dev/fb0` for the left eye and `/dev/fb1` for the right eye.

### Example 2: Different GPIO pins with backlight disabled
```
dtoverlay=gc9a01-configurable,dc_gpio=23,reset_gpio=24,led_gpio=255
```

### Example 3: Custom pins with 60 FPS and 90-degree rotation
```
dtoverlay=gc9a01-configurable,dc_gpio=22,reset_gpio=27,led_gpio=17,fps=60,rotate=90
```

### Example 4: Higher SPI speed on SPI1
```
dtoverlay=gc9a01-configurable,spi=1,dc_gpio=24,reset_gpio=25,led_gpio=12,speed=80000000
```

## Notes

- Make sure the GPIOs you choose are not already in use by other devices
- The SPI pins (MOSI, MISO, CLK, CS) remain on the standard SPI0 pins and cannot be changed through this overlay
- After editing `/boot/config.txt`, reboot for changes to take effect
- If the display doesn't work, try enabling debug output: `debug=7`
