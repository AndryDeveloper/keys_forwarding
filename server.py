import socket
import keyboard


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(
    ('0.0.0.0', 1234)
)

server.listen()

while True:
    conn, addr = server.accept()

    print('connected:', addr)

    while True:
        data = conn.recv(1024).decode('utf-8')

        if data is not None and data != '':
            p, r = data.split()
            if p != '--':
                keyboard.press(p)
            if r != '--':
                keyboard.release(r)

            conn.send(bytes(1))
            continue
        break

    conn.close()

