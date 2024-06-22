
![Logo](https://raw.githubusercontent.com/DKNS-JCC/LCDeej/main/icon.ico)


# LCDeej

Control your audio sessions with the spin of a Wheel!

LCDeej is an enhanced version of the [Deej app](https://github.com/omriharel/deej) developed by omriharel, now with an added LCD screen for Arduino. This feature transforms your setup into a multimedia hub, displaying song titles and authors. The application is also built using Python.

## Features

- **LCD Power Management:** Automatic LCD power-off after a set time to save energy.
- **Customizable Code:** Fully commented and easy to modify to fit your specific needs.
- **Efficient Resource Usage:** Optimized to run with minimal system resources.
- **Windows Support:** Compatible with Windows 10 and later versions.

## Build Your Own

### Materials Needed:
- **Arduino Nano or Similar:** Compatible with Chinese replicas.
- **4 x 10k Potentiometers**
- **16x2 LCD Screen:** Optimized for I2C communication.
- **A Computer**
- **Assorted Jumper Wires**

### Instructions for Assembling the Potentiometers

![Image](https://raw.githubusercontent.com/DKNS-JCC/LCDeej/main/Sketch.png) 

1. **Prepare the Potentiometers:**
   - Gather your four 10k potentiometers.
   - Identify the three pins on each potentiometer: the two outer pins are for VCC (power) and GND (ground), and the middle pin is for the analog signal.

2. **Connect to Arduino:**
   - Connect one outer pin of each potentiometer to the 5V pin on the Arduino.
   - Connect the other outer pin of each potentiometer to a common GND on the Arduino.

3. **Connect the Signal Pins:**
   - Connect the middle pin of each potentiometer to the following analog input pins on the Arduino:
     - Potentiometer 1 to A0
     - Potentiometer 2 to A1
     - Potentiometer 3 to A2
     - Potentiometer 4 to A3

4. **Verify Connections:**
   - Double-check all connections to ensure they are secure and correct.
   - Ensure there are no short circuits or loose wires (Nanos tend to die)

        
## Installation

For new users without python and pip:
Download and install python3.9 https://www.python.org/downloads/

```bash
        python --version
        pip --version

```
If you already have python installed:
```bash
        pip install -r requirements.txt
```
Now lets flash our Arduino board:
```bash
        open own_dej.ino -> Verify -> Upload
```
Modify line COM_PORT = COMX to your own port and run:
```bash
        python3.9 deej.py
```

or run .exe on releases.
    
## Authors

- [dkns-jcc](https://www.github.com/dkns-jcc)


## FAQ

#### It stopped detecting my Arduino Board

First close running app, then reconnect arduino and restart app

#### App stopped working

Rebooting your PC fixes almost everything, open an issue if it is still happening 


## Used tech

**Client:** Python 

**Server:** C++


## License

[Licenced by MIT](https://choosealicense.com/licenses/mit/)

