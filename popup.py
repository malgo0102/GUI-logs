import tkinter as tk

class Popup:
    def __init__(self, model):
        self.model = model

    def show(self):
        """Show popup with min and max value"""
        #popup
        self.popup = tk.Tk()
        self.popup.geometry("300x100")
        self.popup.wm_title("Statistics")
        self.msg = "Minimum value for \"Some number\" is: %d\nMaximum value for \"Some number\" is: %d" %(self.model.minval, self.model.maxval)
        self.label = tk.Label(self.popup, text=self.msg)
        self.label.pack(side="top", fill="x", pady=10)
        self.btn_OK = tk.Button(self.popup, text="OK", command = self.popup.destroy)
        self.btn_OK.pack()

            