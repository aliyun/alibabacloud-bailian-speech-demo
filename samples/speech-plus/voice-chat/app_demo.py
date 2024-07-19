import sys
import wx


class MyFrame(wx.Frame):
    """
    Custom frame class inheriting from wx.Frame for creating a GUI window.

    Attributes:
        label (wx.StaticText): Static text control displaying prompt information.
        button1 (wx.Button): Speak start button triggering the click event handler.
    """

    def __init__(self, click1, *args, **kw):
        """
        Constructor initializes the frame window and sets up its components.

        Args:
            click1 (function): Button click event handler.
            args: Variable argument list passed to the parent constructor.
            kw: Keyword variable arguments passed to the parent constructor.
        """
        super(MyFrame, self).__init__(*args, **kw)

        # Create a panel as container
        panel = wx.Panel(self)

        # Initialize static text control
        self.label = wx.StaticText(panel, label="点击按键开始交互")
        self._configure_label()  # Configure static text style

        # Initialize speak start button
        self.button1 = wx.Button(panel, label="开始说话")
        self.button1.Bind(wx.EVT_BUTTON, click1)  # Bind button click event

        # Set layout manager
        self._setup_layout()

        self.SetTitle("VoiceChat")  # Set window title
        self.SetSize((400, 200))  # Set window size

    def _configure_label(self):
        """Configures the style of the static text control."""
        font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.label.SetFont(font)
        self.label.SetForegroundColour(wx.Colour(128, 0, 128))

    def _setup_layout(self):
        """Sets up the window layout."""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        label_sizer.AddStretchSpacer()
        label_sizer.Add(self.label, 0, wx.CENTER)
        label_sizer.AddStretchSpacer()

        button_sizer.Add(self.button1, 0, wx.ALL, 5)

        main_sizer.AddStretchSpacer()
        main_sizer.Add(label_sizer, 0, wx.EXPAND)
        main_sizer.Add(button_sizer, 0, wx.CENTER)
        main_sizer.AddStretchSpacer()

        panel = self.GetChildren()[0]  # Get panel object
        panel.SetSizer(main_sizer)

    def update_text(self, text):
        """
        Updates the display content of the static text control.

        Args:
            text (str): New text to be displayed.
        """
        self.button1.SetLabel(text)


class MyApp(wx.App):
    """
    Application class inheriting from wx.App responsible for application initialization and control.
    """

    def OnInit(self):
        """
        Initialization method called when the application starts.
        """
        global frame
        return True

    def setButtonClicks(self, click1):
        """
        Sets the button click event handler and displays the frame window.

        Args:
            click1 (function): Button click event handler.
        """
        global frame
        frame = MyFrame(click1, None)
        frame.Show(True)

    def update_text(self, text):
        """
        Updates the static text content in the frame window.

        Args:
            text (str): New text content.
        """
        frame.update_text(text)

    def OnCloseWindow(self, event):
        # when window is closed
        sys.exit(1)
