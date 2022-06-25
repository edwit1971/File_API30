##############################################################
#
# Main.py  created June 2022
#
# Demonstrate the ability to Read and Write a File
# on an Android device running API30+
#
# I'm using Kivy Button instead of the fancier KivyMD Buttons
# because the KivyMD Button don't allow me to alter their
# size easily. There's so many bugs within Kivy and KivyMD.
#
##############################################################

import os

from kivymd.app import MDApp

from kivymd.uix.label       import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout

from kivy.uix.button import Button

from kivy.core.window import Window

from Misc_DrawStuff import DrawStuff

from kivy.utils import platform

import FileRW as RW


##############################################################
##############################################################


####################################################
class LayoutsApp(MDApp):

    def __init__(self, **kwargs):
        super(LayoutsApp, self).__init__(**kwargs)
        self.Main_Win   = MDFloatLayout()
        self.View_Win   = MDFloatLayout()
        self.LText      = MDLabel()
        self.B_Read     = Button()
        self.B_Write    = Button()
        self.Draw_Lines = DrawStuff()
        self.FileName   = 'File_API30.txt'
        self.PathName   = ''
        self.strFPName  = ''
        return
    
    
    def build(self):
        LayoutsApp.title = 'Files with API30'
        self.Draw_Lines.Show_Instructions(self.Main_Win)
        ############################################
        if(platform == 'android'):
            from android.storage import primary_external_storage_path
            self.PathName = primary_external_storage_path()
            
        self.PathName  = os.path.join(self.PathName, 'Download')
        self.strFPName = os.path.join(self.PathName, self.FileName)
        ############################################
        self.Main_Win.size = Window.size
        Screen_Width  = self.Main_Win.width
        Screen_Height = self.Main_Win.height
        Xc = int(Screen_Width * 0.5)
        Yc = int(Screen_Height * 0.5)
        Button_Width  = int(Screen_Width / 6)
        Button_Height = int(Screen_Height / 12)
        ############################################
        self.View_Win.width  = int(Screen_Width * 0.75)
        self.View_Win.height = int(Screen_Height * 0.75)
        self.View_Win.x      = Xc - int(self.View_Win.width * 0.5)
        self.View_Win.y      = Yc - int(self.View_Win.height * 0.5)
        ############################################
        self.Draw_Lines.Draw_Fill_Rectangle(pXo = self.View_Win.x, \
                                             pXf = self.View_Win.x + self.View_Win.width, \
                                             pYo = self.View_Win.y, \
                                             pYf = self.View_Win.y + self.View_Win.height, \
                                             pR = 0.8, \
                                             pG = 0.8, \
                                             pB = 0.8, \
                                             pW = 2)
        self.Draw_Lines.Draw_Rectangle(pXo = self.View_Win.x, \
                                        pXf = self.View_Win.x + self.View_Win.width, \
                                        pYo = self.View_Win.y, \
                                        pYf = self.View_Win.y + self.View_Win.height, \
                                        pR = 0, \
                                        pG = 0, \
                                        pB = 0, \
                                        pW = 3)
        ############################################
        self.B_Read.size_hint = (None, None)
        self.B_Read.font_size = 34
        self.B_Read.width     = Button_Width
        self.B_Read.height    = Button_Height
        self.B_Read.x         = Xc + int(Button_Width * 1)
        self.B_Read.y         = self.View_Win.y + self.View_Win.height + 10
        self.B_Read.text      = 'Read'
        if(self.B_Read.parent == None):
            self.Main_Win.add_widget(self.B_Read)
        self.B_Read.bind(on_release = self.Press_Read)
        ############################################
        self.B_Write.size_hint = (None, None)
        self.B_Write.font_size = 34
        self.B_Write.width     = Button_Width
        self.B_Write.height    = Button_Height
        self.B_Write.x         = Xc - int(Button_Width * 2)
        self.B_Write.y         = self.B_Read.y
        self.B_Write.text      = 'Write'
        if(self.B_Write.parent == None):
            self.Main_Win.add_widget(self.B_Write)
        self.B_Write.bind(on_release = self.Press_Write)
        ############################################
        self.LText.font_style = 'Subtitle2'
        self.LText.font_size  = 34
        self.LText.size_hint  = None, None
        self.LText.width      = self.View_Win.width
        self.LText.height     = self.View_Win.height
        self.LText.text_size  = (self.LText.width, None)
        self.LText.x          = self.View_Win.x
        self.LText.y          = self.View_Win.y
        self.LText.halign     = 'center'
        self.LText.valign     = 'center'
        self.LText.theme_text_color = 'Custom'
        self.LText.color      = (0, 0, 0, 1)
        self.LText.text = self.strFPName
        if(self.LText.parent == None):
            self.Main_Win.add_widget(self.LText)
        ############################################
        return self.Main_Win
        
    
    ################################################
    def Press_Read(self, instance):
        if(platform == 'android'):
            ############################
            # Read a text File and 
            # display its contents
            RW.Read_File(pLabel=self.LText)
        else:
            self.LText.text  = 'Press_Read()\n\nNot Android Device'
        return
    
    
    ################################################
    def Press_Write(self, instance):
        if(platform == 'android'):
            ############################
            # Save STRING_DATA to a file
            RW.Write_File(pLabel=self.LText)
        else:
            self.LText.text  = 'Press_Write()\n\nNot Android Device'
        return


##############################################################
##############################################################
    
LayoutsApp().run()

