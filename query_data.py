import pyodbc
import datetime
import pandas as pd
import json
import sys
from PyQt5 import QtWidgets

class QueryData():
    def __init__(self, input_checkboxes: dict, input_part_number: str, input_text_box: list, min_date: datetime.datetime |None, max_date: datetime.datetime|None, vipx_mapping: str, database_credentials: str, aim_resources=["ANY RESOURCE"], rfb_resources=["ANY RESOURCE"], thermal_resources=["ANY RESOURCE"]):

        # Creating Class attributes that can be shared between methods - created upon Class Instance creation
        self.input_checkboxes = input_checkboxes
        self.input_part_number = input_part_number
        self.input_text_box = input_text_box
        self.min_date = min_date
        self.max_date = max_date

        self.resources = {
                    "ACOUSTIC": ["ANY RESOURCE"],
                    "AIM": aim_resources,
                    "RFB": rfb_resources,
                    "THERMAL": thermal_resources
                    }
        # Convert all default values to "DC_RESOURCE" for later dataframe filtering
        self.resources = {key: 'DC_RESOURCE' if value == ["ANY RESOURCE"] else value for key, value in self.resources.items()}

        # Dictionary corresponding DC_ITEM to table name in VIPx (DFData) database
        with open(vipx_mapping) as f:
            self.VIPx_product_dict = json.load(f)

        # Dictionary with Database Credentials
        with open(database_credentials) as f:
            self.database_credentials = json.load(f)

        # Empty DataFrame with set columns
        self.data = pd.DataFrame(columns=['DC_ITEM', 'DC_SFC', 'DC_TEST_DATE_TIME_LOCAL', 'DC_RESOURCE',
                        'DC_OPERATION', 'DC_MEASURE_NAME', 'DC_DESCRIPTION', 'DC_ACTUAL'], data=[])

    def MES_connection(self):

        server = self.database_credentials["MES"]["server"]
        database = self.database_credentials["MES"]["database"]
        username = self.database_credentials["MES"]["username"]
        password = self.database_credentials["MES"]["password"]

        return self.database_connection(server, database, username, password)

    def VIPx_connection(self):

        server = self.database_credentials["DFData"]["server"]
        database = self.database_credentials["DFData"]["database"]
        username = self.database_credentials["DFData"]["username"]
        password = self.database_credentials["DFData"]["password"]

        return self.database_connection(server, database, username, password)

    def database_connection(self, server, database, username, password):
        """
        Create database connection with 30 second timeout parameter. If connection takes >30 secs than user is prompted to verify VPN if off-site and then exits.
        """        
        timeout = 30
        try:
            cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password, timeout=timeout)
            return cnxn
        except pyodbc.OperationalError:
            print("Error: Could not connect to MES database within {} seconds".format(timeout))
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText(f'Connection to MES Database failed. Please check VPN connection if off-site.')
            msgBox.setWindowTitle('Database Connection Error')
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Close)
            msgBox.exec()
            sys.exit()

    def get_by_workorder(self):
        test_checkboxes = self.input_checkboxes.copy()

        if not any(test_checkboxes):
            return ['no tests selected']
        if "AIM" not in test_checkboxes or "THERMAL" not in test_checkboxes or "ACOUSTIC" not in test_checkboxes or "RFB" not in test_checkboxes:
            return ['invalid test_checkboxes object']

        MES_cnxn = self.MES_connection()
        print('MES Connection Success')
        work_orders = self.input_text_box

        # Get and check part number from MES
        check_part_query = rf"""
                        SELECT DC_ITEM, MIN(DC_TEST_DATE_TIME_LOCAL) as min_date, MAX(DC_TEST_DATE_TIME_LOCAL) as max_date FROM ( 
                            SELECT DC_ITEM, DC_TEST_DATE_TIME_LOCAL FROM rep_ods.dbo.VW_PH_ADHOC_62_PARAMETRIC 
                            WHERE 
                                (DC_SHOP_ORDER = '{"' OR DC_SHOP_ORDER = '".join(work_orders)}')
                        ) a GROUP BY DC_ITEM
                    """
        check_part_data = pd.read_sql_query(check_part_query, MES_cnxn)
        item_num = check_part_data['DC_ITEM'].tolist()
        if len(item_num) > 1:
            return None
        elif len(item_num) == 0:
            return 1
        else:
            item_num = item_num[0]
            if item_num != self.input_part_number:
                return None
            else:
                print('-- Part Number confirmed')
                min_date = check_part_data['min_date'][0] - datetime.timedelta(days=1)
                max_date = check_part_data['max_date'][0] + datetime.timedelta(days=1)

                if test_checkboxes["ACOUSTIC"] and item_num in self.VIPx_product_dict:
                    sfc_query = rf"""
                                SELECT DC_SFC FROM ( 
                                    SELECT DC_SFC FROM rep_ods.dbo.VW_PH_ADHOC_62_PARAMETRIC 
                                    WHERE 
                                        DC_SHOP_ORDER = '{"' OR DC_SHOP_ORDER = '".join(work_orders)}' AND
                                        DC_TEST_DATE_TIME_LOCAL > '{min_date.strftime('%Y-%m-%d')}' AND
                                        DC_TEST_DATE_TIME_LOCAL < '{max_date.strftime('%Y-%m-%d')}'
                                ) a GROUP BY DC_SFC
                                """
                    sfc_list = pd.read_sql_query(sfc_query, MES_cnxn)[
                        'DC_SFC'].tolist()
                    sfc_list = [sfc[sfc.index('-')+1:] for sfc in sfc_list]
                    print('-- SFC\'s collected for DFData Acoustic Database')

                    VIPx_data = self.VIPx_query_create(item_num, sfc_list, min_date, max_date)
                    print('-- DFData Acoustic Data collected')

                    test_checkboxes["ACOUSTIC"] = False

                test_checkboxes_list = [
                    key for key in test_checkboxes if test_checkboxes[key]]
                MES_query = rf"""
                            SELECT DC_ITEM, DC_SFC, DC_TEST_DATE_TIME_LOCAL, DC_RESOURCE, DC_OPERATION, DC_MEASURE_NAME, DC_DESCRIPTION, DC_ACTUAL
                            FROM rep_ods.dbo.VW_PH_ADHOC_62_PARAMETRIC
                            WHERE 
                                (DC_SHOP_ORDER = '{"' OR DC_SHOP_ORDER = '".join(work_orders)}') AND
                                DC_TEST_DATE_TIME_LOCAL > '{min_date.strftime('%Y-%m-%d')}' AND
                                DC_TEST_DATE_TIME_LOCAL < '{max_date.strftime('%Y-%m-%d')}' AND
                                (DC_OPERATION LIKE '%{"%' OR DC_OPERATION LIKE '%".join(test_checkboxes_list)}%')
                                """
                MES_data = pd.read_sql_query(MES_query, MES_cnxn)
                print('MES Test Data collected')
                self.data = pd.concat([self.data, MES_data])

                # Resource Filtering
                resource_query = f"(DC_OPERATION.str.contains('ACOUSTIC') & DC_RESOURCE.isin({self.resources['ACOUSTIC']})) | \
                                (DC_OPERATION.str.contains('AIM') & DC_RESOURCE.isin({self.resources['AIM']})) | \
                                (DC_OPERATION.str.contains('RFB') & DC_RESOURCE.isin({self.resources['RFB']})) | \
                                (DC_OPERATION.str.contains('THERMAL') & DC_RESOURCE.isin({self.resources['THERMAL']}))"
                self.data = self.data.query(resource_query)

                return self.data

    def get_by_dates(self):
        test_checkboxes = self.input_checkboxes.copy()

        if not any(test_checkboxes):
            return ['no tests selected']
        if "AIM" not in test_checkboxes or "THERMAL" not in test_checkboxes or "ACOUSTIC" not in test_checkboxes or "RFB" not in test_checkboxes:
            return ['invalid test_checkboxes object']

        MES_cnxn = self.MES_connection()
        print('MES Connection Success')

        # MES query to gather work order values
        workorder_query = rf"""SELECT SHOP_ORDER, MIN(ACTUAL_START_DATE) as min_date, MAX(ACTUAL_COMP_DATE) as max_date FROM (
                            SELECT SHOP_ORDER, ACTUAL_START_DATE, ACTUAL_COMP_DATE FROM rep_ods.dbo.ODS_SHOP_ORDER
                            WHERE SITE = 'US9P' AND
                                ITEM = '{self.input_part_number}' AND
                                ((RELEASED_DATE > '{self.min_date.strftime('%Y-%m-%d')}' AND RELEASED_DATE < '{self.max_date.strftime('%Y-%m-%d')}') OR
                                (ACTUAL_START_DATE > '{self.min_date.strftime('%Y-%m-%d')}' AND ACTUAL_COMP_DATE < '{self.max_date.strftime('%Y-%m-%d')}')) AND
                                LEFT(ROUTER, 2) <> 'SR' AND
                                ERP_PUTAWAY_STORLOC = 'RE01'
                        ) base GROUP BY SHOP_ORDER"""

        workorder_data = pd.read_sql_query(workorder_query, MES_cnxn)
        work_orders = workorder_data['SHOP_ORDER'].tolist()
        print('-- Work Order\'s collected')
        if len(work_orders) == 0:
            return 1
        else:
            min_date = workorder_data['min_date'].min() - datetime.timedelta(days=1)
            max_date = workorder_data['max_date'].max() + datetime.timedelta(days=1)
            work_orders = workorder_data['SHOP_ORDER'].tolist()

            if test_checkboxes["ACOUSTIC"] and self.input_part_number in self.VIPx_product_dict:
                sfc_query = rf"""
                            SELECT DC_SFC FROM ( 
                                SELECT DC_SFC FROM rep_ods.dbo.VW_PH_ADHOC_62_PARAMETRIC 
                                WHERE 
                                    DC_SHOP_ORDER = '{"' OR DC_SHOP_ORDER = '".join(work_orders)}' AND
                                    DC_TEST_DATE_TIME_LOCAL > '{min_date.strftime('%Y-%m-%d')}' AND
                                    DC_TEST_DATE_TIME_LOCAL < '{max_date.strftime('%Y-%m-%d')}'
                            ) a GROUP BY DC_SFC
                            """
                sfc_list = pd.read_sql_query(sfc_query, MES_cnxn)[
                    'DC_SFC'].tolist()
                sfc_list = [sfc[sfc.index('-')+1:] for sfc in sfc_list]
                print('-- SFC\'s collected for DFData Acoustic Database')

                VIPx_data = self.VIPx_query_create(self.input_part_number, sfc_list, min_date, max_date)
                print('-- DFData Acoustic Data collected')

                test_checkboxes["ACOUSTIC"] = False

            test_checkboxes_list = [
                key for key in test_checkboxes if test_checkboxes[key]]
            MES_query = rf"""
                        SELECT DC_ITEM, DC_SFC, DC_TEST_DATE_TIME_LOCAL, DC_RESOURCE, DC_OPERATION, DC_MEASURE_NAME, DC_DESCRIPTION, DC_ACTUAL
                        FROM rep_ods.dbo.VW_PH_ADHOC_62_PARAMETRIC
                        WHERE 
                            (DC_SHOP_ORDER = '{"' OR DC_SHOP_ORDER = '".join(work_orders)}') AND
                            DC_TEST_DATE_TIME_LOCAL > '{min_date.strftime('%Y-%m-%d')}' AND
                            DC_TEST_DATE_TIME_LOCAL < '{max_date.strftime('%Y-%m-%d')}' AND
                            (DC_OPERATION LIKE '%{"%' OR DC_OPERATION LIKE '%".join(test_checkboxes_list)}%')
                        """
            MES_data = pd.read_sql_query(MES_query, MES_cnxn)
            print('MES Test Data collected')
            self.data = pd.concat([self.data, MES_data])

            # Resource Filtering
            resource_query = f"(DC_OPERATION.str.contains('ACOUSTIC') & DC_RESOURCE.isin({self.resources['ACOUSTIC']})) | \
                            (DC_OPERATION.str.contains('AIM') & DC_RESOURCE.isin({self.resources['AIM']})) | \
                            (DC_OPERATION.str.contains('RFB') & DC_RESOURCE.isin({self.resources['RFB']})) | \
                            (DC_OPERATION.str.contains('THERMAL') & DC_RESOURCE.isin({self.resources['THERMAL']}))"
            self.data = self.data.query(resource_query)

            return self.data

    def VIPx_query_create(self, item_num, sfc_list, min_date, max_date):
        # Input for item_num is self.input_part_number
        VIPx_cnxn = self.VIPx_connection()
        print('VIPx Connection Success')
        table_name = self.VIPx_product_dict[item_num]
        
        if table_name == 'XL_14_3':
            value_alias = '(ParameterValueMin + ParameterValueMax)/2'
            # ValueMean is no longer valid column - replaced with average of Min and Max
            # Remove 'TestName' as column doesnt exist, use 'Parameter' as DC_DESCRIPTION
            VIPx_query_select = rf"SELECT '{item_num}' as DC_ITEM, '{item_num}-' + ProductSN as DC_SFC, time as DC_TEST_DATE_TIME_LOCAL, TestStation as DC_RESOURCE, 'VIPX_ACOUSTIC_TEST' as DC_OPERATION, Parameter as  DC_MEASURE_NAME, Parameter as DC_DESCRIPTION, {value_alias} as DC_ACTUAL"
        
        elif table_name == 'xcube':
            value_alias = 'ParameterMean'
            # Remove 'TestName' as column doesnt exist, use 'Parameter' as DC_DESCRIPTION
            VIPx_query_select = rf"SELECT '{item_num}' as DC_ITEM, '{item_num}-' + ProductSN as DC_SFC, time as DC_TEST_DATE_TIME_LOCAL, TestStation as DC_RESOURCE, 'VIPX_ACOUSTIC_TEST' as DC_OPERATION, Parameter as  DC_MEASURE_NAME, Parameter as DC_DESCRIPTION, {value_alias} as DC_ACTUAL"
        
        else:
            value_alias = 'ParameterValue'
            VIPx_query_select = rf"SELECT '{item_num}' as DC_ITEM, '{item_num}-' + ProductSN as DC_SFC, time as DC_TEST_DATE_TIME_LOCAL, TestStation as DC_RESOURCE, 'VIPX_ACOUSTIC_TEST' as DC_OPERATION, TestName + ' - ' + Parameter as  DC_MEASURE_NAME, TestName as DC_DESCRIPTION, {value_alias} as DC_ACTUAL"

        VIPx_query = VIPx_query_select + rf"""
                    FROM DFData.dbo.{table_name}
                    WHERE
                        ProductSN IN ('{"', '".join(sfc_list)}') AND
                        Parameter NOT LIKE '%\[%' ESCAPE '\' AND
                        sTime > '{min_date.strftime('%Y-%m-%d')}' AND
                        sTime < '{max_date.strftime('%Y-%m-%d')}' AND
                        ProcessStep LIKE '%FINAL%'
                    """
        
        VIPx_data = pd.read_sql_query(VIPx_query, VIPx_cnxn)
        self.data = pd.concat([self.data, VIPx_data])
        VIPx_cnxn.close()

        return VIPx_data

if __name__ == '__main__':
    
    input_checkboxes= {
                        "ACOUSTIC": True,
                        "AIM": True,
                        "RFB": True,
                        "THERMAL": True
                    }
    input_part_number= '453561780787'
    input_text_box= ['302232423']
    min_date= None
    max_date= None
    vipx_mapping = r'data\vipX_product.json'
    database_credentials = r'data\database_credentials.json'

    test = QueryData(input_checkboxes, input_part_number, input_text_box, min_date, max_date, vipx_mapping, database_credentials).get_by_workorder()
    print(test.shape)
