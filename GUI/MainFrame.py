import wx
import wx.grid
import wx.aui
import FileIO
from GUI.Panels import GraphPanel, FittingPanel
from customWX import Frames


class MainFrame(Frames.SplitVHTabFrame):
    def __init__(self, parent, title, size):
        super().__init__(parent, title, size)

        self.graphPanel = self.addTabToMainWindow('Graph', GraphPanel.GraphPanel)
        self.analysisOptionsPanel = self.addTabToRightWindow('Data Analysis', FittingPanel.AnalysisPanel)

        # Setup menu bar
        self.fileMenu = self.appendMenuBar('File')
        self.analysisMenu = self.appendMenuBar('Analysis')
        self.viewMenu = self.appendMenuBar('View')
        self.helpMenu = self.appendMenuBar('Help')

        # File menu
        self.openFileButton = self.addMenuButton(self.fileMenu, 'Open', self.openFile)
        self.saveFileButton = self.addMenuButton(self.fileMenu, 'Save', self.saveFile)
        self.quitButton = self.addMenuButton(self.fileMenu, 'Quit', self.quit)

        # Analysis menu
        self.interpolateButton = self.addMenuButton(self.analysisMenu, 'Interpolate Plot',
                                                    self.graphPanel.interpolateData)
        self.smoothButton = self.addMenuButton(self.analysisMenu, 'Smooth Plot', self.graphPanel.smoothData)

        # View Menu
        self.toggleGraphButton = self.addMenuButton(self.viewMenu, 'Toggle Graph View', self.toggleMainWindow)
        self.toggleOutputButton = self.addMenuButton(self.viewMenu, 'Toggle Output View', self.toggleLowerWindow)
        self.toggleOptionButton = self.addMenuButton(self.viewMenu, 'Toggle Options View', self.toggleRightWindow)
        self.viewMenu.InsertSeparator(2)
        #self.aboutButton = self.addMenuButton(self.helpMenu, 'About', self.defaultMenuButtonFunction)

        # Useful variables
        self.fileName = ''
        self.filePath = ''
        self.spectralFilePath = ''

    def openFile(self, event):
        wildCard = "CSV or TXT Files Containing Coordinate Data (*)|*"
        fileDialog = wx.FileDialog(self, "Open NMR or FID Data", wildcard=wildCard,
                                   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if fileDialog.ShowModal() == wx.ID_OK:
            self.filePath = fileDialog.GetPath()
            plotData = FileIO.openFile(self.filePath)
            self.graphPanel.newDataSet(plotData[0], plotData[1])
        fileDialog.Destroy()

    def saveFile(self, event):
        pass

    def quit(self, event):
        """
        Closes the program when triggered.
        :param event: The event triggering this function
        :return:
        """
        self.Close()


class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame(parent=None, title='Decon1D', size=(1000, 700))
        self.frame.Maximize(True)
        self.frame.Show()
        return True
