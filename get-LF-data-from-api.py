import requests
import pandas as pd
import io

def get_lf_data(heat_id):
    """
    Fetches LF data from the API for a given heat ID and returns it as a pandas DataFrame.
    
    Args:
        heat_id (str): The heat ID to fetch data for.
        
    Returns:
        pd.DataFrame: DataFrame containing the fetched data.
    """
    url = "http://10.192.47.100:61000/api/com-return/by-heatid"
    params = {'heatID': heat_id}
    
    # Define column names based on the data structure provided
    # The API returns CSV data without a header row.
    columns = [
        'id',           # 0
        'cr_time',      # 1
        'SOTHUNG',      # 2
        'heatID',       # 3
        'MACTHEP',      # 4
        'CONGDOAN',     # 5
        'NHIETDO',      # 6
        'Sample_ID',    # 7
        'C_tp',         # 8
        'Si_tp',        # 9
        'Mn_tp',        # 10
        'P_tp',         # 11
        'S_tp',         # 12
        'Cr_tp',        # 13
        'Mo_tp',        # 14
        'Ni_tp',        # 15
        'Al_tp',        # 16
        'Co_tp',        # 17
        'Cu_tp',        # 18
        'Nb_tp',        # 19
        'Ti_tp',        # 20
        'V_tp',         # 21
        'W_tp',         # 22
        'Pb_tp',        # 23
        'Sb_tp',        # 24
        'B_tp',         # 25
        'N_tp',         # 26
        'Fe_tp',        # 27
        'CEV_tp',       # 28
        'Altot_tp',     # 29
        'Alins_tp',     # 30
        'Alsol_tp'      # 31
    ]
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Read CSV data from the response content
        # Check if response is empty
        if not response.text.strip():
            print(f"No data returned for heat ID: {heat_id}")
            return pd.DataFrame(columns=columns)

        df = pd.read_csv(io.StringIO(response.text), header=None, names=columns)
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV data: {e}")
        return None

if __name__ == "__main__":
    # Test with the example heat ID provided
    test_heat_id = "B2600511"
    print(f"Fetching data for heat ID: {test_heat_id}...")
    df = get_lf_data(test_heat_id)
    
    if df is not None and not df.empty:
        print("Data fetched successfully!")
        print(f"Shape: {df.shape}")
        print("\nFirst 5 rows:")
        print(df.head())
        print("\nColumns:")
        print(df.columns.tolist())
    else:
        print("Failed to fetch data or data is empty.")