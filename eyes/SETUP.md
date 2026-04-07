Make sure SPI is turned on (pi logo, preferences, control center)
Follow install instructions at: https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display/tree/main

(If running on current machine, make sure the env is activated)

python sample_image.py

To support the second eye - need to enable spi1 peripheral

add this 

dtoverlay=spi1-1cs

to this:
/boot/firmware/config.txt


## Wiring:
### Left Eye

<table>
    <thead>
        <tr>
            <td>LCD Label</td><td>GPIO Name</td><td>Raspberry Pi Zero 2 physical pin</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>VCC</td><td>3.3V</td><td>1</td>
        </tr>
        <tr>
            <td>GND</td><td>GND</td><td>6</td>
        </tr>
        <tr>
            <td>SDA (MOSI)</td><td>10 (spi0 MOSI)</td><td>19</td>
        </tr>
        <tr>
            <td>SCL (CLK)</td><td>11 (spi0 SCLK)</td><td>23</td>
        </tr>
        <tr>
            <td>CS</td><td>8 (spi0 CE0)</td><td>24</td>
        </tr>
        <tr>
            <td>DC (Data/Command)</td><td>25</td><td>22</td>
        </tr>
        <tr>
            <td>RST (Reset)</td><td>27</td><td>13</td>
        </tr>
    </tbody>
</table>

## Wiring:
### Right Eye

<table>
    <thead>
        <tr>
            <td>LCD Label</td><td>GPIO Name</td><td>Raspberry Pi Zero 2 physical pin</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>VCC</td><td>3.3V</td><td>17</td>
        </tr>
        <tr>
            <td>GND</td><td>GND</td><td>20</td>
        </tr>
        <tr>
            <td>SDA (MOSI)</td><td>20 (spi1 MOSI)</td><td>38</td>
        </tr>
        <tr>
            <td>SCL (CLK)</td><td>21 (spi1 SCLK)</td><td>40</td>
        </tr>
        <tr>
            <td>CS</td><td>16 (spi1 CE2)</td><td>36</td>
        </tr>
        <tr>
            <td>DC (Data/Command)</td><td>26</td><td>37</td>
        </tr>
        <tr>
            <td>RST (Reset)</td><td>6</td><td>31</td>
        </tr>
    </tbody>
</table>