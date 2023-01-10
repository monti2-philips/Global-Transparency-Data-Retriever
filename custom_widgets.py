'''
Source: https://www.youtube.com/watch?v=WnHkx-AvTBA

Custom widget to create DropDown Box with Checks for selecting resources
'''

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, \
                            QVBoxLayout, QComboBox, QPushButton
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QStandardItem

class CheckableComboBox(QComboBox):
    def __init__(self, QWidgets):
        super().__init__(QWidgets)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.closeOnLineEditClick = False

        self.lineEdit().installEventFilter(self)
        self.view().viewport().installEventFilter(self)

        self.model().dataChanged.connect(self.updateLineEditField)

        self.resourceList = []
        self.default_resource = 'ANY RESOURCE'
        self.lineEdit().setText(self.default_resource)
        

    def eventFilter(self, widget, event):
        if widget == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return super().eventFilter(widget, event)

        if widget == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                indx = self.view().indexAt(event.pos())
                item = self.model().item(indx.row())

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
            return super().eventFilter(widget, event)

    def hidePopup(self):
        super().hidePopup()
        self.startTimer(100)

    def reset(self):
        self.clear()
        self.addItems(self.prev_items)

    def addItems(self, items, itemList=None):
        self.resourceList = [self.default_resource]
        for indx, text in enumerate(items):
            try:
                data = itemList[indx]
            except (TypeError, IndexError):
                data=None
            self.addItem(text,data)
        self.lineEdit().setText(self.default_resource)

        self.prev_items = items

    def addItem(self, text, userData=None):
        item = QStandardItem()
        item.setText(text)
        if not userData is None:
            item.setData(userData)
        
        # enable checkbox setting
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)
    
    def updateLineEditField(self):
        self.resourceList = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                self.resourceList.append(self.model().item(i).text())
        if len(self.resourceList) > 1:
            # text_string = ', '.join(self.resourceList)
            self.lineEdit().setText('Multiple Resources')
        elif len(self.resourceList) == 1:
            self.lineEdit().setText(self.resourceList[0])
        else:
            self.lineEdit().setText(self.default_resource)
            self.resourceList = [self.default_resource]

if __name__ == '__main__':
    import sys
    choices = ["R_RT_1","R_RT_2","R_RT_3","R_RT_4","R_RT_5",
            "R_RT_6","R_RT_7","R_RT_8","R_MES_ADMIN"]

    class MyApp(QWidget):
        def __init__(self,):
            super().__init__()
            self.window_width, self.window_height = 500, 200
            self.setMinimumSize(self.window_width,self.window_height)
            self.setStyleSheet('''
            QWidget {
                font-size: 15px;
            }
            ''')
            self.layout = QVBoxLayout()
            self.setLayout(self.layout)

            combobox = CheckableComboBox()
            combobox.addItems(choices)
            self.layout.addWidget(combobox)

            btn = QPushButton('Push', clicked=lambda: print(tuple(combobox.resourceList)))
            self.layout.addWidget(btn)

            rset = QPushButton('Reset', clicked=lambda: combobox.reset())
            self.layout.addWidget(rset)
    
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')