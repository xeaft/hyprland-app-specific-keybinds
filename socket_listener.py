import os
import sys
import socket

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

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    sock.connect(socket_path)
    print("connected to hyprland socket2")

    while True:
        data = sock.recv(4096)
        if not data:
            print("sock closed")
            break

        print(f"data: {data}");

except:
    pass
finally:
    sock.close()
