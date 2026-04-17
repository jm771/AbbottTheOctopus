Install github cli
Clone the abbott repo
install vim (optional)

Follow instructions in gac... to install the SPI display overlay

Add this to /boot/firmware/config.txt

```
dtoverlay=spi1-1cs
dtoverlay=gc9a01-configurable,dc_gpio=25,reset_gpio=27,led_gpio=255,speed=40000000
dtoverlay=gc9a01-configurable,spi=1,dc_gpio=26,reset_gpio=6,led_gpio=255,speed=40000000
```
