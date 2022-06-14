#############################################################
# File Name : Misc_DrawStuff.py
#
#             DrawStuff Class
#             draws a Line given two points and then draws
#             X and Y component Lines and displays their
#             values in an overlapping Label
#
# Created :   April 2020 
#
#
# BMR = mCMW
#
# mCMW = Minimum Calories to Maintain Weight (current weight)
#
# CMW  = Calories to Maintain Weight (current weight)
#
# CMGW = Calories to Maintain Goal Weight
#
# 
# 1) Create Object of Draw_Stuff()  (ex. Draw_Lines)
# 2) Then Call self.Draw_Lines.Show_Instructions(self.Screen_To_Draw)
# 3) Then Call self.Draw_Lines.Draw_Rectangle(pXo=Xo, pXf=Xf, pYo=Yo, pYf=Yf, pR=0, pG=0.39, pB=0.49, pW=3)
# 4) Call self.Draw_Lines.Clear_IG() to clean up
#
#############################################################

import math

from kivy.graphics import InstructionGroup
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.graphics import Point

##############################################################
##############################################################

class DrawStuff():

    #################################################
    def __init__(self, **kwargs):
        self.IG = InstructionGroup()
        return

    #################################################
    # Clear all the Instructions from the IG
    # and make the Labels invisible
    def Clear_IG(self):
        self.IG.clear()
        return

    #################################################
    def Show_Instructions(self, pScreen=None):
        if(pScreen is not None):
            pScreen.canvas.add(self.IG)
            pScreen.canvas.ask_update()
        return

    #################################################
    # Draw a Line inside the Drawing Window Area
    # given Pixel coordinates
    # Not Axis Coordinates
    def Draw_Line(self, pX1=0, pY1=0, pX2=0, pY2=0, pR=1, pG=1, pB=1, pW=1, pOp=1):
        self.IG.add(Color(rgba = (pR, pG, pB, pOp)))
        self.IG.add(Line(points = [pX1, pY1, pX2, pY2], width = pW))
        return

    #################################################
    def Draw_Point(self, pX=0, pY=0, pR=1, pG=1, pB=1, pW=1, pOp=1):
        self.IG.add(Color(rgba = (pR, pG, pB, pOp)))
        self.IG.add(Point(points = [pX, pY], pointsize = pW))
        return

    #################################################
    def Draw_Rectangle(self, pXo=0, pXf=100, pYo=0, pYf=100, pR=1, pG=1, pB=1, pW=1):
        self.Draw_Line(pX1=pXo, pY1=pYo, pX2=pXo, pY2=pYf, pR=pR, pG=pG, pB=pB, pW=pW)
        self.Draw_Line(pX1=pXo, pY1=pYf, pX2=pXf, pY2=pYf, pR=pR, pG=pG, pB=pB, pW=pW)
        self.Draw_Line(pX1=pXf, pY1=pYo, pX2=pXf, pY2=pYf, pR=pR, pG=pG, pB=pB, pW=pW)
        self.Draw_Line(pX1=pXo, pY1=pYo, pX2=pXf, pY2=pYo, pR=pR, pG=pG, pB=pB, pW=pW)
        return
    
    #################################################
    def Draw_Fill_Rectangle(self, pXo=0, pXf=100, pYo=0, pYf=100, pR=1, pG=1, pB=1, pW=1):
        for i in range(pXo, pXf, 1):
            self.Draw_Line(pX1=i, pY1=pYo, pX2=i, pY2=pYf, pR=pR, pG=pG, pB=pB, pW=2)
        return

    #################################################
    def Draw_FCP_Circle(self, pXo=0, pXf=100, pYo=0, pYf=100, pC=0, pF=0, pP=0):
        Xc = pXo + int((pXf - pXo) * 0.5)
        Yc = pYo + int((pYf - pYo) * 0.5)
        Pi = 3.141592653589793
        Two_Pi = Pi * 2.0
        Radius = int((pXf - Xc) * 0.85)
        dTheta = float((Two_Pi / 360.0) * 3.0)
        Starting_Angle = 0
        Total_Grams = pC + pF + pP
        if(Total_Grams > 0):
            Percent_Carbs   = float(pC / Total_Grams)
            Percent_Fats    = float(pF / Total_Grams)
            Percent_Protein = float(pP / Total_Grams)
            Angle_Carbs   = float(Percent_Carbs * Two_Pi)
            Angle_Fats    = float(Percent_Fats * Two_Pi)
            Angle_Protein = float(Percent_Protein * Two_Pi)
        else:
            return

        #############################################
        #
        # Fats - Pastel Blue
        #
        #############################################
        tmpAngle       = Starting_Angle
        Starting_Angle = tmpAngle + dTheta
        tmpAngle      += Angle_Fats
        Final_Angle    = tmpAngle - dTheta
        #########################################
        ### Pull Piece out from center a little
        Half_Angle = Final_Angle - Starting_Angle
        Half_Angle = Starting_Angle + (Half_Angle * 0.5)
        xo = Xc + ((Radius * 0.12) * math.cos(Half_Angle))
        yo = Yc + ((Radius * 0.12) * math.sin(Half_Angle))
        #########################################
        ### Draw First Edge of Pie Slice
        x2 = xo + (Radius * math.cos(Starting_Angle))
        y2 = yo + (Radius * math.sin(Starting_Angle))
        self.Draw_Line(xo, yo, x2, y2, 0.12, 0.47, 0.71, 2)
        #########################################
        x1 = x2
        y1 = y2
        tmp = (360 / Two_Pi) * Starting_Angle
        tmp = round(tmp, 0)
        sA  = int(tmp)
        tmp = (360 / Two_Pi) * Final_Angle
        tmp = round(tmp, 0)
        fA  = int(tmp)
        for xA in range(sA, fA, 12):
            #####################################
            ### Draw the Out Arc Circle
            tmp = float((Two_Pi / 360) * xA)
            x2 = int(xo + (Radius * math.cos(tmp)))
            y2 = int(yo + (Radius * math.sin(tmp)))
            self.Draw_Line(x1, y1, x2, y2, 0.12, 0.47, 0.71, 2)
            x1 = x2
            y1 = y2
        #########################################
        ### Draw Final Edge of Pie Slice
        x2 = xo + (Radius * math.cos(Final_Angle))
        y2 = yo + (Radius * math.sin(Final_Angle))
        self.Draw_Line(x1, y1, x2, y2, 0.12, 0.47, 0.71, 2)
        self.Draw_Line(xo, yo, x2, y2, 0.12, 0.47, 0.71, 2)
        #############################################

        #############################################
        #
        # Proteins - Gold
        #
        #############################################
        Starting_Angle = tmpAngle + dTheta
        tmpAngle      += Angle_Protein
        Final_Angle    = tmpAngle - dTheta
        #########################################
        ### Pull Piece out from center a little
        Half_Angle = Final_Angle - Starting_Angle
        Half_Angle = Starting_Angle + (Half_Angle * 0.5)
        xo = Xc + ((Radius * 0.12) * math.cos(Half_Angle))
        yo = Yc + ((Radius * 0.12) * math.sin(Half_Angle))
        #########################################
        ### Draw First Edge of Pie Slice
        x2 = xo + (Radius * math.cos(Starting_Angle))
        y2 = yo + (Radius * math.sin(Starting_Angle))
        self.Draw_Line(xo, yo, x2, y2, 1.0, 0.5, 0.05, 2)
        #########################################
        x1 = x2
        y1 = y2
        tmp = (360 / Two_Pi) * Starting_Angle
        tmp = round(tmp, 0)
        sA  = int(tmp)
        tmp = (360 / Two_Pi) * Final_Angle
        tmp = round(tmp, 0)
        fA  = int(tmp)
        for xA in range(sA, fA, 12):
            #####################################
            ### Draw the Out Arc Circle
            tmp = float((Two_Pi / 360) * xA)
            x2 = int(xo + (Radius * math.cos(tmp)))
            y2 = int(yo + (Radius * math.sin(tmp)))
            self.Draw_Line(x1, y1, x2, y2, 1.0, 0.5, 0.05, 2)
            x1 = x2
            y1 = y2
        #########################################
        ### Draw Final Edge of Pie Slice
        x2 = xo + (Radius * math.cos(Final_Angle))
        y2 = yo + (Radius * math.sin(Final_Angle))
        self.Draw_Line(x1, y1, x2, y2, 1.0, 0.5, 0.05, 2)
        self.Draw_Line(xo, yo, x2, y2, 1.0, 0.5, 0.05, 2)
        #############################################

        #############################################
        #
        # Carbohydrates - Leaf Green
        #
        #############################################
        Starting_Angle = tmpAngle + dTheta
        tmpAngle      += Angle_Carbs
        Final_Angle    = tmpAngle - dTheta
        #########################################
        ### Pull Piece out from center a little
        Half_Angle = Final_Angle - Starting_Angle
        Half_Angle = Starting_Angle + (Half_Angle * 0.5)
        xo = Xc + ((Radius * 0.12) * math.cos(Half_Angle))
        yo = Yc + ((Radius * 0.12) * math.sin(Half_Angle))
        #########################################
        ### Draw First Edge of Pie Slice
        x2 = xo + (Radius * math.cos(Starting_Angle))
        y2 = yo + (Radius * math.sin(Starting_Angle))
        self.Draw_Line(xo, yo, x2, y2, 0, 0.6, 0.3, 2)
        #########################################
        x1 = x2
        y1 = y2
        tmp = (360 / Two_Pi) * Starting_Angle
        tmp = round(tmp, 0)
        sA  = int(tmp)
        tmp = (360 / Two_Pi) * Final_Angle
        tmp = round(tmp, 0)
        fA  = int(tmp)
        for xA in range(sA, fA, 12):
            #####################################
            ### Draw the Out Arc Circle
            tmp = float((Two_Pi / 360) * xA)
            x2 = int(xo + (Radius * math.cos(tmp)))
            y2 = int(yo + (Radius * math.sin(tmp)))
            self.Draw_Line(x1, y1, x2, y2, 0, 0.6, 0.3, 2)
            x1 = x2
            y1 = y2
        #########################################
        ### Draw Final Edge of Pie Slice
        x2 = xo + (Radius * math.cos(Final_Angle))
        y2 = yo + (Radius * math.sin(Final_Angle))
        self.Draw_Line(x1, y1, x2, y2, 0, 0.6, 0.3, 2)
        self.Draw_Line(xo, yo, x2, y2, 0, 0.6, 0.3, 2)
        #############################################

        return

    #################################################
    def Draw_Calorie_Bar(self, pXo=0, pXf=100, pYo=0, pYf=100, pCal=0, pCMW=0, pCMGW=0):
        Width1     = int(pXf - pXo)
        Width_incr = int(Width1 / 5)
        x_incr     = int(Width_incr * 0.5)
        Width1     = Width_incr
        Height1 = int(pYf - pYo)
        Xo = pXo + Width_incr
        Xf = Xo + Width1
        Yo = pYo
        Yf = pYf
        Ymax = int(Yf * 1.05)
        #######################################
        if(pCal == 0):
            #########################
            # 100% Deficit
            for yp in range(Yo, Yf, 1):
                self.Draw_Line(pX1=Xo, pY1=yp, pX2=Xf, pY2=yp, pR=1, pG=0.5, pB=0.05, pW=2) # Gold
            #########################
            # Tick Mark for pCMW
            self.Draw_Line(pX1=Xo, pY1=Yf, pX2=(Xf+x_incr), pY2=Yf, pR=1, pG=0.5, pB=0.05, pW=2) # Gold
            #########################
            # Tick Mark for pCMGW
            Yg = Yo + int((Height1 / pCMW) * pCMGW)
            self.Draw_Line(pX1=Xo, pY1=Yg, pX2=(Xf+x_incr), pY2=Yg, pR=0, pG=0, pB=0, pW=2) # Black
            #########################
            return
        #######################################
        if(pCal <= pCMW):
            #########################
            # Amount of Calories Eaten still GOOD
            #########################
            Y = Yo + int((Height1 / pCMW) * pCal)
            #########################
            # Amount Eaten
            for yp in range(Yo, Y, 1):
                self.Draw_Line(pX1=Xo, pY1=yp, pX2=Xf, pY2=yp, pR=0.12, pG=0.47, pB=0.71, pW=2) # Blue
            #########################
            # Amount Left to Eat
            for yp in range(Y, Yf, 1):
                self.Draw_Line(pX1=Xo, pY1=yp, pX2=Xf, pY2=yp, pR=1, pG=0.5, pB=0.05, pW=2) # Gold
            #########################
            # Tick Mark for Eaten
            self.Draw_Line(pX1=Xo, pY1=Y, pX2=(Xf+x_incr), pY2=Y, pR=0.12, pG=0.47, pB=0.71, pW=2) # Blue
            #########################
            # Tick Mark for pCMW
            self.Draw_Line(pX1=Xo, pY1=Yf, pX2=(Xf+x_incr), pY2=Yf, pR=1, pG=0.5, pB=0.05, pW=2) # Gold
        else:
            #########################
            # You OVER ATE... BAD
            #########################
            #########################
            # Amount Eaten
            for yp in range(Yo, Yf, 1):
                self.Draw_Line(pX1=Xo, pY1=yp, pX2=Xf, pY2=yp, pR=0.12, pG=0.47, pB=0.71, pW=2) # Blue
            #########################
            # Amount Over Eaten
            for yp in range(Yf, Ymax, 1):
                self.Draw_Line(pX1=Xo, pY1=yp, pX2=Xf, pY2=yp, pR=0.75, pG=0.3, pB=0.3, pW=2) # Dark Red
        #########################
        # Tick Mark for pCMGW
        Yg = Yo + int((Height1 / pCMW) * pCMGW)
        self.Draw_Line(pX1=Xo, pY1=Yg, pX2=(Xf+x_incr), pY2=Yg, pR=0, pG=0, pB=0, pW=2) # Black
        #######################################
        return

##############################################################
##############################################################


