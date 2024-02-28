import wx
import wx.adv
from CustomWidgets.PDFParser import ParsePanel


# Создаем окно
class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 700))
        # panel = wx.Panel(self)
        # wx.Button(panel, label='Кнопка')
        ParsePanel(self)

class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, "PDF Parser by Starkov")
        frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(True)
    app.MainLoop()