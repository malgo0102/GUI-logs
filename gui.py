import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
#https://github.com/dmnfarrell/tkintertable/wiki/Usage
from tkintertable import TableCanvas, TableModel
# python -m tkinter : demonstrate tkinter is properly installed
import tkinter.simpledialog as simpledialog
import pandas as pd

#allow global values accesible across methods
table = None
dictdata = {}



def showData():
    """Open file and show data in the window"""
    df = openFile()
    dictentries = storeRecords(df)
    insertData(dictentries)

#https://realpython.com/python-gui-tkinter/
def openFile(sep="  |=| - | "):
    """
    Open file for reading. Parse file.
    
    Returns Data Frame. 
    """
    filepath = askopenfilename(
        #("Text Files", "*.txt"),
        filetypes=[("All Files", "*.*")]
    )
    if not filepath:
        return
    
    window.title(f"Log Viewer - {filepath}")

    with open(filepath, "r") as input_file:
        df = pd.read_csv(input_file, sep=sep, engine= "python", skip_blank_lines=True)

    return df
    

#create a nested dictionary with parsed records
#https://github.com/dmnfarrell/tkintertable/wiki/Usage
def storeRecords(df, labels=["Some number", "Thread id", "Log level", "Type", "Parameter", "Param value"]):
    """
    Takes DataFrame as a parameter.

    Returns a dictionary.

    The nested dictionary is used to insert data into a table.

    Dictionary form: 
    data = {'rec1': {'label1': 99.88, 'label2': 108.79, 'label3': 'something'},
       'rec2': {'label1': 88.00, 'label2': 100.79, 'label3': 'something else'}
       } 
    """
    global dictdata
    count = 0
    for (index, rec) in df.iterrows():
        dictrecords = {}
        j = 0
        for element in rec:
            dictrecords[labels[j]] = element
            j = j + 1
        dictdata[count] = dictrecords
        count = count + 1
    return dictdata

def insertData(dictdata):
    """
    Insert dictionary data into a table.

    Show table.    
    """
    global table
    table = TableCanvas(fr_table, data=dictdata, read_only=True)
    table.adjustColumnWidths()
    table.show()
    

#findValue() from http://dmnfarrell.github.io/tkintertable/Tables.html#tkintertable.Tables.TableCanvas.findValue
def findValue(searchstring=None, findagain=None):
    """ 
    Search functionality.

    Returns row and column of searched value.
    """
    global table
    if searchstring == None:
        searchstring = simpledialog.askstring("Search table", "Enter search value:", parent=fr_table)
    found=0
    if findagain == None or not hasattr(fr_table,'foundlist'):
        table.foundlist=[]
    if table.model!=None:
        for row in range(table.rows):
            for col in range(table.cols):
                text = str(table.model.getValueAt(row,col))
                if text=='' or text==None:
                    continue
                cell=row,col
                if findagain == 1 and cell in table.foundlist:
                    continue
                if text.lower().find(searchstring.lower())!=-1:
                    print ('found in',row,col)
                    found=1
                    #highlight cell
                    table.delete('searchrect')
                    table.drawRect(row, col, color='red', tag='searchrect', delete=0)
                    table.lift('searchrect')
                    table.lift('celltext'+str(col)+'_'+str(row))
                    #add row/col to foundlist
                    table.foundlist.append(cell)
                    #need to scroll to centre the cell here..
                    x,y = table.getCanvasPos(row, col)
                    table.xview('moveto', x)
                    table.yview('moveto', y)
                    table.tablecolheader.xview('moveto', x)
                    table.tablerowheader.yview('moveto', y)
                    return row, col
    if found==0:
        table.delete('searchrect')
        print ('nothing found')
        return None

def getMinMax():
    """
    Pops up a new window with min and max values from the "Some number" column.
    
    Uses data from a dictionary obtained from storeRecords().
    """
    global dictdata
 
    #https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-15.php
    rows = map(lambda key: dictdata[key], dictdata)
    #turn stream of objects obtained from map into a list, so this data is accesible for multiple operations. Without list() after computing min(), the max() would give a ValueError: max() arg is an empty sequence
    column = list(map(lambda row: row["Some number"], rows))
    minval = min(column)
    maxval = max(column)
    print("Min: %d Max: %d" %(minval, maxval))

    msg = "Minimum value for \"Some number\" is: %d\nMaximum value \"Some number\" is: %d" %(minval, maxval)
    popup = tk.Tk()
    popup.geometry("300x100")
    popup.wm_title("Statistics")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    btn_OK = tk.Button(popup, text="OK", command = popup.destroy)
    btn_OK.pack()
    popup.mainloop()



            
    

#set window, row and column config
#https://realpython.com/python-gui-tkinter/#getting-user-input-with-entry-widgets
window = tk.Tk()  
window.title("Log viewer")
window.rowconfigure(0, minsize=800, weight=1) 
window.columnconfigure(1, minsize=800, weight=1) 

#create widget: table
#http://dmnfarrell.github.io/tkintertable/TableModels.html
fr_table = tk.Frame(window)
#add the frame to the parent
table = TableCanvas(fr_table)
table.show()

#create widget: buttons
fr_buttons = tk.Frame(window)
#btn_open have master attribute set to fr_buttons
btn_open = tk.Button(fr_buttons, text="Open", command=showData)
btn_search = tk.Button(fr_buttons, text="Search", command=findValue)
btn_statistics = tk.Button(fr_buttons, text="Statistics", command=getMinMax)
#set up the grid in the frame with geometry manager
#sticky="ew" expand buttons horizontally
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_search.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_statistics.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

#set up the frames in the window with .pack()     
fr_buttons.pack(side=tk.LEFT, fill=tk.BOTH)
fr_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



window.mainloop()