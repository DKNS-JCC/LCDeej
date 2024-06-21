import asyncio
from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

import serial
import time

import pystray
from pystray import MenuItem as item
from PIL import Image
import threading

COM_PORT = 'COM5' #Modify this to your COM port

exit_flag = 0

async def get_media_info(session):
    info = await session.try_get_media_properties_async()
    info_dict = {song_attr: getattr(info, song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
    info_dict['genres'] = list(info_dict['genres'])
    return info_dict

async def monitor_media_session():
    print("Media session monitoring started...")
    while True:
        try:
            sessions = await MediaManager.request_async() #deadlock aquí (SOLVED by PC restart )
            current_session = sessions.get_current_session()
            
            if current_session and current_session.source_app_user_model_id == "Spotify.exe":  # Modifica esto para tu reproductor de música
                old_title = info['title'] if 'info' in locals() else None
                info = await get_media_info(current_session)
                if info['title'] != old_title:
                    formatted_string = f"*{info['title']}*{info['artist']}"
                    print(formatted_string)
                    ser.write(formatted_string.encode('utf-8')) #fallo primera vez que se ejecuta
            else:
                print("No active media session found")
            if exit_flag == 1:
                break

        except Exception as e:
            print(f"An error occurred while monitoring media session: {e}")

        await asyncio.sleep(1)

    # Código de limpieza después de que exit_flag se establezca en True
    print("Exiting...")
    ser.close()
    print("Serial port closed. \nMonitor media session terminated.")
        
def start_icon():
    icon.run()

def exit_action(icon, item):
    global exit_flag
    icon.stop()  # Detener el icono en la bandeja del sistema
    exit_flag = 1  # Establecer la bandera de salida
    
    
if __name__ == '__main__':
    flag = 0
    thread_count = 1
    image = Image.open("ico.png") #Change ico.png for custom icon  
    menu = (item('Salir', exit_action))
    icon = pystray.Icon("LCDeej", image, "LCDeej", menu=pystray.Menu(pystray.MenuItem("Salir", exit_action)))
    icon_thread = threading.Thread(target=start_icon)
    while flag == 0:
        try:
            if thread_count == 1:
                icon_thread.start()
                thread_count = 0
            ser= serial.Serial(COM_PORT, 9600,timeout=1) 
            flag = 1
            asyncio.run(monitor_media_session())
            
        except KeyboardInterrupt:
            print("Monitoring stopped by user")
            icon.stop()
            break
        except Exception as e:
            print(f"No device detected in {COM_PORT} check connection: {e}")
            print("Retrying in 5 seconds... CTRL+C to stop")
            time.sleep(5)
        

