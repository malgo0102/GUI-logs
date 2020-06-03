import configparser
import json

class Model:
    def __init__(self):
        self.dictdata = {}
        self.minval = None
        self.maxval = None

        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        
        self.labels = json.loads(self.config.get("default","labels"))

    def storeRecords(self, df):
        """
        Takes a DataFrame as a parameter.

        Return a dictionary.

        Returned nested dictionary is used to insert data into a table and in the findValue().
        """
        #     Dictionary form: 
        #     data = {'rec1': {'label1': 99.88, 'label2': 108.79, 'label3': 'something'},
        #        'rec2': {'label1': 88.00, 'label2': 100.79, 'label3': 'something else'}} 
        count = 0        
        for (index, rec) in df.iterrows():
            dictrecords = {}
            j = 0
            for element in rec:
                dictrecords[self.labels[j]] = element
                j = j + 1
                # j += j
            self.dictdata[count] = dictrecords
            count = count + 1
        return self.dictdata

    def getColumn(self, columnName):
        """
        Return a list with a column data.

        Uses data from the dictionary obtained from storeRecords().
        """
        #https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-15.php
        rows = map(lambda key: self.dictdata[key], self.dictdata)
        #turn stream of objects obtained from map into a list, so this data is accesible for multiple operations. Without list() after computing min(), the max() would give a ValueError: max() arg is an empty sequence
        column = list(map(lambda row: row[columnName], rows))

        return column

    def setMinMax(self, column):
        """Set min and max value of a column."""
        self.minval = min(column)
        self.maxval = max(column)
        print("Min: %d Max: %d" %(self.minval, self.maxval))





