from matplotlib.pyplot import axis
import pandas as pd

SHEET_NAMES=['NATIONAL', 'ABIA', 'ABUJA', 'ANAMBRA', 'EBONYI', 'ENUGU', 'IMO',
 'AKWA IBOM', 'BAYELSA', 'CROSS RIVER', 'DELTA', 'RIVERS', 'EDO',
  'ADAMAWA', 'BAUCHI', 'BORNO', 'GOMBE', 'BENUE', 'TARABA', 'YOBE',
   'KOGI', 'KWARA', 'NASSARAWA', 'NIGER', 'PLATEAU', 'EKITI', 'LAGOS',
    'ONDO', 'OGUN_', 'OSUN', 'OYO', 'JIGAWA_', 'KADUNA_', 'KANO_', 'KATSINA', 
    'KEBBI_', 'ZAMFARA_', 'SOKOTO']

def ingest_data(data_path: str, sheet_names: list = None) -> dict:
    for sheet_name in sheet_names:
        if sheet_name in sheet_names:
            data = pd.read_excel(data_path, sheet_names)
        return data


def get_sheet_data(data: dict, sheet_name: str):
    # Extract data from each sheet name.

    return data[sheet_name]


def clean(df):
    # Create a copy of the dataframe to prevent the original being overwitten.
    temp = df.copy()

    # Merge the ItemLabels and Unit of Measurement columns and assign a new variable name to the merged column.
    temp["Item and Size"] = temp["ItemLabels"] + temp["Unit of Measurement"]

    # Drop the individual columns
    temp.drop(['ItemLabels', 'Unit of Measurement'],
              axis='columns', inplace=True)
    
    temp.drop(list(temp.filter(regex='Unnamed')), inplace= True, axis=1)


    # Set index as the new column and transpose the output data.
    transposed_temp = temp.set_index("Item and Size").T
    return transposed_temp
