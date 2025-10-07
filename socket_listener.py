import os
import sys
import socket

EVENT_WINDOW_FOCUSED = "activewindow"

hypr_inst_signature = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE", None)

if (hypr_inst_signature is None):
    print("HIS not found")
    sys.exit(1)
    
xdg_runtime_dir = os.environ.get("XDG_RUNTIME_DIR", None)
if (xdg_runtime_dir is None):
    print("XDG Runtime Dir not set.")
    sys.exit(2)

socket_path = os.path.join(xdg_runtime_dir, "hypr", hypr_inst_signature, ".socket2.sock")

if not os.path.exists(socket_path):
    print("Socket doesnt exist (what?)")
    sys.exit(3)

app_keybinds = []
def create_socket(keybinds):
    global app_keybinds
    app_keybinds = keybinds

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        sock.connect(socket_path)
        print("connected to hyprland socket2")

        while True:
            data = sock.recv(4096)
            if not data:
                print("sock closed")
                break

            on_event(data)
    except Exception as e:
        print("error. sad: ", e)
    finally:
        sock.close()

def add_keybind(keybind_event) -> None:
    cmd = keybind_event.to_command()
    print(cmd)
    os.system(cmd)
    keybind_event.active = True

def remove_keybind(keybind_event):
    os.system(keybind_event.to_command(True))
    keybind_event.active = False

def on_event(event_text : bytes):
    event : str = event_text.decode().strip()
    events = event.split("\n")

    for ev in events:
        event_type, event_data = ev.split(">>")

        if (event_type != EVENT_WINDOW_FOCUSED):
            continue

        window_class = event_data.split(",")[0]
        print(f"Window focused: {window_class}")
        for keyb in app_keybinds:
            if keyb.winclass == window_class:
                add_keybind(keyb)
                continue
            if keyb.active:
                remove_keybind(keyb)

