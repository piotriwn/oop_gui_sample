import tkinter
from tkinter.constants import  BOTH, E, EW, LEFT, NS, NW, S, X
from constants import *
from tkinter.messagebox import askyesno
from tkinter import ttk
from PIL import ImageTk, Image
from figures import Triangle


class Application(tkinter.Tk):
    def __init__(self, winSize, winTitle, transparency) :
        super().__init__()

        self.geometry(winSize)
        self.title(winTitle)
        self.resizable(False, False)
        self.iconbitmap(r"img\icon.ico")
        self.attributes('-alpha', transparency)
        self.frames = {}

        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for frame in (MainMenu, Continue, NewSession, SaveSession, LoadSession ):
            frameObject = frame(container, self) # container Frame is a parent, tkinter.Tk is a controller
            self.frames[frame.__name__] = frameObject
            frameObject.grid(row=0, column=0, sticky="nsew")

        self.showFrame("MainMenu")

    def showFrame(self, frameName):
        frame = self.frames[frameName]
        frame.tkraise()


class DefaultFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__( parent)
        self.backFrame = tkinter.Frame(self, bg='red')
        self.backFrame.place(x=0, y=0, anchor="nw", height=DEFAULT_FRAME_BACK_HEIGHT, width = WINDOW_WIDTH )
        backButton = tkinter.Button(self.backFrame, text="Test back button", command = lambda: controller.showFrame("MainMenu") )
        backButton.pack(side =  LEFT)
        self.dataFrame = tkinter.Frame(self) #, bg ='blue' )
        self.dataFrame.place(x=0, y=DEFAULT_FRAME_BACK_HEIGHT , anchor="nw", height=DEFAULT_FRAME_DATA_HEIGHT, width = WINDOW_WIDTH  )


class MainMenu(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__( parent)
        self.buttonsDataDict = MM_BUTTONS_DICT # this only copies from constants and its values are strings
        self.buttonsObjectDict = {} # values are button objects
        self.continueState = "disabled" # when you first start the program, continue and save buttons are disabled
        self.saveState = "disabled"

        # so that main menu buttons are centered
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure( len(self.buttonsDataDict) + 1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.createButtons()
        self.deployButtons(controller)


    def createButtons(self):
        for k, v in self.buttonsDataDict.items():
            self.buttonsObjectDict[k] = tkinter.Button(self, text=v, width= MM_BUTTON_WIDTH, pady = MM_BUTTON_Y_PADDING) # container is self - that is, MainMenu instance

    def _updateState(self):
        self.continueState = "active"
        self.saveState = "active"
        self.buttonsObjectDict[1].config(state = self.continueState)
        self.buttonsObjectDict[3].config(state = self.saveState)

    def _bindContinue(self, app):
        self.buttonsObjectDict[1].config(state = self.continueState)
        self.buttonsObjectDict[1].config(command = lambda: app.showFrame("Continue") )

    def _bindNewSession(self, app):
        self.buttonsObjectDict[2].config(command = lambda: self.confirmationNewLoad(app, "NewSession") )


    def _bindSaveSession(self):
        self.buttonsObjectDict[3].config(state = self.saveState)

    def _bindLoadSession(self):
        pass

    def _bindExit(self, app):
        self.buttonsObjectDict[5].config(command = app.destroy )

    def _bindButtons(self, app):
        self._bindContinue(app)
        self._bindNewSession(app)
        self._bindSaveSession()
        self._bindLoadSession()
        self._bindExit(app)


    def confirmationPrompt(self):
        return askyesno(title='Confirmation', message='Are you sure you want to scrape existing session?')

    def confirmationNewLoad(self, app, frameName):
        if self.continueState == "active":
            answer = self.confirmationPrompt()
        else:
            answer = True
        if (answer):
            self._updateState()
            app.showFrame(frameName)
        else:
            app.showFrame("MainMenu")


    def deployButtons(self, app):
        for k, v in self.buttonsObjectDict.items():
            v.grid(row = k, column = 0, pady = MM_BUTTON_Y_PADDING)
        self._bindButtons(app)


class Continue(DefaultFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        label = tkinter.Label(self.dataFrame, text="This is continue class")
        label.pack()

class NewSession(DefaultFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.currentChoice = None

        self.comboVar = tkinter.StringVar()
        self.combo = ttk.Combobox(self.dataFrame, textvariable = self.comboVar, width= NS_COMBO_WIDTH)
        self.combo['values'] = ("Triangle", "Square", "Rectangle", "Hexagon")
        self.combo['state'] = 'readonly'
        self.combo.set("Triangle")
        self.combo.place(x= NS_COMBO_X_POS, y = NS_COMBO_Y_POS)

        self.selectButton = tkinter.Button(self.dataFrame, text="Select", width = NS_BUTTON_SELECT_WIDTH, pady = NS_BUTTON_Y_PADDING, command = self.bindSelect)
        self.selectButton.place(x = NS_BUTTON_SELECT_X_POS, y=NS_BUTTON_SELECT_Y_POS, anchor="nw")

        self.propertiesLabel = tkinter.Label(self.dataFrame, text="Properties")
        self.propertiesLabel.place(x=NS_LABEL_PROPERTIES_X_POS, y = NS_LABEL_PROPERTIES_Y_POS, anchor = 'nw')

        self.areaLabel = tkinter.Label(self.dataFrame, text = "Area:")
        self.areaLabel.place(x= NS_LABEL_PROPERTIES_X_POS, y = NS_AREA_LABEL_Y_POS, anchor = "nw")
        self.areaValue = tkinter.Entry(self.dataFrame, state = "disabled", width = NS_ENTRY_VALUES_WIDTH)
        self.areaValue.place(x =NS_ENTRY_VALUES_X, y= NS_AREA_LABEL_Y_POS, anchor = "nw")

        self.circumLabel = tkinter.Label(self.dataFrame, text = "Circumference:")
        self.circumLabel.place(x=NS_LABEL_PROPERTIES_X_POS, y =NS_CIRCUM_LABEL_Y_POS, anchor = "nw")
        self.circumValue = tkinter.Entry(self.dataFrame, state = "disabled", width = NS_ENTRY_VALUES_WIDTH)
        self.circumValue.place(x =NS_ENTRY_VALUES_X, y= NS_CIRCUM_LABEL_Y_POS, anchor = "nw")

        self.rInscribedLabel = tkinter.Label(self.dataFrame, text = "Inscribed circle r:")
        self.rInscribedLabel.place(x=NS_LABEL_PROPERTIES_X_POS , y= NS_INSCR_LABEL_Y_POS, anchor = "nw")
        self.rInscribedValue = tkinter.Entry(self.dataFrame, state = "disabled", width = NS_ENTRY_VALUES_WIDTH)
        self.rInscribedValue.place(x =NS_ENTRY_VALUES_X, y= NS_INSCR_LABEL_Y_POS, anchor = "nw")

        self.RCircumLabel = tkinter.Label(self.dataFrame, text = "Circumscribed circle R:")
        self.RCircumLabel.place(x=NS_LABEL_PROPERTIES_X_POS, y=NS_R_CIRCUM_LABEL_Y_POS, anchor = "nw")
        self.RCircumValue = tkinter.Entry(self.dataFrame, state = "disabled", width = NS_ENTRY_VALUES_WIDTH)
        self.RCircumValue.place(x =NS_ENTRY_VALUES_X, y= NS_R_CIRCUM_LABEL_Y_POS, anchor = "nw")

        #self.leftFrame = tkinter.Frame(self.dataFrame, bg= "blue")
        #self.leftFrame.place(x = NS_LEFT_FRAME_X, y = NS_LEFT_FRAME_Y, width= NS_LEFT_FRAME_WIDTH, height= NS_LEFT_FRAME_HEIGHT)

    def bindSelect(self):
        methodName = getattr(self, f"_bind{self.combo.get()}")
        self._clearValues()
        methodName()
        self.calcButton = tkinter.Button(self.dataFrame, text="Calculate", pady = NS_BUTTON_Y_PADDING)
        self.calcButton.place(x = NS_CALC_BUTTON_X_POS, y = NS_CALC_BUTTON_Y_POS, anchor = "nw")

    def _clearValues(self):
        if self.currentChoice not in ("Triangle", "Square", "Rectangle", "Hexagon"):
            return
        if self.currentChoice == "Triangle":
            [item.destroy() for item in [self.aValue, self.bValue, self.cValue, self.triangle] ]
            try:
                del self.triangleObj
            except NameError:
                pass
            self.currentChoice = None


    def _bindTriangle(self):
        print("Selected triangle!")
        self.currentChoice = "Triangle"
        self.img = Image.open(r"img\triangle.png") # PIL solution
        self.img = self.img.resize( (NS_TRIANGLE_IMAGE_WIDTH,NS_TRIANGLE_IMAGE_WIDTH), Image.ANTIALIAS) # resize
        self.img = ImageTk.PhotoImage(self.img) # # convert to PhotoImage
        self.triangle = tkinter.Label(self.dataFrame, image=self.img)
        self.triangle.place(x = NS_TRIANGLE_IMAGE_X, y = NS_TRIANGLE_IMAGE_Y, anchor = "nw")

        self.aValue = tkinter.Entry(self.dataFrame, width = NS_TRIANGLE_VALUES_WIDTH)
        self.aValue.place(x = NS_TRIANGLE_A_VALUE_X, y =NS_TRIANGLE_A_VALUE_Y, anchor = "nw")

        self.bValue = tkinter.Entry(self.dataFrame, width = NS_TRIANGLE_VALUES_WIDTH)
        self.bValue.place(x = NS_TRIANGLE_B_VALUE_X, y =NS_TRIANGLE_B_VALUE_Y, anchor = "nw")

        self.cValue = tkinter.Entry(self.dataFrame, width = NS_TRIANGLE_VALUES_WIDTH)
        self.cValue.place(x = NS_TRIANGLE_C_VALUE_X, y =NS_TRIANGLE_C_VALUE_Y, anchor = "nw")


    def _bindSquare(self):
        print("Selected square!")

    def _bindRectangle(self):
        print("Selected rectangle!")

    def _bindHexagon(self):
        print("Selected hexagon!")

    def _bindCalc(self):
        if self.currentChoice == "Triangle":
            self.triangleObj = Triangle()
            self.triangleObj.a = self.aValue.get()
            self.triangleObj.b = self.bValue.get()
            self.triangleObj.c = self.cValue.get()



class SaveSession(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__( parent)
        self.controller = controller
        label = tkinter.Label(self, text="This is save session class")

class LoadSession(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tkinter.Label(self, text="This is loadSession class")


def main():
    app = Application(WINDOW_SIZE, WINDOW_TITLE, WINDOW_TRANSPARENCY)
    app.mainloop()


if __name__ == "__main__":
    main()
    