import wx
from MyFunctions.myProtocolParser import read_PDF, save_to_db


class ParsePanel(wx.Panel):
    def __init__(self, parent, data_base=None):
        wx.Panel.__init__(self, parent)

        self.parsedData = None
        self.addPDFBtn = wx.Button(self, label="Add PDF")
        self.saveBtn = wx.Button(self, label="Save to DB")
        self.information = wx.ListCtrl(self, style=wx.LC_REPORT, size=wx.Size(300, 1000))
        self.information.InsertColumn(0, "Номер", width=150)
        self.information.InsertColumn(1, "Дата поверки", width=150)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        buttonSizer.AddMany([
            (self.addPDFBtn),
            (self.saveBtn)
        ])
        tableSizer = wx.BoxSizer(wx.VERTICAL)
        tableSizer.Add(self.information)
        mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        mainSizer.Add(buttonSizer)
        mainSizer.Add(tableSizer)
        self.SetSizer(mainSizer)

        self.addPDFBtn.Bind(wx.EVT_BUTTON, self.getPDFData)
        self.saveBtn.Bind(wx.EVT_BUTTON, self.saveToDataBase)

    def getPDFData(self, event):
        my_dir = "C:/Users/Zver/Desktop/NUMBERS/Actual_folder/2022/utilities/ProtocolParser/NewProtocols"
        dlg = wx.FileDialog(self, message="Выберите файл", defaultDir=my_dir, wildcard='*.pdf', style=wx.DD_DEFAULT_STYLE)
        dlg.ShowModal()
        file = dlg.GetPath()
        self.parsedData = read_PDF(file)
        for item in self.parsedData:
            self.information.Append(item)
        wx.MessageBox(f'Получено {len(self.parsedData)} номеров из файла {file}', 'getPDFData', wx.OK, self)

    def saveToDataBase(self, event):
        save_to_db('aqua_metrology', 'sampling_act', self.parsedData)
        self.parsedData = None
        self.information.DeleteAllItems()
        wx.MessageBox('Данные сохранены в таблицу sampling_act базы данных aqua_metrology', 'saveToDataBase', wx.OK, self)