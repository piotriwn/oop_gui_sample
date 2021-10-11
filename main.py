import tkinter
from constants import *

class Application(tkinter.Tk):
    def __init__(self, winSize, winTitle, transparency) :
        super().__init__()

        self.geometry(winSize)
        self.title(winTitle)
        self.resizable(False, False)
        self.iconbitmap(r"img\icon.ico")
        self.attributes('-alpha', transparency)


class DefaultFrame(tkinter.Frame):
    # clears all widgets in frame
    def clearFrame(self):
        for widget in self.winfo_children():
            widget.destroy()

class MainMenu(DefaultFrame):
    def __init__(self, defaultFrame, buttonsDataDict):
        super().__init__(defaultFrame)
        self.buttonsDataDict = buttonsDataDict # this only copies from constants and its values are strings
        self.buttonsObjectDict = {} # values are button objects
        self.continueState = "disabled" # when you first start the program, continue and save buttons are disabled
        self.saveState = "disabled"

    def createButtons(self, yButtonPadding = 5, buttonWidth = 30):
        for k, v in self.buttonsDataDict.items():
            self.buttonsObjectDict[k] = tkinter.Button(self, text=v, width= buttonWidth, pady = yButtonPadding) # container is self - that is, MainMenu instance
    
    def _bindContinue(self):
        self.buttonsObjectDict[1].config(state = self.continueState)
    
    def _bindNewSession(self):
        pass

    def _bindSaveSession(self):
        self.buttonsObjectDict[3].config(state = self.saveState)

    def _bindLoadSession(self):
        pass

    def _bindExit(self, app):
        self.buttonsObjectDict[5].config(command = app.destroy )

    def _bindButtons(self, app):
        self._bindContinue()
        self._bindNewSession()
        self._bindSaveSession()
        self._bindLoadSession()
        self._bindExit(app)

    def deployButtons(self, app, yGridPadding = 5):
        for k, v in self.buttonsObjectDict.items():
            v.grid(row = k, column = 0, pady = yGridPadding)
        self._bindButtons(app)



def main():
    app = Application(WINDOW_SIZE, WINDOW_TITLE, WINDOW_TRANSPARENCY)

    defaultFrame = DefaultFrame(app)
    defaultFrame.pack(fill='both', expand=True, padx = DEFAULT_FRAME_X_PADDING, pady = DEFAULT_FRAME_Y_PADDING)

    mainMenu = MainMenu(defaultFrame, MM_BUTTONS_DICT)
    mainMenu.pack(expand=True)
    mainMenu.createButtons(MAIN_MENU_BUTTON_Y_PADDING, MAIN_MENU_BUTTON_WIDTH)
    mainMenu.deployButtons(app, MAIN_MENU_BUTTON_GRID_PADDING)

    app.mainloop()


if __name__ == "__main__":
    main()
    