#!/usr/bin/python
# -*- coding: utf-8 -*-

# windowGen.py
try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required for this program. Please run pip install wxpython --user"



QUIT_ID = 1
ABOUT_ID = 2

class windowGen(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(windowGen, self).__init__(*args, **kwargs) 
            
        self.SetSize((400,500))
        self.SetTitle('Test GenTeX')
        #self.Subjects=['Mathematics','Biology','Chemistry','Physics','General Science']
        self.Subjects=['Mathematics','Chemistry','Physics']
        self.CoursesMath = ['MPM1D','MFM1P','MPM1H','MPM2D','MFM2D','MCR3U','MCF3M','MBF3C','MEL3E','MHF4U','MCV4U','MDM4U','MCT4C','MAP4C','MEL4E']
        self.CoursesChem = ['SCH3U','SCH3C','SCH4U']
        self.CoursesPhys = ['SPH3U','SPH3C','SPH4U']
        self.InitUI()
        #self.CoursesBio = ['SBI3U','SBI3C','SBI4U']
        #self.CoursesiGenSci = ['SNC1D','SNC1P','SNC2D','SNC2P','SNC4M','SNC4E']
        
    def InitUI(self):
        
        # Here's where there's a future call but it should display this when the function is done working!
        #wx.FutureCall(5000,self.ShowCompleted)
        
        # ---------------------------------------------------------------
        # Menu!
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu = wx.Menu()
        fmn = fileMenu.Append(wx.ID_NEW, '&New')
        fmq = fileMenu.Append(wx.ID_EXIT,'&Quit')
        self.Bind(wx.EVT_MENU, self.OnQuit, fmq)
        
        help = wx.Menu()
        help.Append(ABOUT_ID,'&About')
        self.Bind(wx.EVT_MENU, self.OnAboutBox, id=ABOUT_ID)
        
        menubar.Append(fileMenu,'&File')
        menubar.Append(help,'&Help')
        
        self.SetMenuBar(menubar)
        # ---------------------------------------------------------------
        # Sizer information
        panel = wx.Panel(self)
        font = wx.SystemSetting_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        # ---------------------------------------------------------------
        
        #choice_editor = wx.grid.GridCellChoiceEditor(choices_list, True) 
        #grid.SetCellEditor(row, col, choice_editor)
        
        subj = wx.ComboBox(self,-1,name=u'Subject',choices=self.Subjects)
        subj.SetFont(font)
        
        self.label = wx.StaticText(self,wx.ID_ANY,"Subject:")
        self.entry = 
        #sizer.Add(self.entry,(0,1),(1,2),wx.EXPAND)
        sizer.Add(self.entry,1,wx.EXPAND)
        #self.Bind(wx.EVT_TEXT_ENTER, self.OnPressEnter, self.entry)

        
        
        #button = wx.Button(self,-1,label="Ok")
        #sizer.Add(button, (1,0))
        #self.Bind(wx.EVT_BUTTON, self.OnButtonClick, button)
        
        ##self.label = wx.StaticText(self,-1,label=u'Welcome to Test GenTeX!')
        #self.label.SetForegroundColour(wx.BLACK)
        #sizer.Add( self.label, (1,1),(2,2), wx.EXPAND )

        
        #wx.Panel(self)
        
        # ---------------------------------------------------------------
        # Now we start the radio buttons!
        # 1) Course
        
        self.Centre()
        self.SetSizerAndFit(sizer)
        self.Show(True)
        
        
    def OnButtonClick(self,event):
        None # do stuff

    def OnPressEnter(self,event):
        self.label.SetLabel("You Pressed Enter!")
        
    def OnQuit(self, e):
        self.Close()

    def OnAboutBox(self, e):
        description = """Test GenTeX is a Python and LaTeX based test generating program built to optimize the test making and administration process to reduce workload for teachers and reduce the possibilities of cheating within the classroom."""
        licence = """Awesome license."""
        info = wx.AboutDialogInfo()
        #info.SetIcon(wx.Icon('hunter.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Test Generator')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2017 Anthony Salerno')
        info.SetWebSite('http://www.gentex.com')
        info.SetLicence(licence)
        info.AddDeveloper('Anthony Salerno')
        info.AddDocWriter('Anthony Salerno')
        #info.AddArtist('The Tango crew')
        #info.AddTranslator('Jan Bodnar')
        wx.AboutBox(info)
    
    def ShowCompleted(self):
        wx.MessageBox('Tests generated. %i Version(s) Made Successfully'%1,'Success!',wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
  
    app = wx.App()
    windowGen(None)
    app.MainLoop()
