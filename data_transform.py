import pandas as pd
import json


class DataTransform():
    def __init__(self, data, inventory_mapping, partnumber, test):

        # Variable for DataFrame
        if type(data) == pd.core.frame.DataFrame:
            self.df = data
        elif (type(data) == str) and ('csv' in data):
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

        # Execution of Functions at instance creation
        self.filter_dataframe()
        self.transform_dataframe()

    def filter_dataframe(self):
        self.df_test = self.df.query(
            f'DC_OPERATION.str.contains("{self.test}")')
        return self.df_test

    def transform_dataframe(self):
        x = self.df_test.sort_values(by="DC_TEST_DATE_TIME_LOCAL").drop_duplicates(
            subset=["DC_SFC", "DC_MEASURE_NAME"], keep="last")

        info = self.mappings[self.PartNumber]['TESTS'][self.test]['INFO']
        test_list = self.mappings[self.PartNumber]['TESTS'][self.test]['DATA']

        base_l = x["DC_SFC"].drop_duplicates()
        for k, v in info.items():
            if k.startswith('DC_'):
                if k == "DC_SFC":
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

        base_r = x["DC_SFC"].drop_duplicates()
        for k, v in test_list.items():
            a = x[x['DC_MEASURE_NAME'] == k].loc[:, ['DC_SFC', 'DC_ACTUAL']]
            a.rename(columns={"DC_ACTUAL": v}, inplace=True)
            base_r = pd.merge(base_r, a, on="DC_SFC", how='outer')

        final_r = base_r

        df_test_final = pd.merge(final_l, final_r, on="DC_SFC")
        df_test_final.sort_values(by="DC_SFC", inplace=True)
        df_test_final.rename(columns={"DC_SFC": info["DC_SFC"]}, inplace=True)
        df_test_final = df_test_final[list(
            info.values()) + list(test_list.values())]

        self.df_test_final = df_test_final

        return self.df_test_final


if __name__ == '__main__':
    pass
