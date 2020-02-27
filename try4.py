import wx
from wx.lib.pubsub import pub
from client import *


class MyPanel(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.symbol = ""
        self.yourTurn = False
        self.xo = self.creatXO()  # כל העיגולים והאיקסים שיש במשחק#x,3
        self.table = self.createTable()  # טבלת מיקומים
        self.places = self.createPlaces()  # offset_x, offset_y#מקומות אפשריים לטבלה
        self.dc = wx.MemoryDC()  # when drawing not in OnPaint, use MemoryDC
        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)

        commThread = Thread(target=client_send, args=())
        commThread.start()
        pub.subscribe(self.updateDisplay, "update")

    def updateDisplay(self, msg):
        """
        Receives update message about move in other side
        """
        global other_color
        t = msg
        tmp = t[len("server response") + 1:]
        info = tmp.split(",")
        if len(info) == 3:
            if info[0] == "symbol":
                self.symbol = str(info[1])
                if info[2] == "True":
                    self.yourTurn = True
                if info[2] == "False":
                    self.yourTurn = False
                print(msg)
            if info[0] == "draw":
                place = int(info[1])
                symbol = str(info[2])
                self.xo[place - 1][0] = str(symbol)  # add another X to ticTacToe list
                msg = "draw," + str(info[1]) + "," + str(info[2])
                print("msg 222", msg)
                if self.symbol != symbol:
                    self.yourTurn = True
                self.redraw()

    def drawX(self, x, y):
        print("111", x, y)  # spmetime one press is few press.need to do some bouncing
        size = 20
        pen = wx.Pen(wx.Colour(0, 0, 255))
        self.dc.SetPen(pen)
        self.dc.DrawLine(x - size, y + size, x + size, y - size)
        self.dc.DrawLine(x - size, y - size, x + size, y + size)

    def OnPaint(self, evt):
        self.dc = wx.PaintDC(self)  # when drawing in OnPaint, use PaintDC.this definition should be here in the event !
        self.drawBoard()
        for i in self.xo:  # draw all the X
            place = int(i[1])
            if i[0] != "":
                x = int(self.places[place - 1][0])
                y = int(self.places[place - 1][1])
                if i[0] == "x":
                    self.drawX(x, y)
                else:
                    self.drawO(x, y)

        if self.checkRow()[0]== True:
            print(self.checkRow()[1]+ " is the winner!!!!! :)")
            self.yourTurn = False
        if self.checkColumn()[0] == True:
            print(self.checkColumn()[1] + " is the winner!!!!! :)")
            self.yourTurn = False
        if self.checkDiagonal()[0] == True:
            print(self.checkDiagonal()[1] + " is the winner!!!!! :)")
            self.yourTurn = False

    def redraw(self):  # redraw the windows - create EVT_PAINT
        self.Hide()  # redraw the board
        self.Show()

    def MouseUp(self, e):
        self.d = 1
        x, y = e.GetPosition()
        ok = self.checkPlace(x, y)
        if ok[1] == True and self.yourTurn == True:
            print("mushi")
            self.xo[ok[0] - 1][0] = self.symbol
            msg = "draw," + str(ok[0]) + "," + self.symbol
            conn_q.put(msg)
            print("msg 111", msg)
            self.yourTurn = False
            self.redraw()

    def checkRow(self):
        win = False
        symbol=""
        for i in range(0, 6, 3):
            if self.xo[i][0] == self.xo[i + 1][0] and self.xo[i + 1][0] == self.xo[i + 2][0] and self.xo[i][0] != "":
                win = True
                symbol=self.xo[i][0]
                print("win row " + self.xo[i][0])
        return win,symbol

    def checkColumn(self):
        win = False
        symbol = ""
        for i in range(2):
            if self.xo[i][0] == self.xo[i + 3][0] and self.xo[i + 3][0] == self.xo[i + 6][0] and self.xo[i][0] != "":
                win = True
                symbol = self.xo[i][0]
                print("win column" + self.xo[i][0])
        return win,symbol

    def checkDiagonal(self):
        win = False
        symbol = ""
        if (self.xo[0][0] == self.xo[4][0] and self.xo[4][0] == self.xo[8][0] and self.xo[4][0] != "")\
                or(self.xo[2][0] == self.xo[4][0] and self.xo[4][0] == self.xo[6][0]  and self.xo[4][0] != ""):
            win = True
            symbol= self.xo[4][0]
            print("win Diagonal" + self.xo[4][0])
        return win,symbol

    def drawBoard(self):
        # x0,y0,x1,y1
        pen = wx.Pen(wx.Colour(0, 0, 255))
        self.dc.SetPen(pen)
        offset_x = 350
        offset_y = 350
        self.dc.DrawLine(offset_x, offset_y, offset_x - 300, offset_y)
        self.dc.DrawLine(offset_x, offset_y - 100, offset_x - 300, offset_y - 100)
        self.dc.DrawLine(offset_x, offset_y - 200, offset_x - 300, offset_y - 200)
        self.dc.DrawLine(offset_x, offset_y - 300, offset_x - 300, offset_y - 300)

        self.dc.DrawLine(offset_x, offset_y - 300, offset_x, offset_y)
        self.dc.DrawLine(offset_x - 100, offset_y - 300, offset_x - 100, offset_y)
        self.dc.DrawLine(offset_x - 200, offset_y - 300, offset_x - 200, offset_y)
        self.dc.DrawLine(offset_x - 300, offset_y - 300, offset_x - 300, offset_y)

    def drawX(self, x, y):
        pen = wx.Pen(wx.Colour(0, 0, 255))
        self.dc.SetPen(pen)
        size = 20
        # x0,y1,x1,y0
        self.dc.DrawLine(x - size, y + size, x + size, y - size)
        self.dc.DrawLine(x - size, y - size, x + size, y + size)

    def drawO(self, x, y):
        pen = wx.Pen(wx.Colour(0, 0, 255))
        self.dc.SetPen(pen)
        self.dc.DrawCircle(x, y, 25)

    def createTable(self):
        table = []
        offset_x = 50
        offset_y = 50
        for i in range(3):
            for j in range(3):
                table.append([offset_x, offset_y, offset_x + 100, offset_y + 100])
                offset_x = offset_x + 100
            offset_x = offset_x - 300
            offset_y = offset_y + 100
        return table

    def createPlaces(self):
        places = []
        offset_x = 100
        offset_y = 100
        for i in range(3):
            for j in range(3):
                places.append([offset_x, offset_y])
                offset_x = offset_x + 100
            offset_x = offset_x - 300
            offset_y = offset_y + 100
        return places

    def creatXO(self):
        xo = []
        for i in range(9):
            xo.append(["", i + 1])
        return xo

    def checkPlace(self, x, y):
        pos = 0  # המקום ברשימה שבו צריך לשים את האיקס או את העיגול
        empty = True
        rightPlace = False
        for i in self.table:
            if (x >= i[0] and x <= i[2]) and (y >= i[1] and y <= i[3]):
                rightPlace = True
                break
            pos = pos + 1

        place = ""
        if rightPlace == True:
            place = pos + 1
            if self.xo[place - 1][0] == "x" or self.xo[place - 1][0] == "o":
                empty = False

        ok = empty * rightPlace
        list = (place, ok)
        return list


app = wx.App()
frame = wx.Frame(None, -1, "BOKER MUSH", size=(400, 400))
MyPanel(frame, -1)
frame.Show(True)
app.MainLoop()
