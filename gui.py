from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import socket
import threading


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Work\AI Freind\Components\GUI\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1920x1080")
window.state("zoomed")
window.configure(bg="#F3F3F3")
window.title("INSERT NAME HERE")
HEADER = 2000000000
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.104"  # "ec2-13-41-72-251.eu-west-2.compute.amazonaws.com"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


###############################
def sending_message(event=None):
    msg = entry_1.get()
    if not msg:
        print("RETURNING")
        return
    # Send MSG to Server
    print("Sending")
    entry_1.delete(0, "end")
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(f"{msg}")
    pass


def threadGetField(event=None):
    my_thread = threading.Thread(target=sending_message())
    my_thread.start()


##############################

canvas = Canvas(
    window,
    bg="#F3F3F3",
    height=1080,
    width=1920,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvas.place(x=0, y=0)
canvas.create_rectangle(56.0, 0.0, 1901.0, 66.0, fill="#FFFFFF", outline="")

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat",
    bg="#FFFFFF",
)
button_1.place(x=65.0, y=6.0, width=60.0, height=60.0)

canvas.create_text(
    166.0,
    20.0,
    anchor="nw",
    text="Lionel Messi",
    fill="#000000",
    font=("Inter SemiBold", 36 * -1),
)

#################################################

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(1000.0, 1005.0, image=entry_image_1)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
)
entry_1.place(
    x=124.0,
    y=981.0,
    width=1752.0,
    height=46.0,
)

entry_1.bind("<Return>", threadGetField)


##################################################
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat",
    bg="#FFFFFF",
)
button_2.place(x=1831.0, y=983.0, width=44.0, height=44.0)

canvas.create_rectangle(0.0, 0.0, 56.0, 1080.0, fill="#FFFFFF", outline="")

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat",
    bg="#FFFFFF",
)
button_3.place(x=16.0, y=384.0, width=24.0, height=24.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat",
    bg="#FFFFFF",
)
button_4.place(x=16.0, y=440.0, width=24.0, height=24.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat",
    bg="#FFFFFF",
)
button_5.place(x=16.0, y=496.0, width=24.0, height=24.0)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat",
    bg="#FFFFFF",
)
button_6.place(x=16.0, y=552.0, width=24.0, height=24.0)

button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat",
    bg="#FFFFFF",
)
button_7.place(x=16.0, y=608.0, width=24.0, height=24.0)

button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat",
    bg="#FFFFFF",
)
button_8.place(x=0.0, y=6.0, width=56.0, height=56.0)

button_image_9 = PhotoImage(file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_9 clicked"),
    relief="flat",
    bg="#FFFFFF",
)

button_9.place(x=16.0, y=998.0, width=24.0, height=24.0)
window.resizable(True, True)
window.mainloop()
