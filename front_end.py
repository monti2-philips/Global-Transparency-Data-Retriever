"""
Front End file for GUI - Generated from QtDesigner Application and then altered.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from custom_widgets import CheckableComboBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        # Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(900, 850)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setToolTip("")
        MainWindow.setToolTipDuration(-1)

        # Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Test Checkboxes
        self.testBox = QtWidgets.QGroupBox(self.centralwidget)
        self.testBox.setGeometry(QtCore.QRect(20, 80, 316, 66))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.testBox.sizePolicy().hasHeightForWidth())
        self.testBox.setSizePolicy(sizePolicy)
        self.testBox.setObjectName("testBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.testBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.acousticBool = QtWidgets.QCheckBox(self.testBox)
        self.acousticBool.setChecked(True)
        self.acousticBool.setObjectName("acousticBool")
        self.horizontalLayout.addWidget(self.acousticBool)
        self.aimBool = QtWidgets.QCheckBox(self.testBox)
        self.aimBool.setChecked(True)
        self.aimBool.setObjectName("aimBool")
        self.horizontalLayout.addWidget(self.aimBool)
        self.rfbBool = QtWidgets.QCheckBox(self.testBox)
        self.rfbBool.setChecked(True)
        self.rfbBool.setObjectName("rfbBool")
        self.horizontalLayout.addWidget(self.rfbBool)
        self.thermalBool = QtWidgets.QCheckBox(self.testBox)
        self.thermalBool.setChecked(True)
        self.thermalBool.setObjectName("thermalBool")
        self.horizontalLayout.addWidget(self.thermalBool)

        # Query Radio Buttons
        self.queryBox = QtWidgets.QGroupBox(self.centralwidget)
        self.queryBox.setGeometry(QtCore.QRect(20, 10, 352, 66))
        self.queryBox.setObjectName("queryBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.queryBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.variantBool = QtWidgets.QRadioButton(self.queryBox)
        self.variantBool.setChecked(True)
        self.variantBool.setObjectName("variantBool")
        self.horizontalLayout_2.addWidget(self.variantBool)
        self.referenceBool = QtWidgets.QRadioButton(self.queryBox)
        self.referenceBool.setObjectName("referenceBool")
        self.horizontalLayout_2.addWidget(self.referenceBool)

        # Data Input
        self.dataBox = QtWidgets.QGroupBox(self.centralwidget)
        self.dataBox.setGeometry(QtCore.QRect(20, 150, 490, 342))
        self.dataBox.setObjectName("dataBox")
        
        # Work Order Input
        self.workOrderInput = QtWidgets.QPlainTextEdit(self.dataBox)
        self.workOrderInput.setEnabled(True)
        self.workOrderInput.setGeometry(QtCore.QRect(20, 145, 450, 70))
        self.workOrderInput.setToolTip("")
        self.workOrderInput.setToolTipDuration(-1)
        self.workOrderInput.setObjectName("workOrderInput")
        self.workOrderLabel = QtWidgets.QLabel(self.dataBox)
        self.workOrderLabel.setGeometry(QtCore.QRect(20, 115, 122, 21))
        self.workOrderLabel.setToolTipDuration(-1)
        self.workOrderLabel.setObjectName("workOrderLabel")

        # Reset Button
        self.inputReset = QtWidgets.QPushButton(self.dataBox)
        self.inputReset.setGeometry(QtCore.QRect(20, 290, 450, 30))
        self.inputReset.setObjectName("inputReset")

        # Part Number Input
        self.partNumberLabel = QtWidgets.QLabel(self.dataBox)
        self.partNumberLabel.setGeometry(QtCore.QRect(20, 30, 131, 21))
        self.partNumberLabel.setToolTipDuration(-1)
        self.partNumberLabel.setObjectName("partNumberLabel")
        self.partNumberInput = QtWidgets.QLineEdit(self.dataBox)
        self.partNumberInput.setEnabled(True)
        self.partNumberInput.setGeometry(QtCore.QRect(20, 60, 150, 25))
        self.partNumberInput.setText("")
        self.partNumberInput.setMaxLength(12)
        self.partNumberInput.setObjectName("partNumberInput")

        # Min Date Input
        self.minDateInput = QtWidgets.QDateEdit(self.dataBox)
        self.minDateInput.setEnabled(False)
        self.minDateInput.setGeometry(QtCore.QRect(20, 250, 125, 27))
        self.minDateInput.setAcceptDrops(False)
        self.minDateInput.setMinimumDate(QtCore.QDate(2022, 1, 1))
        self.minDateInput.setMaximumDate(QtCore.QDate.currentDate().addDays(-1))
        self.minDateInput.setCurrentSection(
            QtWidgets.QDateTimeEdit.YearSection)
        self.minDateInput.setCalendarPopup(True)
        self.minDateInput.setDate(QtCore.QDate(2022, 1, 1))
        self.minDateInput.setObjectName("minDateInput")
        self.minDateLabel = QtWidgets.QLabel(self.dataBox)
        self.minDateLabel.setGeometry(QtCore.QRect(20, 220, 146, 21))
        self.minDateLabel.setObjectName("minDateLabel")

        # Max Date Input
        self.maxDateLabel = QtWidgets.QLabel(self.dataBox)
        self.maxDateLabel.setGeometry(QtCore.QRect(200, 220, 148, 21))
        self.maxDateLabel.setObjectName("maxDateLabel")
        self.maxDateInput = QtWidgets.QDateEdit(self.dataBox)
        self.maxDateInput.setEnabled(False)
        self.maxDateInput.setGeometry(QtCore.QRect(200, 250, 125, 27))
        self.maxDateInput.setAcceptDrops(False)
        self.maxDateInput.setMinimumDate(QtCore.QDate(2022, 1, 2))
        self.maxDateInput.setCurrentSection(
            QtWidgets.QDateTimeEdit.YearSection)
        self.maxDateInput.setCalendarPopup(True)
        # self.maxDateInput.setDate(QtCore.QDate(2022, 1, 2))
        self.maxDateInput.setDate(QtCore.QDate.currentDate())
        self.maxDateInput.setObjectName("maxDateInput")

        # Execute Query Button
        self.executeButton = QtWidgets.QPushButton(self.centralwidget)
        self.executeButton.setGeometry(QtCore.QRect(20, 500, 490, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.executeButton.setFont(font)
        self.executeButton.setObjectName("executeButton")

        # Instructions Label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(540, 20, 340, 500))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setScaledContents(True)
        self.label.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # Table Content Font
        font2 = QtGui.QFont()
        font2.setFamily(u"Calibri")
        font2.setPointSize(8)
        # Table Header Font
        font3 = QtGui.QFont()
        font3.setFamily(u"Calibri")
        font3.setPointSize(10)
        font3.setBold(True)
        
        # Data Preview
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QtCore.QRect(20, 540, 850, 250))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        
        # Acoustic Tab
        self.acousticTab = QtWidgets.QWidget()
        self.acousticTab.setObjectName(u"acousticTab")
        self.acousticView = QtWidgets.QTableView(self.acousticTab)
        self.acousticView.setObjectName(u"acousticView")
        self.acousticView.setGeometry(QtCore.QRect(0, 0, 844, 216))
        self.acousticView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.acousticView.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.acousticView.setFont(font2)
        self.acousticView.horizontalHeader().setFont(font3)
        self.acousticView.setAlternatingRowColors(True)
        self.tabWidget.addTab(self.acousticTab, "")

        # AIM Tab
        self.aimTab = QtWidgets.QWidget()
        self.aimTab.setObjectName(u"aimTab")
        self.aimView = QtWidgets.QTableView(self.aimTab)
        self.aimView.setObjectName(u"aimView")
        self.aimView.setGeometry(QtCore.QRect(0, 0, 844, 216))
        self.aimView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.aimView.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.aimView.setFont(font2)
        self.aimView.horizontalHeader().setFont(font3)
        self.aimView.setAlternatingRowColors(True)
        self.tabWidget.addTab(self.aimTab, "")

        # RFB Tab
        self.rfbTab = QtWidgets.QWidget()
        self.rfbTab.setObjectName(u"rfbTab")
        self.rfbView = QtWidgets.QTableView(self.rfbTab)
        self.rfbView.setObjectName(u"rfbView")
        self.rfbView.setGeometry(QtCore.QRect(0, 0, 844, 216))
        self.rfbView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.rfbView.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.rfbView.setFont(font2)
        self.rfbView.horizontalHeader().setFont(font3)
        self.rfbView.setAlternatingRowColors(True)
        self.tabWidget.addTab(self.rfbTab, "")

        # Thermal Tab
        self.thermalTab = QtWidgets.QWidget()
        self.thermalTab.setObjectName(u"thermalTab")
        self.thermalView = QtWidgets.QTableView(self.thermalTab)
        self.thermalView.setObjectName(u"thermalView")
        self.thermalView.setGeometry(QtCore.QRect(0, 0, 844, 216))
        self.thermalView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.thermalView.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.thermalView.setFont(font2)
        self.thermalView.horizontalHeader().setFont(font3)
        self.thermalView.setAlternatingRowColors(True)
        self.tabWidget.addTab(self.thermalTab, "")

        #Acoustic Resource Selection
        self.acousticResourceLabel = QtWidgets.QLabel(self.dataBox)
        self.acousticResourceLabel.setObjectName(u"acousticResourceLabel")
        self.acousticResourceLabel.setGeometry(QtCore.QRect(200, 20, 140, 21))
        self.acousticCombo = CheckableComboBox(self.dataBox)
        self.acousticCombo.setObjectName(u"acousticCombo")
        self.acousticCombo.setGeometry(QtCore.QRect(340, 20, 130, 25))
        self.acousticCombo.setFont(font2)

        # AIM Resource Selection
        self.aimResourceLabel = QtWidgets.QLabel(self.dataBox)
        self.aimResourceLabel.setObjectName(u"aimResourceLabel")
        self.aimResourceLabel.setGeometry(QtCore.QRect(200, 50, 100, 21))
        self.aimCombo = CheckableComboBox(self.dataBox)
        self.aimCombo.setObjectName(u"aimCombo")
        self.aimCombo.setGeometry(QtCore.QRect(340, 50, 130, 25))
        self.aimCombo.setFont(font2)

        # RFB Resource Selection
        self.rfbResourceLabel = QtWidgets.QLabel(self.dataBox)
        self.rfbResourceLabel.setObjectName(u"rfbResourceLabel")
        self.rfbResourceLabel.setGeometry(QtCore.QRect(200, 80, 100, 21))
        self.rfbCombo = CheckableComboBox(self.dataBox)
        self.rfbCombo.setObjectName(u"rfbCombo")
        self.rfbCombo.setGeometry(QtCore.QRect(340, 80, 130, 25))
        self.rfbCombo.setFont(font2)

        # Thermal Resource Selection
        self.thermalResourceLabel = QtWidgets.QLabel(self.dataBox)
        self.thermalResourceLabel.setObjectName(u"thermalResourceLabel")
        self.thermalResourceLabel.setGeometry(QtCore.QRect(200, 110, 140, 21))
        self.thermalCombo = CheckableComboBox(self.dataBox)
        self.thermalCombo.setObjectName(u"thermalCombo")
        self.thermalCombo.setGeometry(QtCore.QRect(340, 110, 130, 25))
        self.thermalCombo.setFont(font2)

        # Export Button
        self.exportButton = QtWidgets.QPushButton(self.centralwidget)
        self.exportButton.setObjectName(u"exportButton")
        self.exportButton.setGeometry(QtCore.QRect(670, 790, 200, 33))
        self.exportButton.setFont(font)
        self.exportButton.setEnabled(False)

        # MAIN WINDOW - Create Status Bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.reportlabel = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.reportlabel, stretch=0)

        ### RETRANSLATE UI ###
        self.retranslateUi(MainWindow)

        
        # Reset Button actions
        self.inputReset.clicked.connect(
            self.partNumberInput.clear)
        self.inputReset.clicked.connect(
            self.workOrderInput.clear)
        self.inputReset.clicked.connect(
            lambda: self.minDateInput.setDate(QtCore.QDate(2022, 1, 1)))
        self.inputReset.clicked.connect(lambda: self.maxDateInput.setDate(
            QtCore.QDate.currentDate()))
        self.inputReset.clicked.connect(lambda: self.aimCombo.reset())
        self.inputReset.clicked.connect(lambda: self.rfbCombo.reset())
        self.inputReset.clicked.connect(lambda: self.thermalCombo.reset())

        # Enable Export Button after first query run
        self.executeButton.clicked.connect(lambda: self.exportButton.setEnabled(True)) 
        
        self.tabWidget.setCurrentIndex(0)

        # Logic for disabling inputs based on selection
        self.variantBool.toggled['bool'].connect(
            self.minDateInput.setDisabled)
        self.variantBool.toggled['bool'].connect(
            self.maxDateInput.setDisabled)
        self.workOrderInput.textChanged.connect(
            lambda: self.minDateInput.setEnabled(True) if ((self.workOrderInput.document().isEmpty()) and (self.referenceBool.isChecked())) else self.minDateInput.setDisabled(True))
        self.workOrderInput.textChanged.connect(
            lambda: self.maxDateInput.setEnabled(True) if ((self.workOrderInput.document().isEmpty()) and (self.referenceBool.isChecked())) else self.maxDateInput.setDisabled(True))
        self.referenceBool.toggled['bool'].connect(
            lambda: self.minDateInput.setEnabled(True) if ((self.workOrderInput.document().isEmpty()) and (self.referenceBool.isChecked())) else self.minDateInput.setDisabled(True))
        self.referenceBool.toggled['bool'].connect(
            lambda: self.maxDateInput.setEnabled(True) if ((self.workOrderInput.document().isEmpty()) and (self.referenceBool.isChecked())) else self.maxDateInput.setDisabled(True))

        # Setting tab key order
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.variantBool, self.referenceBool)
        MainWindow.setTabOrder(self.referenceBool, self.acousticBool)
        MainWindow.setTabOrder(self.acousticBool, self.thermalBool)
        MainWindow.setTabOrder(self.thermalBool, self.rfbBool)
        MainWindow.setTabOrder(self.rfbBool, self.aimBool)
        MainWindow.setTabOrder(self.aimBool, self.workOrderInput)

    # Retranslate to add text to each part of GUI
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.testBox.setTitle(_translate("MainWindow", "Test Input"))
        self.acousticBool.setText(_translate("MainWindow", "Acoustic"))
        self.thermalBool.setText(_translate("MainWindow", "Thermal"))
        self.rfbBool.setText(_translate("MainWindow", "RFB"))
        self.aimBool.setText(_translate("MainWindow", "AIM"))
        self.queryBox.setTitle(_translate("MainWindow", "Query Selection"))
        self.variantBool.setText(_translate("MainWindow", "Variant Pop Query"))
        self.referenceBool.setText(_translate(
            "MainWindow", "Reference Pop Query"))
        self.dataBox.setTitle(_translate("MainWindow", "Input Data"))
        self.workOrderInput.setPlaceholderText(_translate(
            "MainWindow", "Single or Multiple Work Orders (comma separated)"))
        self.workOrderLabel.setText(
            _translate("MainWindow", "Work Order Input"))
        self.inputReset.setText(_translate("MainWindow", "Reset"))
        self.inputReset.setToolTip(_translate(
            "MainWindow", u"Click to Reset Part Number, Work Order, Resources, and Dates", None))
        self.partNumberLabel.setText(
            _translate("MainWindow", "Part Number Input"))
        self.partNumberInput.setPlaceholderText(
            _translate("MainWindow", "12-Digit PN"))
        self.minDateInput.setDisplayFormat(
            _translate("MainWindow", "yyyy/MM/dd"))
        self.minDateLabel.setText(_translate(
            "MainWindow", "Minimum Date Input"))
        self.maxDateLabel.setText(_translate(
            "MainWindow", "Maximum Date Input"))
        self.maxDateInput.setDisplayFormat(
            _translate("MainWindow", "yyyy/MM/dd"))
        self.executeButton.setText(_translate("MainWindow", "Run Query"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.aimTab), _translate("MainWindow", "AIM", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rfbTab), _translate("MainWindow", "RFB", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.thermalTab), _translate("MainWindow", "THERMAL", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.acousticTab), _translate("MainWindow", "ACOUSTIC", None))

        self.acousticResourceLabel.setText(_translate("MainWindow","ACOUSTIC Resource", None))
        self.aimResourceLabel.setText(_translate("MainWindow","AIM Resource", None))
        self.rfbResourceLabel.setText(_translate("MainWindow", "RFB Resource", None))
        self.thermalResourceLabel.setText(_translate("MainWindow", "THERMAL Resource", None))

        self.exportButton.setText(_translate("MainWindow", "Export Results", None))

        self.label.setText(_translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                      "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                      "p, li { white-space: pre-wrap; }\n"
                                      "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600; text-decoration: underline;\">Instructions:</span></p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">1) Variant - Work Order Only</span></p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Select Query Type &quot;Variant&quot;</p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px;"
                                      " -qt-block-indent:0; text-indent:0px;\">- Select Test(s) for Query</p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Enter 12-digit part number</p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Enter Work Order(s)</p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">2) Reference - Work Order Only</span></p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Select Query Type &quot;Reference&quot;</p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Select Test(s) for Query</p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; "
                                      "text-indent:0px;\">- Enter 12-digit part number</p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Enter Work Order(s)</p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">3) Reference - Part Number and Date Range</span></p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Select Query Type &quot;Reference&quot;</p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Select Test(s) for Query</p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Enter 12-digit part number</p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-ind"
                                      "ent:0px;\">- Select Minimum and Maximum Date</p>\n"
                                      "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">(longer ranges will cause longer query times)</p></body></html>", None))
