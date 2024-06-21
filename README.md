
![Logo](https://raw.githubusercontent.com/DKNS-JCC/LCDeej/main/icon.ico)


# LCDeej

An improvement for the deej app developed byomriharel.\
This version includes the implementation of an LCD screen for Arduino that support a multimedia hub displaying song title and autor \
Also built in Python. 



## Features

- LCD power off with time
- Fully customisable code with comments
- Low resource execution
- Windows support (10+) 


## Installation

For new users without python and pip:

```bash
  # Download and install python3.9 https://www.python.org/downloads/

    # Verify the install
        python --version
        pip --version

```
If you already have python installed:
```bash
    #Install required libs
        pip install -r requirements.txt
```
Now lets flash our Arduino board:
```bash
    #Install Arduino IDE or VSCode Extension and ensure COMX is free
        open own_dej.ino -> Verify -> Upload
```
Modify line COM_PORT = COMX to your own port and run:
```bash
    #Execute program
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

