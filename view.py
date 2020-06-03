import tkinter as tk
from tkinter.filedialog import askopenfilename
#https://github.com/dmnfarrell/tkintertable/wiki/Usage
from tkintertable import TableCanvas, TableModel
# python -m tkinter : demonstrate tkinter is properly installed

from popup import Popup

class View:
    def __init__(self, root, model, controller):
        self.model = model
        self.root = root
        self.controller = controller
        self.popup = Popup(model)

        # Table setup
        self.frame_table = tk.Frame(root)
        self.table = TableCanvas(self.frame_table)
        self.table.show()

        self.frame_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Buttons setup
        self.frame_buttons = tk.Frame(root)
        # Event handlers
        self.btn_open = tk.Button(self.frame_buttons, text="Open", command=self.controller.openFile)
        self.btn_search = tk.Button(self.frame_buttons, text="Search", command=self.controller.findValue)
        self.btn_statistics = tk.Button(self.frame_buttons, text="Statistics", command=self.controller.getMinMax)
        self.btn_plot = tk.Button(self.frame_buttons, text="Show plot", command=self.controller.openPlot)

        # Grid setup
        self.btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_search.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.btn_statistics.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.btn_plot.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        self.frame_buttons.pack(side=tk.LEFT, fill=tk.BOTH)

        #Window setup
        self.root.rowconfigure(0, minsize=800, weight=1)
        self.root.columnconfigure(1, minsize=800, weight=1)
        self.root.title("Log viewer")

    #Methods
    def showData(self):
        """Show data in te table"""
        self.table = TableCanvas(self.frame_table, data=self.model.dictdata, read_only=True)
        self.table.adjustColumnWidths()
        self.table.show()

    def setTitle(self):
        """Set root title with filepath"""
        self.root.title(f"Log Viewer - {self.controller.filepath}")

    def showSearchResult(self, row, col):
        """Show cell with search result in the table"""
        self.table.delete('searchrect')
        self.table.drawRect(row, col, color='red', tag='searchrect', delete=0)
        self.table.lift('searchrect')
        self.table.lift('celltext'+str(col)+'_'+str(row))

