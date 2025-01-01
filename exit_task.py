from socket import AF_INET, SOCK_STREAM, socket

import wx  # wxPython のモジュール
import wx.adv

HOST = "localhost"
PORT = 51000
EXIT_MESSAGE = "/14"

# -------------------------------------------------------------------------------
#   タスクトレイのクラス　(TaskBarIconを継承)
# -------------------------------------------------------------------------------


class SysTray(wx.adv.TaskBarIcon):

    def __init__(self):

        wx.adv.TaskBarIcon.__init__(self)  # 継承本の初期化を呼び出す

        icon = wx.Icon("logo.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon, "PAUSE_App")

        # 左クリック時の関数登録
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.LeftClick)

    # 注意点１　return　では、メニュー(self.menu)を渡す
    #           return Noneは、何もしない
    # 　　　　　ここで、メニューを毎回作成しなければいけない
    def CreatePopupMenu(self):

        menu = wx.Menu()  # タスクトレイメニューの作成
        menu.Append(1, "Exit")
        self.Bind(wx.EVT_MENU, self.click_item)
        return menu

    def LeftClick(self, even):
        # クリックされる度にフレームが作成されるので
        # されないようにしなければならな（クローズイベントを利用）
        # 終了処理ですタスクトレイから削除されます
        return

    def exitTray(self, event):
        self.Destroy()
        wx.Exit()

    # メニュー項目がクリックされた

    def click_item(self, event):
        event_id = event.GetId()  # IDを取得する

        if event_id == 1:
            self.exit_send()
            self.exitTray(event)

    def exit_send(self):
        while True:
            try:
                # 通信の確立
                sock = socket(AF_INET, SOCK_STREAM)
                sock.connect((HOST, PORT))

                # メッセージ送信
                sock.send(EXIT_MESSAGE.encode("utf-8"))

                # 通信の終了
                sock.close()
                break
            except ConnectionRefusedError:
                continue


# -------------------------------------------------------------------------------
# メイン
# -------------------------------------------------------------------------------


if __name__ == "__main__":
    app = wx.App()
    SysTray()  # タスクトレイクラスの呼出
    app.MainLoop()
