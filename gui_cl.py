from tkinter import *
from tkinter.ttk import *
import re
import socket
import keyboard
from threading import Thread
from time import sleep


success = False
save_conn = True


def client_connect(ip, port, keys):
    global success
    cl = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    cl.connect(
        (ip, port)
    )

    success = True

    k_pressed_past = set()
    k_released_past = set()
    while save_conn:
        k_pressed = set()
        k_released = set()
        for k in keys:
            if keyboard.is_pressed(k):
                if keys[k] not in k_pressed_past:
                    k_pressed.add(keys[k])
            else:
                if keys[k] not in k_released_past:
                    k_released.add(keys[k])
        if k_pressed or k_released:
            p = '+'.join(list(k_pressed)) if k_pressed else '--'
            r = '+'.join(list(k_released)) if k_released else '--'
            data = p + ' ' + r

            cl.send(data.encode('utf-8'))
            ans = cl.recv(1)

            k_pressed_past = k_pressed
            k_released_past = k_released


def connect():
    global mes, save_conn
    save_conn = True

    ip, port = ip_field.get(), port_field.get()
    if re.match('((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))', ip):
        keys = {}
        for i in range(len(keys_lbl)):
            keys[keys_lbl[i][1].get()] = keys_lbl[i][3].get()

        # client_connect(ip, int(port), keys)
        th = Thread(target=client_connect, args=(ip, int(port), keys,))
        th.start()

        sleep(1)
        if success:
            mes.config(text='Connection established')

            conn.grid_remove()
            br.grid(column=4, row=0)
        else:
            mes.config(text='Error')
    else:
        mes.config(text='Incorrect ip')


def break_conn():
    global save_conn
    save_conn = False

    br.grid_remove()
    conn.grid(column=4, row=0)
    mes.config(text='Connection break')


def add_key():
    keys_lbl.append([Label(frame, text=f'key: {len(keys_lbl) + 1}'),
                     Entry(frame, width=5),
                     Label(frame, text="to"),
                     Entry(frame, width=5)
                     ])
    keys_lbl[-1][0].grid(column=0, row=len(keys_lbl) + 1)
    keys_lbl[-1][1].grid(column=1, row=len(keys_lbl) + 1)
    keys_lbl[-1][2].grid(column=2, row=len(keys_lbl) + 1)
    keys_lbl[-1][3].grid(column=3, row=len(keys_lbl) + 1)

    add_key.grid(column=0, row=len(keys_lbl)+2)


window = Tk()
window.title("Client")
# window.geometry('800x600')

frame = Frame(window)
frame.pack()

lbl_ip = Label(frame, text="ip")
lbl_ip.grid(column=0, row=0)

ip_field = Entry(frame, width=10)
ip_field.grid(column=1, row=0)

lbl_port = Label(frame, text="port")
lbl_port.grid(column=2, row=0)

port_field = Entry(frame, width=10)
port_field.grid(column=3, row=0)

lbl_key = Label(frame, text="key binds:")
lbl_key.grid(column=0, row=1)

keys_lbl = []
add_key = Button(frame, text="Add key", command=add_key)
add_key.grid(column=0, row=2)

conn = Button(frame, text="Connect!", command=connect)
conn.grid(column=4, row=0)

br = Button(frame, text="Break", command=break_conn)

mes = Label(frame, text="")
mes.grid(column=4, row=1)

window.mainloop()