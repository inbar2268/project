import wx
import re
from wx.lib.pubsub import pub
from client import *
from time import sleep

class Chat(wx.Frame):
    def __init__(self, name):
        self.name="hi"
        wx.Frame.__init__(self, None, title="Chat", size=(450,470))
        self.SetBackgroundColour((234, 205, 220))

        col = wx.BoxSizer(wx.VERTICAL)
        col.AddSpacer(30)

        row = wx.BoxSizer(wx.HORIZONTAL)
        row.AddSpacer(100)
        self.messageBox = wx.TextCtrl(self, size=wx.Size(300, 260), style=wx.TE_MULTILINE | wx.HSCROLL)
        self.messageBox.SetEditable(False)
        row.Add(self.messageBox)
        col.Add(row)
        col.AddSpacer(30)

        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.AddSpacer(70)
        sendBtn = wx.Button(self, label='Send', size=wx.Size(80, 25))
        sendBtn.Bind(wx.EVT_BUTTON, self.sendMsg)
        row1.Add(sendBtn)
        row1.AddSpacer(50)
        self.sendBox = wx.TextCtrl(self, size=wx.Size(200, 50))
        row1.Add(self.sendBox)
        col.Add(row1)

        self.SetSizer(col)
        self.Show()

        commThread = Thread(target=client_send, args=())
        commThread.start()
        pub.subscribe(self.updateDisplay, "update")

    def updateDisplay(self, msg):
        t = msg
        tmp = t[len("server response") + 1:]
        info = tmp.split(",")
        if info[0] == "msg":
            self.messageBox.AppendText(info[1]+":" + info[2] + '\n')

    def sendMsg(self, event):
        msg1 = self.sendBox.GetValue()
        self.sendBox.Clear()
        msg = "msg," + self.name + "," + msg1
        conn_q.put(msg)
        self.messageBox.AppendText("You: " + msg1 + '\n')



if __name__ == "__main__":
    app = wx.App(False)
    c = Chat("hi")
    app.MainLoop()
