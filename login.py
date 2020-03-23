import wx
import re
from wx.lib.pubsub import pub
from client import *
from time import sleep


# signUp
class SignUp(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Sign Up",size=(430,290))
        self.SetBackgroundColour((234, 205, 220))

        col = wx.BoxSizer(wx.VERTICAL)
        col.AddSpacer(40)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.AddSpacer(100)  # space between StaticText and TextCtrl

        lbl1 = wx.StaticText(self, label="Create an account")
        lbl1.SetFont(wx.Font(22, wx.ROMAN, wx.NORMAL, wx.BOLD))
        row.Add(lbl1)
        col.Add(row)

        col.AddSpacer(20)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.AddSpacer(80)
        self.user = wx.TextCtrl(self, size=wx.Size(110, 22))
        self.user.Bind(wx.EVT_SET_FOCUS, self.removeLbl2)
        row1.Add(self.user)
        row1.AddSpacer(40)  # space between StaticText and TextCtrl
        lbl2 = wx.StaticText(self, label=":Username")
        lbl2.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.LIGHT))
        row1.Add(lbl2)
        col.Add(row1)

        row5 = wx.BoxSizer(wx.HORIZONTAL)
        row5.AddSpacer(70)
        self.lbl3 = wx.StaticText(self)
        self.lbl3.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.LIGHT))
        self.lbl3.SetForegroundColour((255,0,0)) # set text color
        row5.Add(self.lbl3)
        col.Add(row5)


        col.AddSpacer(5)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.AddSpacer(80)  # space between StaticText and TextCtrl
        self.password = wx.TextCtrl(self, size=wx.Size(110, 22), style=wx.TE_PASSWORD)
        row2.Add(self.password)
        row2.AddSpacer(42)  # space between StaticText and TextCtrl
        lbl4 = wx.StaticText(self, label=":Password")
        self.password.Bind(wx.EVT_SET_FOCUS, self.removeLbl1)
        lbl4.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.LIGHT))
        row2.Add(lbl4)
        col.Add(row2)

        row3 = wx.BoxSizer(wx.HORIZONTAL)
        row3.AddSpacer(70)
        self.lbl5 = wx.StaticText(self)
        self.lbl5.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.LIGHT))
        self.lbl5.SetForegroundColour((255,0,0))
        row3.Add(self.lbl5)
        col.Add(row3)

        col.AddSpacer(10)
        row4 = wx.BoxSizer(wx.HORIZONTAL)
        row4.AddSpacer(80)
        btn1 = wx.Button(self, label="sign up")
        btn1.Bind(wx.EVT_BUTTON, self.ok)
        row4.Add(btn1)
        row4.AddSpacer(70)
        cancel = wx.Button(self, label="cancel")
        cancel.Bind(wx.EVT_BUTTON, self.cancel)
        row4.Add(cancel)
        col.Add(row4)

        self.SetSizer(col)
        self.Show()

        commThread = Thread(target=client_send, args=())
        commThread.start()
        pub.subscribe(self.updateDisplay, "update")

        self.valid = False

    def removeLbl1(self, event):
        self.lbl5.SetLabelText("")
        self.password.SetBackgroundColour("white")
        self.password.Clear()


    def removeLbl2(self, event):
        self.lbl3.SetLabelText("")
        self.user.SetBackgroundColour("white")
        self.user.Clear()

    def updateDisplay(self, msg):
        t = msg
        tmp = t[len("server response") + 1:]
        info = tmp.split(",")
        if info[0] == "checkSignUp":
            print (info[1])
            if info[1] == "True":
                self.valid = True

    def ok(self, event):
        p = self.password.GetValue()
        u = self.user.GetValue()
        msg = "checkSignUp," + u
        conn_q.put(msg)
        sleep(0.05)
        cond1 = len(p)<4
        cond2 = len(u)<4
        print("ccc" + str(self.valid))
        if cond1 or self.valid == False or cond2:
            if self.valid == False or cond2:
                self.user.SetBackgroundColour("pink")
                self.user.Refresh()
                if cond2:
                    self.lbl3.SetLabelText("Use at least 4 characters")
                else:
                    self.lbl3.SetLabelText("Username is already taken")
            if cond1:
                self.password.SetBackgroundColour("pink")
                self.password.Refresh()
                self.lbl5.SetLabelText("Use at least 4 characters")
        else:
            msg = "insertUser," + u + "," + p
            conn_q.put(msg)
            self.Close()

    def cancel(self, event):
        self.Close()


# chat
class Chat(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Chat")
        self.Show()


# main
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Main App", size=(430,320))
        self.SetBackgroundColour((234, 205, 220))

        col = wx.BoxSizer(wx.VERTICAL)
        col.AddSpacer(60)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.AddSpacer(60)  # space between StaticText and TextCtrl

        lbl1 = wx.StaticText(self, label="....Welcome to the ")
        lbl1.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD))
        row.Add(lbl1)
        col.Add(row)

        col.AddSpacer(20)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.AddSpacer(80)
        self.user = wx.TextCtrl(self, size=wx.Size(110, 25))
        self.user.Bind(wx.EVT_SET_FOCUS, self.removeLbl2)
        row1.Add(self.user)
        row1.AddSpacer(40)  # space between StaticText and TextCtrl
        lbl2 = wx.StaticText(self, label=":Username")
        lbl2.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.LIGHT))
        row1.Add(lbl2)
        col.Add(row1)

        col.AddSpacer(10)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.AddSpacer(80)  # space between StaticText and TextCtrl
        self.password = wx.TextCtrl(self, size=wx.Size(110, 25), style=wx.TE_PASSWORD)
        row2.Add(self.password)
        row2.AddSpacer(42)  # space between StaticText and TextCtrl
        lbl3 = wx.StaticText(self, label=":Password")
        self.password.Bind(wx.EVT_SET_FOCUS, self.removeLbl1)
        lbl3.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.LIGHT))
        row2.Add(lbl3)
        col.Add(row2)

        row3 = wx.BoxSizer(wx.HORIZONTAL)
        row3.AddSpacer(122)
        self.lbl4 = wx.StaticText(self)
        self.lbl4.SetForegroundColour((255, 0, 0))
        row3.Add(self.lbl4)
        col.AddSpacer(10)
        col.Add(row3)

        row4 = wx.BoxSizer(wx.HORIZONTAL)
        row4.AddSpacer(80)
        btn1 = wx.Button(self, label="Login")
        btn1.Bind(wx.EVT_BUTTON, self.login)
        row4.Add(btn1)

        row4.AddSpacer(25)  # space between StaticText and TextCtrl
        btn2 = wx.Button(self, label="Sign up")
        btn2.Bind(wx.EVT_BUTTON, self.sighUp)
        row4.Add(btn2)
        col.AddSpacer(20)
        col.Add(row4)

        self.SetSizer(col)
        self.Show()

        commThread = Thread(target=client_send, args=())
        commThread.start()
        pub.subscribe(self.updateDisplay, "update")

    def updateDisplay(self, msg):
        t = msg
        tmp = t[len("server response") + 1:]
        info = tmp.split(",")
        if info[0] == "checkLogin":
            if info[1] == "True":
                self.Close()
                #c=Chat()
            else:
                self.lbl4.SetLabelText(".Incorrect username or password")

    def login(self, event):
        u = self.user.GetValue()
        p = self.password.GetValue()
        msg = "checkLogin," + u + "," + p
        conn_q.put(msg)

    def sighUp(self, event):
        s = SignUp()
        self.user.Clear()
        self.password.Clear()
        self.lbl4.SetLabelText("")

    def removeLbl1(self, event):
        self.lbl4.SetLabelText("")
        self.password.Clear()

    def removeLbl2(self, event):
        self.lbl4.SetLabelText("")
        self.user.Clear()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
