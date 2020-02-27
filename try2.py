import wx

class MyPanel(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.symbol = "o"
        self.xo = []  # כל העיגולים והאיקסים שיש במשחק#x,3
        self.table = self.createTable()  # טבלת מיקומים
        self.places = self.createPlaces() # counter, offset_x, offset_y#מקומות אפשריים לטבלה
        self.dc = wx.MemoryDC()  # when drawing not in OnPaint, use MemoryDC
        self.SetBackgroundColour("WHITE")
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)


    def OnPaint(self, evt):
        self.dc = wx.PaintDC(self)  # when drawing in OnPaint, use PaintDC.this definition should be here in the event !
        self.drawBoard()
        for i in self.xo:  # draw all the X
            x = int(i[1])
            y = int(i[2])
            if i[0] == "x":
                self.drawX(x, y)
            else:
                self.drawO(x, y)

    def redraw(self):  #redraw the windows - create EVT_PAINT
        self.Hide() #redraw the board
        self.Show()

    def MouseUp(self, e):
        self.d = 1
        x, y = e.GetPosition()
        ok = self.checkPlace(x, y)
        x = ok[0]
        y = ok[1]
        if ok[2] == True:
            self.xo.append([self.symbol, x, y])  # add another X to ticTacToe list
            msg = "draw," + str(x) + "," + str(y) + "," + self.symbol
            print("msg 111", msg)
            self.redraw()

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
        places=[]
        offset_x=100
        offset_y=100
        counter=1
        for i in range(3):
            for j in range(3):
                places.append([counter, offset_x, offset_y])
                offset_x = offset_x + 100
            offset_x = offset_x - 300
            offset_y = offset_y + 100
        return places

    def checkPlace(self, x, y):
        pos = 0  # המקום ברשימה שבו צריך לשים את האיקס או את העיגול
        empty = True
        rightPlace = False
        for i in self.table:
            if (x >= i[0] and x <= i[2]) and (y >= i[1] and y <= i[3]):
                rightPlace = True
                break
            pos = pos + 1

        if rightPlace == True:
            x = self.places[pos][1]
            y = self.places[pos][2]
            place=self.places[pos][0] ############להוסיף את זה
            
            for i in self.xo:
                if i[1] == x and i[2] == y:
                    empty = False

        ok = empty * rightPlace
        list = (x, y, ok)
        return list

    def fromPlaceToXY(self, place):
        for i in self.places:
            if place == i[0]:
                list= (i[1],i[2])
                return list


app = wx.App()
frame = wx.Frame(None, -1, "BOKER MUSH", size=(400, 400))
MyPanel(frame, -1)
frame.Show(True)
app.MainLoop()
