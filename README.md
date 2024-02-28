# alphazero - Digital Typewriter powered by Raspberry Pi Zero 2W
Digital Typewriter

This is an early version of the code, I still need to add comments and a few small features, but it does work.  To use a display other than the Waveshare 7in5, you will need a different file from Waveshare to replace epd7in5_V2.py and you'll need to adjust a few variables in the AlphaZero.py.  I'll make it more ubiquitus in the future.
## Hardware
- [Raspberry Pi Zero 2W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
- [7.5inch E-Ink display](https://www.waveshare.com/7.5inch-e-Paper-HAT.htm)
- [Lithium Ion Polymer Battery - 3.7v](https://www.adafruit.com/product/258)
- [PowerBoost 500 Charger](https://www.adafruit.com/product/1944) or the 1000. I used the 500 because the 1000 was out of stock.
- [Vortex Core 40% Keyboard](https://vortexgear.store/products/core) Any keyboard will do, but the code is customized to this keyboard, so if you go with a different one, then you will need to adjust the key_reader() function in main.py.
- Power button
- Cables to connect keyboard to pi, and to charge the device.
- I soldered a pin rack to the pi to make it easier to test things in the build, you can do the same or solder the wires from various things directly to the pi.
## Software
I will get something better written later.  For now, it is a python program, setup main.py to launch on start and make sure all the libraries on the top of the .py files in this repository are installed via pip.
## Wiring and component setup
TODO for later.
## 3D printed case
I haven't finished creating/editing the 3D models to print, but I will add them here once I do.  
## Special thanks to the [ZeroWriter1](https://github.com/zerowriter/zerowriter1)
I used your stuff as a starting point.  If you look at my code then you will realize that I basically started over and programmed it completely differently, but you were an inspiration.  I also borrowed your STLs :)
