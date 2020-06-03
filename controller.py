import tkinter as tk
import pandas as pd
from tkinter.filedialog import askopenfilename
import tkinter.simpledialog as simpledialog
import configparser

from model import Model
from view import View
from popup import Popup
from plot import Plot

class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.model = Model()
        self.view = View(self.root, self.model, self)
        self.popup = Popup(self.model)
        self.plot = Plot(self.model)
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        
    def run(self):
        """Run the program by calling the mainloop of Tk."""
        self.root.mainloop()

    def openFile(self):
        """Open the file and present data in the table."""
        self.filepath = askopenfilename(
            #("Text Files", "*.txt"),
            filetypes=[("All Files", "*.*")])
        sep = self.config["default"]["sep"]
        sep = sep[1:-1]
        with open(self.filepath, "r") as input_file:
            df = pd.read_csv(input_file, sep=sep, engine= "python", skip_blank_lines=True)
        if not self.filepath:
            return    
        self.model.dictdata.clear()
        self.model.storeRecords(df)
        self.view.showData()
        self.view.setTitle()

    #http://dmnfarrell.github.io/tkintertable/Tables.html#tkintertable.Tables.TableCanvas.findValue
    def findValue(self, searchstring=None, findagain=None):
        """Return the row/col for the input value"""

        if searchstring == None:
            searchstring = simpledialog.askstring("Search table",
                                            "Enter search value:",
                                            parent=self.view.frame_table)
        found=0
        if findagain == None or not hasattr(self,"foundlist"):
            self.foundlist=[]
        if (self.model.dictdata!=None) and (searchstring!=None):
            for row in range(self.view.table.rows):
                for col in range(self.view.table.cols):
                    text = str(self.view.table.model.getValueAt(row,col))
                    if text=="" or text==None:
                        continue
                    cell=row,col
                    if findagain == 1 and cell in self.foundlist:
                        continue
                    if text.lower().find(searchstring.lower())!=-1:
                        print ("Found in",row,col)
                        found=1
                        #highlight cell
                        self.view.showSearchResult(row, col)
                        #add row/col to foundlist
                        self.foundlist.append(cell)
                        return row, col
        if found==0:
            self.view.table.delete("searchrect")
            print ("Nothing found")
            return None

    def getMinMax(self):
        """Show min and max value of "Some numbers" column in a popup window."""
        #get data
        columnName = self.model.labels[0]
        column = self.model.getColumn(columnName)
        self.model.setMinMax(column)
        #open popup
        self.popup.show()
    
    def openPlot(self):
        """Select data from "Some numbers" column and show it in a plot. """
        columnName = self.model.labels[0]
        column = self.model.getColumn(columnName)
        self.plot.show(column, columnName)