import sys

import wx  # wxPython のモジュール
import wx.adv

import windowSuspend

# -------------------------------------------------------------------------------
#   タスクトレイのクラス　(TaskBarIconを継承)
# -------------------------------------------------------------------------------


class SysTray(wx.adv.TaskBarIcon):

    def __init__(self, name, icon_path):

        wx.adv.TaskBarIcon.__init__(self)  # 継承本の初期化を呼び出す

        self.name = name

        icon = wx.Icon(icon_path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon, "PAUSE：" + self.name)

        # CreatePopupMenuを使う場合は、コメントにする
        # 右クリック時の関数登録
        # //self.Bind( wx.adv.EVT_TASKBAR_RIGHT_UP,     self.RightClick)

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
        self.window_resume()
        self.exitTray(even)

    # 終了処理ですタスクトレイから削除されます
    def exitTray(self, event):
        self.Destroy()
        wx.Exit()

    # メニュー項目がクリックされた

    def click_item(self, event):
        event_id = event.GetId()  # IDを取得する

        if event_id == 1:
            self.exitTray(event)

    def window_resume(self):
        winCls.window_resume()
        winCls.window_maximize()


# -------------------------------------------------------------------------------
# メイン
# -------------------------------------------------------------------------------


if __name__ == "__main__":
    args = sys.argv
    winCls = windowSuspend.ResumeClass(args[1], args[2])
    app = wx.App()
    SysTray(args[3], args[4])  # タスクトレイクラスの呼出
    app.MainLoop()
