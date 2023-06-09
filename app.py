import warnings
import os
import data_transform
import query_data
import table_model
import pandas as pd
import xlsxwriter
import json
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from front_end import Ui_MainWindow

# Status Update - Python Startup
print('Python Initializing...')

# Status Update - Imports Complete
print('Imports Complete')

# Setting Base Directory for file references
basedir = os.path.dirname(__file__)

# Try-Except to set logo for taskbar
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = u'Philips.GlobalTransparency.DataRetriever'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

# Main Window Class
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Set window title
        self.setWindowTitle("Global Transparency Data Retriever")

        # Set window icon
        app_icon = QtGui.QIcon(os.path.join(basedir, "./static/logo.ico"))
        app.setWindowIcon(app_icon)

        pts = r'\\usdrdsech1vwa15\Reedsville\PTS\GlobalTransparencyDataRetrieverSourceCode'
        # Check for File Existence and Import Configuration Files
        self.inventory_mapping = self.get_config(os.path.join(pts, 'inventory.json'))
        self.resource_mapping = self.get_config(os.path.join(pts, 'operation-resource.json'))
        self.vipx_mapping = self.get_config(os.path.join(pts, 'vipX_product.json'))
        self.database_credentials = self.get_config(os.path.join(pts, 'database_credentials.json'))
        
        # Set resources to comboboxes for AIM, RFB, and Thermal test stations
        with open(self.resource_mapping) as f:
            self.resources = json.load(f)
        self.aimCombo.addItems(self.resources["AIM"])
        self.rfbCombo.addItems(self.resources["RFB"])
        self.thermalCombo.addItems(self.resources["THERMAL"])
        # Set resource of Acoustic only when the combo box is enabled; reference front_end.py - this box is only enabled when 12-digit part number is entered
        self.partNumberInput.textChanged.connect(
            lambda: self.fill_acousticCombo() if self.acousticCombo.isEnabled() else None)

        # Initiate run count
        self.runCount = 0

        # Set "Run Query" button to run_query method
        self.executeButton.clicked.connect(lambda: self.run_query())
        # Set "Export" button to save_dataframes method
        self.exportButton.clicked.connect(lambda: self.save_dataframes())

    def get_config(self, json_file):
        """
        Method that takes in file path and verifies if the file exists. A Warning message box is raised if file is not found.

        Args:
            json_file (filepath): file path to configuration file

        Raises:
            FileNotFoundError: if file is not found a message box will appear and upon close the application will quit

        Returns:
            json_file (filepath): file path that was passed as input
        """        
        if os.path.exists(json_file) == False:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(
                f'File "{json_file}" does not exist in source directory.\nIf the issue continues, please contact Engineering for support.')
            msgBox.setWindowTitle('Configuration File Not Found')
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Close)
            msgBox.exec()
            raise FileNotFoundError
        else:
            return json_file

    def get_parameters(self):
        """
        Collect parameters from the GUI interface [Query Type, Tests, Part Number, Work Orders, Dates]
        """        
        if self.variantBool.isChecked():
            self.query_type = 'Variant'
        elif self.referenceBool.isChecked():
            self.query_type = 'Reference'

        self.test_checkboxes = {
            "ACOUSTIC": self.acousticBool.isChecked(),
            "AIM": self.aimBool.isChecked(),
            "RFB": self.rfbBool.isChecked(),
            "THERMAL": self.thermalBool.isChecked()
        }

        self.part_number = self.partNumberInput.text()

        if self.workOrderInput.toPlainText() != "":
            self.work_orders = [
                order.strip() for order in self.workOrderInput.toPlainText().split(',')]
        else:
            self.work_orders = None

        if (self.minDateInput.isEnabled() == True) and (self.maxDateInput.isEnabled() == True):
            self.min_date = self.minDateInput.date().toPyDate()
            self.max_date = self.maxDateInput.date().toPyDate()
        else:
            self.min_date = None
            self.max_date = None
        return

    def check_parameters(self):      
        self.check_tests()
        self.check_partnumber()
        self.check_workorders()
        return

    def check_tests(self):
        """
        Verify that at least one test is selected. Raises message box if no tests selected.
        """        
        if all(value == False for value in self.test_checkboxes.values()):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText('Please select a minimum of 1 test type')
            msgBox.setWindowTitle('Test Selection Error')
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Retry)
            msgBox.exec()
        else:
            self.param_check['tests'] = True
        return

    def check_partnumber(self):
        """
        Verify that part number is 12 Digits, Numeric, and Base11 exist in inventory.json
        """        
        if len(self.part_number) != 12:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText('Please enter a 12 digit Part Number')
            msgBox.setWindowTitle('Part Number Error')
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Retry)
            msgBox.exec()
        elif self.part_number.isnumeric() == False:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText('Please enter only numerics for Part Number')
            msgBox.setWindowTitle('Part Number Error')
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Retry)
            msgBox.exec()
        else:
            with open(self.inventory_mapping) as f:
                self.mappings = json.load(f)
            if self.part_number[:11] not in self.mappings.keys():
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText('Part Number not found in JSON')
                msgBox.setWindowTitle('Part Number Error')
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Retry)
                msgBox.exec()
            else:
                self.param_check['partnumber'] = True
                self.is_vipX_product()
        return

    def is_vipX_product(self):
        """
        Checks if part number will be querying Acoustic DB for results and notifies user that query will take longer than normal.
        """        
        # Dictionary corresponding DC_ITEM to table name in VIPx (DFData) database
        with open(self.vipx_mapping) as f:
            self.VIPx_product_dict = json.load(f)
        
        if self.test_checkboxes["ACOUSTIC"] and self.part_number in self.VIPx_product_dict:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setText('You have selected a product with acoustic data in the DFData Database.\nThis query will take slightly longer than normal.')
            msgBox.setWindowTitle('DFData Database Product')
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()
        else:
            pass
        return

    def fill_acousticCombo(self):
        # Dictionary corresponding DC_ITEM to table name in VIPx (DFData) database
        with open(self.vipx_mapping) as f:
            self.VIPx_product_dict = json.load(f)
        # Collect parameters to get part number
        self.get_parameters()
        # Clear current combobox list
        self.acousticCombo.clear()

        # Check if part number is VIPx product and set options based on part number
        if self.part_number in self.VIPx_product_dict:
            self.acousticCombo.addItems(self.resources["ACOUSTIC"][self.part_number])
        else:
            self.acousticCombo.addItems(self.resources["ACOUSTIC"]["MES"])

    def check_workorders(self):
        if self.query_type == 'Variant':
            if self.work_orders == None:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText('Please enter one or more work orders')
                msgBox.setWindowTitle('Work Order Error')
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Retry)
                msgBox.exec()
            elif self.work_orders != None:
                if all([_.isnumeric() for _ in self.work_orders]) != True:
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                    msgBox.setText(
                        'Please ensure all Work Orders are only numerics')
                    msgBox.setWindowTitle('Work Order Error')
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Retry)
                    msgBox.exec()
                else:
                    self.param_check['workorders'] = True
        elif self.query_type == 'Reference':
            if self.work_orders == None and ((self.min_date == None) and (self.max_date == None)):
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText('Please enter one or more work orders')
                msgBox.setWindowTitle('Work Order Error')
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Retry)
                msgBox.exec()
            elif self.work_orders == None and ((self.min_date != None) and (self.max_date != None)):
                if self.check_dates() == True:
                    self.param_check['workorders'] = True
                elif self.check_dates() == False:
                    self.minDateInput.setDate(
                        QtCore.QDate.currentDate().addDays(-1))
                    self.maxDateInput.setDate(QtCore.QDate.currentDate())
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                    msgBox.setText(
                        'Please ensure minimum date is before maximum date.\nValues being reset to yesterday and today.')
                    msgBox.setWindowTitle('Date Entry Error')
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Retry)
                    msgBox.exec()
            elif self.work_orders != None and ((self.min_date == None) and (self.max_date == None)):
                self.param_check['workorders'] = True
        else:
            raise ValueError('Data Input Logic Broken')
        return

    def check_dates(self):
        if self.min_date < self.max_date:
            return True
        else:
            return False

    def get_resources(self):
        self.acoustic_resource = self.acousticCombo.resourceList
        self.aim_resource = self.aimCombo.resourceList
        self.rfb_resource = self.rfbCombo.resourceList
        self.thermal_resource = self.thermalCombo.resourceList
        print(f'ACOUSTIC Resource: {self.acoustic_resource}\nAIM Resource: {self.aim_resource}\nRFB Resource: {self.rfb_resource}\nTHERMAL Resource: {self.thermal_resource}')
        return 

    def clear_dataViews(self):
        self.aimView.setModel(None)
        self.rfbView.setModel(None)
        self.thermalView.setModel(None)
        self.acousticView.setModel(None)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.acousticTab), f"Acoustic")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.aimTab), f"AIM")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rfbTab), f"RFB")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.thermalTab), f"THERMAL")

        print('Views cleared')


    def filter_dataframes(self):
        if self.test_checkboxes['AIM']:
            self.aim = data_transform.DataTransform(
                self.data, self.inventory_mapping, self.part_number, 'AIM').df_test_final
            self.aimView.setModel(table_model.pandasModel(self.aim))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.aimTab), f"AIM ({self.aim.shape[0]})")
            print(f'Shape of AIM: {self.aim.shape}')

        if self.test_checkboxes['RFB']:
            self.rfb = data_transform.DataTransform(
                self.data, self.inventory_mapping, self.part_number, 'RFB').df_test_final
            self.rfbView.setModel(table_model.pandasModel(self.rfb))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.rfbTab), f"RFB ({self.rfb.shape[0]})")
            print(f'Shape of RFB: {self.rfb.shape}')

        if self.test_checkboxes['THERMAL']:
            self.thermal = data_transform.DataTransform(
                self.data, self.inventory_mapping, self.part_number, 'THERMAL').df_test_final
            self.thermalView.setModel(table_model.pandasModel(self.thermal))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.thermalTab), f"THERMAL ({self.thermal.shape[0]})")
            print(f'Shape of THERMAL: {self.thermal.shape}')

        if self.test_checkboxes['ACOUSTIC']:
            self.acoustic = data_transform.DataTransform(
                self.data, self.inventory_mapping, self.part_number, 'ACOUSTIC').df_test_final
            self.acousticView.setModel(table_model.pandasModel(self.acoustic))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.acousticTab), f"Acoustic ({self.acoustic.shape[0]})")
            print(f'Shape of ACOUSTIC: {self.acoustic.shape}')
        
        return

    def create_filename(self):
        parent = os.path.expanduser('~')
        child = 'Downloads'
        path = os.path.join(parent, child)
        if os.path.isdir(path):  # Does the directory exist
            f_name = '__'.join([self.query_type,
                                self.part_number,
                                datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
                                '.xlsx'])
            self.output_path = os.path.join(path, f_name)
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(
                f'Folder "{path}" could not be located for downloads.\nIf the issue continues, please contact Engineering for support.')
            msgBox.setWindowTitle('Downloads Folder Not Found')
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Close)
            msgBox.exec()
            raise FileNotFoundError
        return

    def completed_run(self):
        self.reportlabel.setText(f'Current Run Complete')
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.NoIcon)
        msgBox.setText('<p align="center">Please see row counts for each test on respective tab.<br>If you would like to export these results click "Export Results"</p>')
        msgBox.setWindowTitle('Current Run Complete')
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        msgBox.exec()
        print('')
        return

    def create_parameter_dataframe(self):
        def list_parse(_):
            if _ == None:
                return _
            else:
                return ", ".join(_)

        parameter_dict = {
            "Query Type" : [self.query_type],
            "Acoustic Test" : [self.test_checkboxes["ACOUSTIC"]],
            "AIM Test" : [self.test_checkboxes["AIM"]],
            "RFB Test" : [self.test_checkboxes["RFB"]],
            "Thermal Test" : [self.test_checkboxes["THERMAL"]],
            "Part Number" : [self.part_number],
            "Work Orders" : [list_parse(self.work_orders)],
            "Min Date" : [self.min_date],
            "Max Date" : [self.max_date],
            "Acoustic Resources" : [list_parse(self.acoustic_resource)],
            "AIM Resources" : [list_parse(self.aim_resource)],
            "RFB Resources" : [list_parse(self.rfb_resource)],
            "Thermal Resources" : [list_parse(self.thermal_resource)]
            }

        self.parameter_dataframe = pd.DataFrame(parameter_dict).T
        return

    def save_dataframes(self):
        self.create_parameter_dataframe()
        with pd.ExcelWriter(self.output_path, engine="xlsxwriter", engine_kwargs={"options": {"strings_to_numbers": True}}) as writer:
            self.parameter_dataframe.to_excel(writer, sheet_name='Inputs', header=False)
            workbook = writer.book
            worksheet = writer.sheets['Inputs']
            cell_format = workbook.add_format({'align': 'center', 'valign': 'center', 'text_wrap': True, 'num_format': '0'})
            worksheet.set_column("A:B", 20, cell_format)

            if self.test_checkboxes['ACOUSTIC']:
                self.acoustic.to_excel(writer, sheet_name='Acoustic', index=False)
            if self.test_checkboxes['AIM']:
                self.aim.to_excel(writer, sheet_name='AIM', index=False)
            if self.test_checkboxes['RFB']:
                self.rfb.to_excel(writer, sheet_name='RFB', index=False)                
            if self.test_checkboxes['THERMAL']:
                self.thermal.to_excel(writer, sheet_name='Thermal', index=False)

        self.show_file_location()

        return

    def show_file_location(self):
        self.reportlabel.setText(f'Results saved at {self.output_path}')
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.NoIcon)
        msgBox.setText(f'Results saved at:\n{self.output_path}')
        msgBox.setWindowTitle('Query Complete')
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        msgBox.exec()

        return

    def run_query(self):
        self.runCount += 1
        print(f'Run Count: {self.runCount}')
        self.get_parameters()
        self.param_check = {'tests': False,
                            'partnumber': False, 'workorders': False}
        self.check_parameters()
        self.get_resources()
        self.clear_dataViews()
        if any(value == False for value in self.param_check.values()):
            print(f'Parameter Check did not pass: {self.param_check}')
        elif all(value == True for value in self.param_check.values()):
            if self.query_type == 'Variant':
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    self.data = query_data.QueryData(
                        self.test_checkboxes, self.part_number, self.work_orders, self.min_date, self.max_date, self.vipx_mapping, self.database_credentials, self.acoustic_resource, self.aim_resource, self.rfb_resource, self.thermal_resource).get_by_workorder()

                if isinstance(self.data, pd.DataFrame):
                    self.filter_dataframes()
                    self.create_filename()
                    self.completed_run()
                elif self.data is None:
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                    msgBox.setText(
                        f'Part Numbers between Work Orders do not match')
                    msgBox.setWindowTitle('Multiple Part Number Error')
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Close)
                    msgBox.exec()
                elif self.data == 1:
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                    msgBox.setText(
                        f'Work Order does not exist')
                    msgBox.setWindowTitle('Work Order Error')
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Close)
                    msgBox.exec()
                else:
                    print('Issues with data return')

            elif self.query_type == 'Reference':
                if (self.work_orders != None) and ((self.min_date == None) and (self.max_date == None)):
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", UserWarning)
                        self.data = query_data.QueryData(
                            self.test_checkboxes, self.part_number, self.work_orders, self.min_date, self.max_date, self.vipx_mapping, self.database_credentials, self.acoustic_resource, self.aim_resource, self.rfb_resource, self.thermal_resource).get_by_workorder()

                    if isinstance(self.data, pd.DataFrame):
                        self.filter_dataframes()
                        self.create_filename()
                        self.completed_run()
                    elif self.data is None:
                        msgBox = QtWidgets.QMessageBox()
                        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                        msgBox.setText(
                            f'Part Numbers between Work Orders do not match')
                        msgBox.setWindowTitle('Multiple Part Number Error')
                        msgBox.setStandardButtons(QtWidgets.QMessageBox.Close)
                        msgBox.exec()
                    elif self.data == 1:
                        msgBox = QtWidgets.QMessageBox()
                        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                        msgBox.setText(
                            f'Work Order does not exist')
                        msgBox.setWindowTitle('Work Order Error')
                        msgBox.setStandardButtons(QtWidgets.QMessageBox.Close)
                        msgBox.exec()
                    else:
                        print('Issues with data return')

                elif (self.work_orders == None) and ((self.min_date != None) and (self.max_date != None)):
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", UserWarning)
                        self.data = query_data.QueryData(
                            self.test_checkboxes, self.part_number, self.work_orders, self.min_date, self.max_date, self.vipx_mapping, self.database_credentials, self.acoustic_resource, self.aim_resource, self.rfb_resource, self.thermal_resource).get_by_dates()

                    if isinstance(self.data, pd.DataFrame):
                        self.filter_dataframes()
                        self.create_filename()
                        self.completed_run()
                    elif self.data == 1:
                        msgBox = QtWidgets.QMessageBox()
                        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                        msgBox.setText(
                            f'No Data Found for this time period')
                        msgBox.setWindowTitle('No Data Error')
                        msgBox.setStandardButtons(QtWidgets.QMessageBox.Close)
                        msgBox.exec()
                    else:
                        print('Issues with data return')

                else:
                    print('reference query loophole')
            else:
                print('loophole')

        return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    print('Window Initialized\n')
    window.show()
    app.exec()
