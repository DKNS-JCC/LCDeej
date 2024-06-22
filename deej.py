
#Proyect developed by: DKNSJCC
#Date: 2024-06-24
#Time Spent: 2 hours

#Description: This script allows you to display the song title and artist on an LCD screen connected to an Arduino, 
#while controlling the volume of the system with a potentiometer connected to the Arduino. 
#The script uses the Windows Media Control API to get the song information and the PySerial library to communicate with the Arduino. 
#The script also uses the PyStray library to create a system tray icon that allows you to exit the script and run in background.


#Audio dependencies
from ctypes import cast, POINTER
import asyncio
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

#Arduino dependencies
import serial
import time

#icon dependencies
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading

COM_PORT = 'COM5' #Modify this to your COM port

exit_flag = 0
n1=n2=n3=n4=0


async def get_media_info(session):
    info = await session.try_get_media_properties_async()
    info_dict = {song_attr: getattr(info, song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
    info_dict['genres'] = list(info_dict['genres'])
    return info_dict

async def monitor_media_session():
    print("Media session monitoring started...")
    while True:
        try:
            sessions = await MediaManager.request_async() #deadlock aquí (SOLVED by PC restart)
            current_session = sessions.get_current_session()
            
            if current_session and current_session.source_app_user_model_id == "Spotify.exe":  # Modifica esto para tu reproductor de música
                old_title = info['title'] if 'info' in locals() else None
                info = await get_media_info(current_session)
                if info['title'] != old_title:
                    formatted_string = f"*{info['title']}*{info['artist']}"
                    print(formatted_string)
                    ser.write(formatted_string.encode('utf-8')) #fallo primera vez que se ejecuta 
                    time.sleep(0.5) #esperar a que el arduino procese la información (fallo de buffer en arduino)
            else:
                print("No media session found")
                break
                
            if exit_flag == 1:
                break

        except Exception as e:
            print(f"An error occurred while monitoring media session: {type(e)} {e} ")

        await asyncio.sleep(1)

    # Código de limpieza después de que exit_flag se establezca en True
    print("Exiting...")
    ser.close()
    print("Serial port closed. \nMonitor media session terminated.")
    
def scale_value(value, from_min, from_max, to_min, to_max):
    # Escalar el valor de una escala a otra
    scaled_value = (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min
    return scaled_value

def process_serial(data):
    try:
        if data.startswith('*'):
            return None, None, None, None
        values = list(map(int, data.strip().split('|')))
        if len(values) != 4:
            raise ValueError("The data must contain exactly four numbers")
        
        scaled_values = [scale_value(v, 0, 1023, 0, 100) for v in values]

        # Separar en variables
        n1, n2, n3, n4 = scaled_values
        return n1, n2, n3, n4
    except ValueError as e:
        print(f"Error processing data: {e}")
        return None, None, None, None

    
    
async def set_volume():
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
    from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize
    from ctypes import cast, POINTER
    
    print("Volume control started...")

    # Inicializar la librería COM
    CoInitialize()
    
    try:
        while not exit_flag:
            if ser.in_waiting > 0:
                # Leer una línea desde el puerto serial
                serial_data = ser.read_until("\n").decode('utf-8')
                print(f"Received: {serial_data.strip()}")
                global n1, n2, n3, n4
                n1, n2, n3, n4 = process_serial(serial_data)
                if None not in (n1, n2, n3, n4):
                    print(f"n1: {n1:.2f}, n2: {n2:.2f}, n3: {n3:.2f}, n4: {n4:.2f}")
                
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                if session.Process and session.Process.name().lower() == "spotify.exe":
                    volume = session.SimpleAudioVolume
                    if n2 is None:
                        volume.SetMasterVolume(1, None) #0 to 1.0 relative volume master
                    else:
                        volume.SetMasterVolume(n2/100, None)
                    print(f"Volume set to {n2:.2f}")

                elif session.Process and session.Process.name().lower() == "brave.exe":
                    volume = session.SimpleAudioVolume
                    if n3 is None:
                        volume.SetMasterVolume(1, None)
                    else:
                        volume.SetMasterVolume(n3/100, None)
                    print(f"Volume set to {n3:.2f}")
                    
                elif session.Process and session.Process.name().lower() == "discord.exe":
                    volume = session.SimpleAudioVolume
                    if n4 is None:
                        volume.SetMasterVolume(1, None)
                    else:
                        volume.SetMasterVolume(n4/100, None)
                    print(f"Volume set to {n4:.2f}")

            await asyncio.sleep(1)

    except Exception as e:
        print(f"An error occurred while setting volume: {type(e)} {e}")

    finally:
        # Desinicializar la librería COM
        CoUninitialize()
        
def run_volume_control():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(set_volume())
        
    
def start_icon():
    print("Icon started...")
    icon.run()

def exit_action(icon, item):
    global exit_flag
    icon.stop()
    exit_flag = 1  
    
#Main function
if __name__ == '__main__':
    
    flag = 0
    thread_count = 1
    
    image = Image.open("ico.png") #Change ico.png for custom icon  
    menu = (item('Salir', exit_action))
    icon = pystray.Icon("LCDeej", image, "LCDeej", menu=pystray.Menu(pystray.MenuItem("Salir", exit_action)))
    icon_thread = threading.Thread(target=start_icon)
    
    volume_thread = threading.Thread(target=run_volume_control)
    
    
    
    while flag == 0:
        try:
            ser= serial.Serial(COM_PORT, 9600,timeout=1) 
            icon_thread.start()
            volume_thread.start()
            asyncio.run(monitor_media_session())
            
        except KeyboardInterrupt:
            print("Monitoring stopped by user")
            icon.stop()
            exit_flag = 1
            break
        except Exception as e:
            print(f"No device detected in {COM_PORT} check connection: {e}")
            print("Retrying in 5 seconds... CTRL+C to stop")
            time.sleep(5)
        

