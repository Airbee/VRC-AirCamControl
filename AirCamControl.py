import customtkinter as ctk
import threading
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

root = ctk.CTk()
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

root.geometry("300x200")
root.title("AirCamControl")

# Variables

ApertureMin = 1.4
ApertureMax = 32
ApertureMinSlider = 1.4
ApertureMaxSlider = 32
ApertureValue = 0

FocalDistMin = 0
FocalDistMax = 10
FocalDistMinSlider = 0
FocalDistMaxSlider = 10
FocalDistValue = 0

ZoomMin = 20
ZoomMax = 300
ZoomMinSlider = 20
ZoomMaxSlider = 300
ZoomValue = 0




# --------------------------
# OSC Settings
# --------------------------
OSC_IP = "127.0.0.1"
OSC_PORT = 9000
OSC_PORT_RECEIVE = 9001
client = SimpleUDPClient(OSC_IP, OSC_PORT)

def osc_callback(address, *args):
    global ApertureMax, ApertureMin, ApertureMinSlider, ApertureMaxSlider, ApertureValue
    global FocalDistMax, FocalDistMin, FocalDistMinSlider, FocalDistMaxSlider, FocalDistValue
    global ZoomMax, ZoomMin, ZoomMinSlider, ZoomMaxSlider, ZoomValue

    if address == "/avatar/parameters/AirCCApMax" and args:
        ApertureMaxSlider = ApertureMin + ((ApertureMax - ApertureMin) * args[0])
        log_message(f"Aperture Max set to {ApertureMaxSlider}")

    if address == "/avatar/parameters/AirCCApMin" and args:
        ApertureMinSlider = ApertureMin + ((ApertureMax - ApertureMin) * args[0])
        log_message(f"Aperture Min set to {ApertureMinSlider}")

    if address == "/avatar/parameters/AirCCApValue" and args:
        ApertureValue = ApertureMinSlider + ((ApertureMaxSlider - ApertureMinSlider) * args[0])
        client.send_message("/usercamera/Aperture", ApertureValue)
        log_message(f"Aperture Value set to {ApertureValue}")



    if address == "/avatar/parameters/AirCCFocDisMax" and args:
        FocalDistMaxSlider = FocalDistMin + ((FocalDistMax - FocalDistMin) * args[0])
        log_message(f"Focal Distance Max set to {FocalDistMaxSlider}")
    
    if address == "/avatar/parameters/AirCCFocDisMin" and args:
        FocalDistMinSlider = FocalDistMin + ((FocalDistMax - FocalDistMin) * args[0])
        log_message(f"Focal Distance min set to {FocalDistMinSlider}")
    
    if address == "/avatar/parameters/AirCCFocDisValue" and args:
        FocalDistValue = FocalDistMinSlider + ((FocalDistMaxSlider - FocalDistMinSlider) * args[0])
        client.send_message("/usercamera/FocalDistance", FocalDistValue)
        log_message(f"Focal Distance Value set to {FocalDistValue}")
    


    if address == "/avatar/parameters/AirCCZoomMax" and args:
        ZoomMaxSlider = ZoomMin + ((ZoomMax - ZoomMin) * args[0])
        log_message(f"Zoom Max set to {ZoomMaxSlider}")

    if address == "/avatar/parameters/AirCCZoomMin" and args:
        ZoomMinSlider = ZoomMin + ((ZoomMax - ZoomMin) * args[0])
        log_message(f"Zoom Min set to {ZoomMinSlider}")

    if address == "/avatar/parameters/AirCCZoomValue" and args:
        ZoomValue = ZoomMinSlider + ((ZoomMaxSlider - ZoomMinSlider) * args[0])
        client.send_message("/usercamera/Zoom", ZoomValue)
        log_message(f"Zoom Value set to {ZoomValue}")
    

    # print(f"Received OSC message: {address} with arguments: {args}")

 
def start_osc_server():
    dispatcher = Dispatcher()
    dispatcher.map("/*", osc_callback)
    server = osc_server.ThreadingOSCUDPServer((OSC_IP, OSC_PORT_RECEIVE), dispatcher)
    server.serve_forever()

def start_osc_server_thread():
    threading.Thread(target=start_osc_server, daemon=True).start()


log_textbox = None

def log_message(msg):
    print(msg)
    if log_textbox:
        log_textbox.insert("end", msg + "\n")
        log_textbox.see("end")


# --------------------------
# UI
# --------------------------
log_textbox = ctk.CTkTextbox(master=root, width=300)
log_textbox.pack(expand=True)
log_textbox.insert("end", "AirCamControl running..." + "\n")
log_textbox.insert("end", "This window will display logs..." + "\n")


if __name__ == "__main__":
    start_osc_server_thread()
    root.mainloop()
    
