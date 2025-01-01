import ctypes
import subprocess
import sys

import psutil
import win32.win32gui
import win32.win32process

USER32 = ctypes.windll.user32


class SuspendClass:
    def __init__(self):
        self.hw = None
        self.pid = None
        self.proc = []

    def get_pid(self):
        # フォアグラウンドのPIDの取得
        self.hw = win32.win32gui.GetForegroundWindow()
        (tid1, self.pid) = win32.win32process.GetWindowThreadProcessId(self.hw)
        self.proc.append(psutil.Process(self.pid))
        for p in self.proc[0].children():
            self.proc.append(p)

    def window_minimize(self):
        # ウィンドウの最小化
        USER32.ShowWindow(self.hw, 6)

    def window_suspend(self):
        # ウィンドウの停止
        for p in self.proc:
            if p != "explorer.exe":
                p.suspend()
            else:
                sys.exit()

    def create_task(self):
        # タスクの作成
        folder_pass = "./tesks.py"
        cmd = (
            "python"
            + " "
            + folder_pass
            + " "
            + str(self.pid)
            + " "
            + str(self.hw)
            + " "
            + self.proc[0].name()
            + ' "'
            + self.proc[0].cmdline()[0]
            + '"'
        )
        subprocess.Popen(cmd, shell=True)


class ResumeClass:
    def __init__(self, pid, hw):
        self.pid = pid
        self.hw = hw

    def window_resume(self):
        # ウィンドウの再開
        self.proc = psutil.Process(int(self.pid))
        self.proc.resume()
        for p in self.proc.children():
            p.resume()

    def window_maximize(self):
        # ウィンドウの最大化
        USER32.ShowWindow(int(self.hw), 1)
