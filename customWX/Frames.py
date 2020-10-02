import wx


class SplitVHTabFrame(wx.Frame):
    """
    A custom wx Frame that has 3 separate windows in the following fashion:

    *---------------*----*
    |  mainWindow   |    |
    |               |    | <-- rightWindow
    *---------------|    |
    |  lowerWindow  |    |
    *---------------*----*

    The lower and rightmost windows have the ability to hold multiple tabs (panels).
    The user can toggle the view of the windows by clicking the "X" button.
    The user must implement a way in the GUI to toggle them back on after they are closed
    by utilizing the toggleWindow functions.
    """
    def __init__(self, parent, title, size, styleMain=None, styleDown=None, styleRight=None):
        super().__init__(parent, title=title, size=size)

        if styleMain is None:
            styleMain = wx.aui.AUI_NB_CLOSE_BUTTON | wx.aui.AUI_NB_TAB_MOVE
        if styleDown is None:
            styleDown = wx.aui.AUI_NB_CLOSE_BUTTON | wx.aui.AUI_NB_TAB_MOVE
        if styleRight is None:
            styleRight = wx.aui.AUI_NB_CLOSE_BUTTON | wx.aui.AUI_NB_TAB_MOVE

        # Setting up panel / notebook structure
        self.vSplitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.hSplitter = wx.SplitterWindow(self.vSplitter, style=wx.SP_LIVE_UPDATE)
        self.notebookDOWN = wx.aui.AuiNotebook(self.hSplitter, style=styleDown)
        self.notebookRIGHT = wx.aui.AuiNotebook(self.vSplitter, style=styleRight)
        self.notebookMAIN = wx.aui.AuiNotebook(self.hSplitter, style=styleMain)

        self.notebookDOWN.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.toggleLowerWindow)
        self.notebookMAIN.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.toggleMainWindow)
        self.notebookRIGHT.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.toggleRightWindow)

        self.hSplitter.SplitHorizontally(self.notebookMAIN, self.notebookDOWN, self.GetSize()[1] - 200)
        self.vSplitter.SplitVertically(self.hSplitter, self.notebookRIGHT, self.GetSize()[0] - 350)
        self.vSplitter.SetMinimumPaneSize(350)
        self.hSplitter.SetMinimumPaneSize(150)
        self.hSplitter.SetSashGravity(1)
        self.vSplitter.SetSashGravity(1)

        # Create Menubar
        self.menuBar = wx.MenuBar()
        self.SetMenuBar(self.menuBar)

        self.statusBar = self.CreateStatusBar(1)
        self.updateStatus('Welcome!')

    def addMenuButton(self, menu, buttonLabel, buttonFunction):
        """
        Adds a new button to the menu.
        :param menu: Where the button is going to be added
        :param buttonLabel: The label of the button
        :param buttonFunction: The function the button triggers when pushed
        :return: The button that was created and added to the menu
        """
        button = menu.Append(wx.ID_ANY, buttonLabel)
        self.Bind(wx.EVT_MENU, buttonFunction, button)
        return button

    def appendMenuBar(self, menuLabel):
        """
        Appends a new menu to the menubar.
        :param menuLabel: The label of the menu
        :return: The menu that was created and added to the menubar
        """
        menu = wx.Menu()
        self.menuBar.Append(menu, menuLabel)
        return menu

    def addTabToLowerWindow(self, label, panelConstructor):
        """
        Adds a panel tab to the lower window.
        :param label: The label of the tab
        :param panelConstructor: The constructor of the panel to be added
        :return: The panel that was added
        """
        panel = panelConstructor(self.notebookDOWN, self)
        self.notebookDOWN.AddPage(panel, label)
        return panel

    def addTabToRightWindow(self, label, panelConstructor):
        """
        Adds a panel tab to the rightmost window.
        :param label: The label of the tab
        :param panelConstructor: The constructor of the panel to be added
        :return: The panel that was added
        """
        panel = panelConstructor(self.notebookRIGHT, self)
        self.notebookRIGHT.AddPage(panel, label)
        return panel

    def addTabToMainWindow(self, label, panelConstructor):
        panel = panelConstructor(self.notebookMAIN, self)
        self.notebookMAIN.AddPage(panel, label)
        return panel

    def setHorizontalSplitterGravity(self, gravity):
        """
        Sets the gravity (resizing and scaling) of the horizontal splitter window.
        :param gravity: The value of the splitter window gravity with range [0,1]
        """
        self.hSplitter.SetSashGravity(1)

    def setVerticalSplitterGravity(self, gravity):
        """
        Sets the gravity (resizing and scaling) of the vertical splitter window.
        :param gravity: The value of the splitter window gravity with range [0,1]
        """
        self.vSplitter.SetSashGravity(1)

    def toggleRightWindow(self, event):
        """
        Toggles the rightmost window.
        :param event:
        """
        if self.vSplitter.IsSplit():
            self.vSplitter.Unsplit(self.notebookRIGHT)
            event.Veto()
        else:
            self.vSplitter.SplitVertically(self.hSplitter, self.notebookRIGHT, self.GetSize()[0] - 250)

    def toggleLowerWindow(self, event):
        """
        Toggles the lower window.
        :param event:
        """
        if self.hSplitter.IsSplit():
            self.hSplitter.Unsplit(self.notebookDOWN)
            event.Veto()
        else:
            self.hSplitter.SplitHorizontally(self.notebookMAIN, self.notebookDOWN, self.GetSize()[1] - 300)

    def toggleMainWindow(self, event):
        """
        Toggles the lower window.
        :param event:
        """
        if self.hSplitter.IsSplit():
            self.hSplitter.Unsplit(self.notebookMAIN)
            event.Veto()
        else:
            self.hSplitter.SplitHorizontally(self.notebookMAIN, self.notebookDOWN, self.GetSize()[1] - 300)

    def updateStatus(self, text):
        self.statusBar.SetStatusText(text)