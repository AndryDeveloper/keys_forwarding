from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import re
import socket
import keyboard
from threading import Thread
from time import sleep


success = False
save_conn = True
focus = {}


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


def add_key_f():
    keys_lbl.append([Label(frame, text=f'key: {len(keys_lbl) + 1}'),
                     Entry(frame, width=5, state="readonly"),
                     Label(frame, text="to"),
                     Entry(frame, width=5, state="readonly")
                     ])
    keys_lbl[-1][0].grid(column=0, row=len(keys_lbl) + 1)
    keys_lbl[-1][1].grid(column=1, row=len(keys_lbl) + 1)
    keys_lbl[-1][1].bind("<FocusIn>", in_focus_key)
    keys_lbl[-1][1].bind("<FocusOut>", out_focus_key)
    keys_lbl[-1][2].grid(column=2, row=len(keys_lbl) + 1)
    keys_lbl[-1][3].grid(column=3, row=len(keys_lbl) + 1)
    keys_lbl[-1][3].bind("<FocusIn>", in_focus_key)
    keys_lbl[-1][3].bind("<FocusOut>", out_focus_key)

    key_frame.grid(column=0, row=len(keys_lbl)+2)


def add_config():
    path = filedialog.askopenfilename(
        filetypes=(("TXT files", "*.txt"),
                   ("All files", "*.*"))
    )

    with open(path) as f:
        ip, port, keys = f.read().split()
        ip, port, keys = ip.split('=')[1], port.split('=')[1], keys.split('=')[1]
        keys = {k.split(',')[0]: k.split(',')[1] for k in keys.split(';')}
    ip_field.insert(0, ip)
    port_field.insert(0, port)
    for k in keys:
        add_key_f()
        keys_lbl[-1][1].config(state="normal")
        keys_lbl[-1][3].config(state="normal")

        keys_lbl[-1][1].insert(0, k)
        keys_lbl[-1][3].insert(0, keys[k])

        keys_lbl[-1][1].config(state="readonly")
        keys_lbl[-1][3].config(state="readonly")


def save_config():
    path = filedialog.askdirectory()
    ip, port = 'ip=' + ip_field.get(), 'port=' + port_field.get()
    keys = 'keys='
    for i in range(len(keys_lbl)):
        keys += keys_lbl[i][1].get() + ',' + keys_lbl[i][3].get()
        if i != len(keys_lbl) - 1:
            keys += ';'
    with open(path + '/config.txt', 'w') as f:
        f.write(ip + '\n' + port + '\n' + keys)


def start_listening_keys(widget):
    while focus[str(widget)]:
        k = keyboard.read_key()
        if focus[str(widget)]:
            widget.config(state="normal")
            widget.delete(0, END)
            widget.insert(0, k)
            widget.config(state="readonly")


def in_focus_key(event):
    global focus
    focus[str(event.widget)] = True

    th = Thread(target=start_listening_keys, args=(event.widget,))
    th.start()


def out_focus_key(event):
    global focus
    focus[str(event.widget)] = False


window = Tk()
window.title("Client")

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
key_frame = Frame(frame)
key_frame.grid(column=0, row=2)
add_key = Button(key_frame, text="Add key", command=add_key_f)
add_key.grid(column=0, row=0)
add_conf = Button(key_frame, text="Add config", command=add_config)
add_conf.grid(column=1, row=0)
save_conf = Button(key_frame, text="Save config", command=save_config)
save_conf.grid(column=2, row=0)

conn = Button(frame, text="Connect!", command=connect)
conn.grid(column=4, row=0)

br = Button(frame, text="Break", command=break_conn)

mes = Label(frame, text="")
mes.grid(column=4, row=1)

window.mainloop()