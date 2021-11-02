import tkinter
from tkinter.constants import  BOTH, E, EW, LEFT, NS, NW, S, SINGLE, VERTICAL, X, END
from constants import *
from tkinter.messagebox import askyesno, showerror, showwarning, showinfo
from tkinter import ttk
from PIL import ImageTk, Image
from figures import Triangle, Square, Hexagon
import fnmatch
import os
import json


class Application(tkinter.Tk):
    def __init__(self) :
        super().__init__()

        self.geometry(WINDOW_SIZE)
        self.title(WINDOW_TITLE)
        self.resizable(False, False)
        self.iconbitmap(r"img\icon.ico")
        self.attributes('-alpha', WINDOW_TRANSPARENCY)
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
        self.backFrame = tkinter.Frame(self)
        self.backFrame.place(x=0, y=0, anchor="nw", height=DEFAULT_FRAME_BACK_HEIGHT, width = WINDOW_WIDTH )
        self.backImg = Image.open(r"img\back.png") # PIL solution
        self.backImg = self.backImg.resize( (DEFAULT_BACK_IMAGE_WIDTH,DEFAULT_BACK_IMAGE_WIDTH), Image.ANTIALIAS) # resize
        self.backImg = ImageTk.PhotoImage(self.backImg) # # convert to PhotoImage
        self.back = tkinter.Label(self.backFrame, image=self.backImg)
        self.back.place(x = DEFAULT_BACK_IMAGE_X_POS, y = DEFAULT_BACK_IMAGE_Y_POS, anchor = "nw")
        self.back.focus_set()
        self.back.bind('<Button-1>', lambda l: controller.showFrame("MainMenu"))

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
        self.buttonsObjectDict[1].config(command = lambda: app.showFrame("NewSession") )

    def _bindNewSession(self, app):
        self.buttonsObjectDict[2].config(command = lambda: self.confirmationNewLoad(app, "NewSession") )

    def _bindSaveSession(self, app):
        self.buttonsObjectDict[3].config(state = self.saveState)
        self.buttonsObjectDict[3].config(command = lambda: app.showFrame("SaveSession") )

    def _bindLoadSession(self, app):
        self.buttonsObjectDict[4].config(command = lambda: [ self.confirmationNewLoad(app, "LoadSession"), app.frames["LoadSession"].loadList()  ])

    def _bindExit(self, app):
        self.buttonsObjectDict[5].config(command = app.destroy )

    def _bindButtons(self, app):
        self._bindContinue(app)
        self._bindNewSession(app)
        self._bindSaveSession(app)
        self._bindLoadSession(app)
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
            if (frameName == "NewSession"):
                app.frames["NewSession"]._clearValues()
                app.frames["NewSession"]._clearLabels()
                app.showFrame(frameName)
            elif (frameName == "LoadSession"):
                app.frames["NewSession"]._clearValues()
                app.frames["NewSession"]._clearLabels()
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
        self.valuesEntryDict = {}

        self.comboVar = tkinter.StringVar()
        self.combo = ttk.Combobox(self.dataFrame, textvariable = self.comboVar, width= NS_COMBO_WIDTH)
        self.combo['values'] = ("Triangle", "Square", "Hexagon")
        self.combo['state'] = 'readonly'
        self.combo.set("Triangle")
        self.combo.place(x= NS_COMBO_X_POS, y = NS_COMBO_Y_POS)

        self.selectButton = tkinter.Button(self.dataFrame, text="Select", width = NS_BUTTON_SELECT_WIDTH, pady = NS_BUTTON_Y_PADDING, command = self.bindSelect)
        self.selectButton.place(x = NS_BUTTON_SELECT_X_POS, y=NS_BUTTON_SELECT_Y_POS, anchor="nw")

        self.propertiesLabel = tkinter.Label(self.dataFrame, text="Properties")
        self.propertiesLabel.place(x=NS_LABEL_PROPERTIES_X_POS, y = NS_LABEL_PROPERTIES_Y_POS, anchor = 'nw')

        self.areaLabel = tkinter.Label(self.dataFrame, text = "Area:")
        self.areaLabel.place(x= NS_LABEL_PROPERTIES_X_POS, y = NS_AREA_LABEL_Y_POS, anchor = "nw")
        self.areaValue = tkinter.Entry(self.dataFrame, state = "normal", width = NS_ENTRY_VALUES_WIDTH)
        self.valuesEntryDict["area"] = self.areaValue
        self.areaValue.place(x =NS_ENTRY_VALUES_X, y= NS_AREA_LABEL_Y_POS, anchor = "nw")

        self.circumLabel = tkinter.Label(self.dataFrame, text = "Circumference:")
        self.circumLabel.place(x=NS_LABEL_PROPERTIES_X_POS, y =NS_CIRCUM_LABEL_Y_POS, anchor = "nw")
        self.circumValue = tkinter.Entry(self.dataFrame, state = "normal", width = NS_ENTRY_VALUES_WIDTH)
        self.valuesEntryDict["circum"] = self.circumValue
        self.circumValue.place(x =NS_ENTRY_VALUES_X, y= NS_CIRCUM_LABEL_Y_POS, anchor = "nw")

        self.rInscribedLabel = tkinter.Label(self.dataFrame, text = "Inscribed circle r:")
        self.rInscribedLabel.place(x=NS_LABEL_PROPERTIES_X_POS , y= NS_INSCR_LABEL_Y_POS, anchor = "nw")
        self.rInscribedValue = tkinter.Entry(self.dataFrame, state = "normal", width = NS_ENTRY_VALUES_WIDTH)
        self.valuesEntryDict["r"] = self.rInscribedValue
        self.rInscribedValue.place(x =NS_ENTRY_VALUES_X, y= NS_INSCR_LABEL_Y_POS, anchor = "nw")

        self.RCircumLabel = tkinter.Label(self.dataFrame, text = "Circumscribed circle R:")
        self.RCircumLabel.place(x=NS_LABEL_PROPERTIES_X_POS, y=NS_R_CIRCUM_LABEL_Y_POS, anchor = "nw")
        self.RCircumValue = tkinter.Entry(self.dataFrame, state = "normal", width = NS_ENTRY_VALUES_WIDTH)
        self.valuesEntryDict["R"] = self.RCircumValue
        self.RCircumValue.place(x =NS_ENTRY_VALUES_X, y= NS_R_CIRCUM_LABEL_Y_POS, anchor = "nw")

        #self.leftFrame = tkinter.Frame(self.dataFrame, bg= "blue")
        #self.leftFrame.place(x = NS_LEFT_FRAME_X, y = NS_LEFT_FRAME_Y, width= NS_LEFT_FRAME_WIDTH, height= NS_LEFT_FRAME_HEIGHT)

    def bindSelect(self, passedMethodName = None):
        self._clearValues()
        if (not passedMethodName):
            methodName = getattr(self, f"_bind{self.combo.get()}")
            methodName()
        else:
            passedMethodName()
        self.calcButton = tkinter.Button(self.dataFrame, text="Calculate", pady = NS_BUTTON_Y_PADDING, command = lambda: self._bindCalc() )
        self.calcButton.place(x = NS_CALC_BUTTON_X_POS, y = NS_CALC_BUTTON_Y_POS, anchor = "nw")

    def _clearValues(self):
        if self.currentChoice not in ("Triangle", "Square", "Hexagon"):
            return
        self._clearPropertiesEntryValues()
        if self.currentChoice == "Triangle":
            [item.destroy() for item in [self.aValue, self.bValue, self.cValue, self.triangle] ]
            try:
                del self.triangleObj
            except NameError:
                pass
        if self.currentChoice == "Square":
            [item.destroy() for item in [self.aValue, self.bValue, self.cValue, self.dValue, self.square] ]
            try:
                del self.squareObj
            except NameError:
                pass
        if self.currentChoice == "Hexagon":
            [item.destroy() for item in [self.aValue, self.bValue, self.cValue, self.dValue, self.eValue, self.fValue, self.hexagon] ]
            try:
                del self.hexagonObj
            except NameError:
                pass
        self.currentChoice = None

    def _clearPropertiesEntryValues(self):
        for entry in self.valuesEntryDict.values():
            entry.delete(0, END)

    def _bindTriangle(self):
        print("Selected triangle!")
        self.currentChoice = "Triangle"
        self.triangleObj = Triangle()
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
        self.currentChoice = "Square"
        self.squareObj = Square()
        self.img = Image.open(r"img\square.png") # PIL solution
        self.img = self.img.resize( (NS_SQUARE_IMAGE_WIDTH,NS_SQUARE_IMAGE_WIDTH), Image.ANTIALIAS) # resize
        self.img = ImageTk.PhotoImage(self.img) # # convert to PhotoImage
        self.square = tkinter.Label(self.dataFrame, image=self.img)
        self.square.place(x = NS_SQUARE_IMAGE_X, y = NS_SQUARE_IMAGE_Y, anchor = "nw")

        self.aValue = tkinter.Entry(self.dataFrame, width = NS_SQUARE_VALUES_WIDTH)
        self.aValue.place(x = NS_SQUARE_A_VALUE_X, y =NS_SQUARE_A_VALUE_Y, anchor = "nw")

        self.bValue = tkinter.Entry(self.dataFrame, width = NS_SQUARE_VALUES_WIDTH)
        self.bValue.place(x = NS_SQUARE_B_VALUE_X, y =NS_SQUARE_B_VALUE_Y, anchor = "nw")

        self.cValue = tkinter.Entry(self.dataFrame, width = NS_SQUARE_VALUES_WIDTH)
        self.cValue.place(x = NS_SQUARE_C_VALUE_X, y =NS_SQUARE_C_VALUE_Y, anchor = "nw")

        self.dValue = tkinter.Entry(self.dataFrame, width = NS_SQUARE_VALUES_WIDTH)
        self.dValue.place(x = NS_SQUARE_D_VALUE_X, y =NS_SQUARE_D_VALUE_Y, anchor = "nw")

    def _bindHexagon(self):
        print("Selected hexagon!")
        self.currentChoice = "Hexagon"
        self.hexagonObj = Hexagon()
        self.img = Image.open(r"img\hexagon.png") # PIL solution
        self.img = self.img.resize( (NS_HEXAGON_IMAGE_WIDTH,NS_HEXAGON_IMAGE_WIDTH), Image.ANTIALIAS) # resize
        self.img = ImageTk.PhotoImage(self.img) # # convert to PhotoImage
        self.hexagon = tkinter.Label(self.dataFrame, image=self.img)
        self.hexagon.place(x = NS_HEXAGON_IMAGE_X, y = NS_HEXAGON_IMAGE_Y, anchor = "nw")

        self.aValue = tkinter.Entry(self.dataFrame, width = NS_HEXAGON_VALUES_WIDTH)
        self.aValue.place(x = NS_HEXAGON_A_VALUE_X, y =NS_HEXAGON_A_VALUE_Y, anchor = "nw")

        self.bValue = tkinter.Entry(self.dataFrame, width = NS_HEXAGON_VALUES_WIDTH)
        self.bValue.place(x = NS_HEXAGON_B_VALUE_X, y =NS_HEXAGON_B_VALUE_Y, anchor = "nw")

        self.cValue = tkinter.Entry(self.dataFrame, width = NS_HEXAGON_VALUES_WIDTH)
        self.cValue.place(x = NS_HEXAGON_C_VALUE_X, y =NS_HEXAGON_C_VALUE_Y, anchor = "nw")

        self.dValue = tkinter.Entry(self.dataFrame, width = NS_HEXAGON_VALUES_WIDTH)
        self.dValue.place(x = NS_HEXAGON_D_VALUE_X, y =NS_HEXAGON_D_VALUE_Y, anchor = "nw")

        self.eValue = tkinter.Entry(self.dataFrame, width = NS_HEXAGON_VALUES_WIDTH)
        self.eValue.place(x = NS_HEXAGON_E_VALUE_X, y =NS_HEXAGON_E_VALUE_Y, anchor = "nw")

        self.fValue = tkinter.Entry(self.dataFrame, width = NS_HEXAGON_VALUES_WIDTH)
        self.fValue.place(x = NS_HEXAGON_F_VALUE_X, y =NS_HEXAGON_F_VALUE_Y, anchor = "nw")

    def _bindCalc(self):
        self._clearLabels()
        self._clearPropertiesEntryValues()
        if self.currentChoice == "Triangle":
            self._bindCalcTriangle()
        elif self.currentChoice == "Square":
            self._bindCalcSquare()
        elif self.currentChoice == "Hexagon":
            self._bindCalcHexagon()

    def _bindCalcTriangle(self):
        try:
            del self.triangleObj.a
        except AttributeError:
            pass
        try:
            del self.triangleObj.b
        except AttributeError:
            pass
        try:
            del self.triangleObj.c
        except AttributeError:
            pass

        self.triangleObj.a = self.aValue.get()
        self.triangleObj.b = self.bValue.get()
        self.triangleObj.c = self.cValue.get()
        try:
            [self.triangleObj.a, self.triangleObj.b, self.triangleObj.c]
        except AttributeError:
            print("At least one value could not be set")
            # show error label
            self.sidesNotSetLabel = tkinter.Label(self.dataFrame, text = "The sides could not be set!", fg="red")
            self.sidesNotSetLabel.place(x=NS_TRIANGLE_INEQ_LABEL_X_POS , y= NS_TRIANGLE_INEQ_LABEL_Y_POS, anchor = "nw")
            return

        if (not self.triangleObj.checkTriangleIneq()):
            # display warning message
            self.trIneqFalseLabel = tkinter.Label(self.dataFrame, text = "Provided values do not satifsy triangle inequality!", fg="red")
            self.trIneqFalseLabel.place(x=NS_TRIANGLE_INEQ_LABEL_X_POS , y= NS_TRIANGLE_INEQ_LABEL_Y_POS, anchor = "nw")
        else:
            self.circumValue.insert(0, self.triangleObj.circumference)
            self.areaValue.insert(0, self.triangleObj.area)
            self.rInscribedValue.insert(0, self.triangleObj.rInscribed)
            self.RCircumValue.insert(0, self.triangleObj.RCircum)

            self.successLabel = tkinter.Label(self.dataFrame, text = "Calculation success!", fg="green")
            self.successLabel.place(x=NS_TRIANGLE_INEQ_LABEL_X_POS , y= NS_TRIANGLE_INEQ_LABEL_Y_POS, anchor = "nw")

    def _bindCalcSquare(self):
        try:
            del self.squareObj.a
        except AttributeError:
            pass

        setVal = set( [self.aValue.get(), self.bValue.get(), self.cValue.get(), self.dValue.get()] ) 
        setValNoEmpty = setVal.difference({""})
        if len ( setValNoEmpty ) > 1:
            print("At least 2 contradictory sides' lengths set.")
            # show error label
            self.sidesContrLabel = tkinter.Label(self.dataFrame, text = "At least 2 contradictory sides' lengths set!", fg="red")
            self.sidesContrLabel.place(x=NS_SQUARE_CONTR_LABEL_X_POS , y= NS_SQUARE_CONTR_LABEL_Y_POS, anchor = "nw")
            return
        elif len ( setValNoEmpty ) == 0:
            self.sidesEmptyLabel = tkinter.Label(self.dataFrame, text = "Fill in at least 1 side!", fg="red")
            self.sidesEmptyLabel.place(x=NS_SQUARE_CONTR_LABEL_X_POS , y= NS_SQUARE_CONTR_LABEL_Y_POS, anchor = "nw")
            return
        
        self.squareObj.a = setValNoEmpty.pop()

        try:
            self.squareObj.a
        except AttributeError:
            print("Side value could not be set")
            # show error label
            self.sidesNotSetLabel = tkinter.Label(self.dataFrame, text = "The sides could not be set!", fg="red")
            self.sidesNotSetLabel.place(x=NS_SQUARE_CONTR_LABEL_X_POS , y= NS_SQUARE_CONTR_LABEL_Y_POS, anchor = "nw")
            return

        self.circumValue.insert(0, self.squareObj.circumference)
        self.areaValue.insert(0, self.squareObj.area)
        self.rInscribedValue.insert(0, self.squareObj.rInscribed)
        self.RCircumValue.insert(0, self.squareObj.RCircum)

        self.successLabel = tkinter.Label(self.dataFrame, text = "Calculation success!", fg="green")
        self.successLabel.place(x=NS_SQUARE_CONTR_LABEL_X_POS , y= NS_SQUARE_CONTR_LABEL_Y_POS, anchor = "nw")

    def _bindCalcHexagon(self):
        try:
            del self.hexagonObj.a
        except AttributeError:
            pass

        setVal = set( [self.aValue.get(), self.bValue.get(), self.cValue.get(), self.dValue.get(), self.eValue.get(), self.fValue.get()] ) 
        setValNoEmpty = setVal.difference({""})
        if len ( setValNoEmpty ) > 1:
            print("At least 2 contradictory sides' lengths set.")
            # show error label
            self.sidesContrLabel = tkinter.Label(self.dataFrame, text = "At least 2 contradictory sides' lengths set!", fg="red")
            self.sidesContrLabel.place(x=NS_SQUARE_CONTR_LABEL_X_POS , y= NS_SQUARE_CONTR_LABEL_Y_POS, anchor = "nw")
            return
        elif len ( setValNoEmpty ) == 0:
            self.sidesEmptyLabel = tkinter.Label(self.dataFrame, text = "Fill in at least 1 side!", fg="red")
            self.sidesEmptyLabel.place(x=NS_SQUARE_CONTR_LABEL_X_POS , y= NS_SQUARE_CONTR_LABEL_Y_POS, anchor = "nw")
            return
        
        self.hexagonObj.a = setValNoEmpty.pop()

        try:
            self.hexagonObj.a
        except AttributeError:
            print("Side value could not be set")
            # show error label
            self.sidesNotSetLabel = tkinter.Label(self.dataFrame, text = "The sides could not be set!", fg="red")
            self.sidesNotSetLabel.place(x=NS_SQUARE_CONTR_LABEL_X_POS , y= NS_SQUARE_CONTR_LABEL_Y_POS, anchor = "nw")
            return

        self.circumValue.insert(0, self.hexagonObj.circumference)
        self.areaValue.insert(0, self.hexagonObj.area)
        self.rInscribedValue.insert(0, self.hexagonObj.rInscribed)
        self.RCircumValue.insert(0, self.hexagonObj.RCircum)

        self.successLabel = tkinter.Label(self.dataFrame, text = "Calculation success!", fg="green")
        self.successLabel.place(x=NS_SQUARE_CONTR_LABEL_X_POS , y= NS_SQUARE_CONTR_LABEL_Y_POS, anchor = "nw")

    def _clearLabels(self):
        try:
            self.successLabel.destroy()
        except AttributeError:
            pass
        try:
            self.sidesNotSetLabel.destroy()
        except AttributeError:
            pass
        if (self.currentChoice == "Triagle"):
            try:
                self.trIneqFalseLabel.destroy()
            except AttributeError:
                pass
        elif (self.currentChoice in ("Hexagon", "Square")):
            try:
                self.sidesEmptyLabel.destroy()
            except AttributeError:
                pass
            try:
                self.sidesContrLabel.destroy()
            except AttributeError:
                pass

class SaveSession(DefaultFrame):
    def __init__(self, parent, controller):
        super().__init__( parent, controller)
        self.controller = controller
        self.data = {}

        self.saveLabel = tkinter.Label(self.dataFrame, text = "Enter the name of the file:")
        self.saveLabel.place(x = SF_LABEL_POS_X, y = SF_LABEL_POS_Y, anchor = "nw")

        self.saveEntry = tkinter.Entry(self.dataFrame, width = SF_ENTRY_WIDTH)
        self.saveEntry.place(x = SF_LABEL_POS_X, y = SF_ENTRY_POS_Y, anchor = "nw")

        self.saveButton = tkinter.Button(self.dataFrame, text = "Save", width =SF_BUTTON_WIDTH, pady= NS_BUTTON_Y_PADDING, command = self.saveAction )
        self.saveButton.place(x = SF_LABEL_POS_X, y = SF_BUTTON_POS_Y, anchor = "nw")

    def gatherData(self):
        self.data["sides"] = {}
        self.data["sides"]["a"] = self.controller.frames["NewSession"].aValue.get()
        self.data["sides"]["b"] = self.controller.frames["NewSession"].bValue.get()
        self.data["sides"]["c"] = self.controller.frames["NewSession"].cValue.get()
        if (self.data["objectType"] == "Triangle"):
            pass
        elif(self.data["objectType"] == "Square"):
            self.data["sides"]["d"] = self.controller.frames["NewSession"].dValue.get()
        elif(self.data["objectType"] == "Hexagon"):
            self.data["sides"]["d"] = self.controller.frames["NewSession"].dValue.get()
            self.data["sides"]["e"] = self.controller.frames["NewSession"].eValue.get()
            self.data["sides"]["f"] = self.controller.frames["NewSession"].fValue.get()

    def saveAction(self):
        self.fileName = self.saveEntry.get()
        self.data["objectType"] = self.controller.frames["NewSession"].currentChoice
        if (not self.data["objectType"]):
            showwarning("No object selected", "The file cannot be saved, as not geometric figure has been selected.")
            return
        self.gatherData()
        if (f"{self.fileName}.json" in os.listdir('./saves')):
            answer = askyesno(title='Overwrite?', message='The files with such a name already exists.\nWould you like to overwrite?')
        else:
            answer = True
        if (answer):
            with open(f'./saves/{self.fileName}.json', 'w') as f:
                try:
                    json.dump(self.data, f, ensure_ascii=False)
                    showinfo("Success", "Data written successfully.")
                except:
                    showerror("Failure", "Error writing to a file.")
        else:
            return


class LoadSession(DefaultFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.savesList = []
        self._createListbox()

        self.loadButton = tkinter.Button(self.innerFrame, text = "Load", width = SF_BUTTON_WIDTH, pady= NS_BUTTON_Y_PADDING, command =  self.importData)
        self.loadButton.grid(column = 0, row = 1)

    def _createListbox(self):
        savesVar = tkinter.StringVar(value=self.savesList)
        self.innerFrame = tkinter.Frame(self.dataFrame)
        self.loadListbox = tkinter.Listbox(self.innerFrame, height = LF_LISTBOX_HEIGHT, selectmode=SINGLE, width= LF_LISTBOX_WIDTH)
        self.scrollbar = tkinter.Scrollbar(self.innerFrame, orient=VERTICAL, command = tkinter.Listbox.yview)
        self.loadListbox['yscrollcommand'] = self.scrollbar.set

        self.innerFrame.pack()
        self.loadListbox.grid(column = 0, row = 0 )
        self.scrollbar.grid(column = 1, row = 0, sticky = "ns")

    def _loadSaveList(self):
        self.savesList = []
        for file in os.listdir('./saves'):
            if fnmatch.fnmatch(file, '*.json'):
                self.savesList.append(file)
        self.savesVar = tkinter.StringVar(value = self.savesList)

    def loadList(self):
        self._loadSaveList()
        self.loadListbox.config(listvariable=self.savesVar)

    def importData(self):
        selected_index = self.loadListbox.curselection()
        filename = self.loadListbox.get(selected_index)
        with open(f'./saves/{filename}', 'r') as f:
            try:
                self.data = json.load(f)
                self.loadDataToView()
                showinfo("Success", "Data loaded successfully.")
                self.controller.showFrame("NewSession")
            except:
                showerror("Failure", "Error loading the file.")

    def loadDataToView(self):
        if (self.data["objectType"] == "Triangle"):
            self.controller.frames["NewSession"].bindSelect(  self.controller.frames["NewSession"]._bindTriangle )
        elif (self.data["objectType"] == "Square"):
            self.controller.frames["NewSession"].bindSelect(  self.controller.frames["NewSession"]._bindSquare )
            self.controller.frames["NewSession"].dValue.insert(0, self.data["sides"]["d"])
        elif (self.data["objectType"] == "Hexagon"):
            self.controller.frames["NewSession"].bindSelect(  self.controller.frames["NewSession"]._bindHexagon )
            self.controller.frames["NewSession"].dValue.insert(0, self.data["sides"]["d"])
            self.controller.frames["NewSession"].eValue.insert(0, self.data["sides"]["e"])
            self.controller.frames["NewSession"].fValue.insert(0, self.data["sides"]["f"])
        self.controller.frames["NewSession"].aValue.insert(0, self.data["sides"]["a"])
        self.controller.frames["NewSession"].bValue.insert(0, self.data["sides"]["b"])
        self.controller.frames["NewSession"].cValue.insert(0, self.data["sides"]["c"])

def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
    