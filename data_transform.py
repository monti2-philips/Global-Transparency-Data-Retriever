import pandas as pd
import json


class DataTransform():
    def __init__(self, data, inventory_mapping, partnumber, test):

        
        if type(data) == pd.core.frame.DataFrame: # Verify that input is DataFrame
            self.df = data
        elif (type(data) == str) and ('csv' in data): # Verify that input is CSV (currently user has no way to import CSV) this is old and unused
            self.df = pd.read_csv(data)
        else:
            raise TypeError(
                'Input Type for "data" variable was not accepted. Only DataFrame or CSV.')

        # Variable for storing inventory_mapping dictionary
        with open(inventory_mapping) as f:
            self.mappings = json.load(f)

        # Variable for Part Number String
        self.PartNumber = partnumber[:11]

        # Variable for Test String
        self.test = test

        # Execution of methods at instance creation
        self.filter_dataframe()
        self.transform_dataframe()

    def filter_dataframe(self):
        """
        Generate Dataframe that is filtered by Test provided

        Returns:
            Filtered DataFrame
        """        
        self.df_test = self.df.query(
            f'DC_OPERATION.str.contains("{self.test}")')
        return self.df_test

    def transform_dataframe(self):
        """
        Method to perform transformations on DataFrame based on JSON mappings

        Returns:
            Final transformed DataFrame
        """
        # Drop duplicate values for DC_SFC-DC_MEASURE_NAME pairs and keep last
        x = self.df_test.sort_values(by="DC_TEST_DATE_TIME_LOCAL").drop_duplicates(
            subset=["DC_SFC", "DC_MEASURE_NAME"], keep="last")

        # Pull in "Database Headings : Excel Headings" pairs from JSON
        info = self.mappings[self.PartNumber]['TESTS'][self.test]['INFO']
        test_list = self.mappings[self.PartNumber]['TESTS'][self.test]['DATA']

        # Transformations for INFO Headers
        base_l = x["DC_SFC"].drop_duplicates()
        for k, v in info.items():
            if k.startswith('DC_'):
                if k == "DC_SFC": # Do not change DC_SFC at this step, final step
                    pass
                else:
                    a = x.loc[base_l.index, [k]]
                    a.rename(columns={k: v}, inplace=True)
                    base_l = pd.merge(
                        base_l, a, left_index=True, right_index=True)
        for k, v in info.items():
            if not k.startswith('DC_'):
                a = x[x['DC_MEASURE_NAME'] == k].loc[:, ['DC_SFC', 'DC_ACTUAL']]
                a.rename(columns={"DC_ACTUAL": v}, inplace=True)
                base_l = pd.merge(base_l, a, on="DC_SFC")

        final_l = base_l

        # Transformations for DATA Headers
        base_r = x["DC_SFC"].drop_duplicates()
        for k, v in test_list.items():
            a = x[x['DC_MEASURE_NAME'] == k].loc[:, ['DC_SFC', 'DC_ACTUAL']]
            a.rename(columns={"DC_ACTUAL": v}, inplace=True)
            base_r = pd.merge(base_r, a, on="DC_SFC", how='outer')

        final_r = base_r

        # Joing DataFrames on DC_SFC
        df_test_final = pd.merge(final_l, final_r, on="DC_SFC")
        df_test_final.sort_values(by="DC_SFC", inplace=True)

        # Change "DC_SFC" header to mapped value in info
        df_test_final.rename(columns={"DC_SFC": info["DC_SFC"]}, inplace=True)
        
        # Set Header orders for Final DataFrame
        df_test_final = df_test_final[list(
            info.values()) + list(test_list.values())]

        self.df_test_final = df_test_final

        return self.df_test_final


if __name__ == '__main__':
    pass
