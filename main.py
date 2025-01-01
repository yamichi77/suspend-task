import ctypes
import subprocess
import time
from socket import AF_INET, SOCK_STREAM, socket

import windowSuspend

HOST = "localhost"
PORT = 51000
MAX_MESSEAGE = 2048
NUM_THREAD = 4
PAUSE = 0x13


def isPressed(key):
    return bool(ctypes.windll.user32.GetAsyncKeyState(key) & 0x8000)


def create_task():
    folder_path = []
    cmd = []
    folder_path.append("exit_task.py")
    cmd.append("python" + " " + folder_path[0])
    subprocess.Popen(cmd[0], shell=True)


def receive():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setblocking(False)
    sock.bind((HOST, PORT))
    sock.listen(NUM_THREAD)
    return sock


def main():
    create_task()
    sock = receive()
    while True:
        if isPressed(PAUSE):
            winCls = windowSuspend.SuspendClass()
            winCls.get_pid()
            winCls.window_minimize()
            winCls.window_suspend()
            # winCls.get_name_by_pid()
            winCls.create_task()
            time.sleep(1)
            del winCls
        time.sleep(0.01)
        try:
            conn, addr = sock.accept()
            mess = conn.recv(MAX_MESSEAGE).decode("utf-8")
            conn.close()
            if mess == "/14":
                break
            else:
                continue
        except BlockingIOError:
            continue


if __name__ == "__main__":
    main()
