import pandas as pd

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

class TableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = pd.DataFrame(data= {
            "Time (min)": [],
            "[Start] (mM)": [],
            "[End] (mM)": []
        })
        
    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
            """Override method from QAbstractTableModel

            Return data cell from the pandas DataFrame
            """
            if not index.isValid():
                return None

            if role == Qt.DisplayRole:
                return str(self._dataframe.iloc[index.row(), index.column()])

            return None

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
            """Override method from QAbstractTableModel

            Return column count of the pandas DataFrame
            """
            if parent == QModelIndex():
                return len(self._dataframe.columns)
            return 0
        
    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])

        return None
    
    def insertRows(self, row: int, count: int, parent: QModelIndex = QModelIndex()) -> bool:
        if self.beginInsertRows(parent, row, row+count-1):
            for i in range(count):
                new_index = f'New Index{i}'
                self.table_index.loc[new_index] = ['<empty>']*self.columnCount(parent)
            return self.endInsertRows()
        else:
            return False
    
    def removeRows(self, position, rows, parent=QModelIndex()):
        start, end = position, position + rows - 1
        if 0 <= start <= end and end < self.rowCount(parent):
            self.beginRemoveRows(parent, start, end)
            for index in range(start, end + 1):
                self._data.drop(index, inplace=True)
            self._data.reset_index(drop=True, inplace=True)
            self.endRemoveRows()
            return True
        return False
        
    def add_segment(self, seg):
        self._dataframe.loc[len(self._dataframe)] = seg
        self.layoutChanged.emit()
    
    def get_segments(self):
        return self._dataframe    
    
    def clear_segments(self):   
        self._dataframe = pd.DataFrame(
            data= {
                "Time": [],
                "Start Conc.": [],
                "End Conc.": []
        })
        self.layoutChanged.emit()
    
    #def headerData(self, section, orientation, role=Qt.DisplayRole):
    #    if orientation == Qt.Horizontal and role == Qt.DisplayRole:
    #        if section == 0:
    #            return "Time"
    #        elif section == 1:
    #            return "Start Conc."
    #        elif section == 2:
    #            return "End Conc."

 #       return super().headerData(section, orientation, role)