import pandas as pd
import numpy as np
import glob
import os
from tqdm import tqdm
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--output', type=str, default='database/data/final.csv', help='path to processed csv file')
    parser.add_argument('-d', '--data', type=str, default='COVID-19-master', help='path to cloned data repo')

    return parser.parse_args()

def sanitise_column_names(df):
    '''
    Some files do not follow the standardised column naming conventions (e.g. csse_covid_19_daily_reports/01-22-2020.csv)
    Check for these erroneous formats and convert the column names back to the standard
    '''
    standard_cols = {
        'Province/State': 'Province_State',
        'Country/Region': 'Country_Region',
        'Last Update': 'Last_Update'
    }
    for k, v in standard_cols.items():
        if k in df.columns:
            df = df.rename(columns={k: v})
    return df

def convert_float(row, column):
    '''
    some float calculated values have errors which returns values like '#DIV/0'.
    test for these erroneous values by trying to typecase to float.
    '''
    try:
        return float(row[column])
    except ValueError:
        return np.nan

def main():
    args = parse_arguments()
    
    daily_reports_world_files = glob.glob(os.path.join(args.data, 'csse_covid_19_data', 'csse_covid_19_daily_reports', '*.csv'))
    
    # print(daily_reports_world_files[0], len(daily_reports_world_files))
    # return
    combined_columns = ['Province_State', 'Country_Region', 'Date', 'Last_Update', 'Lat', 'Long_', 
                        'Confirmed', 'Deaths', 'Recovered', 'Active', 'Incident_Rate', 'Case_Fatality_Ratio']
    output_df = pd.DataFrame(columns=combined_columns)

    # print(output_df)
    for csv_fpath in tqdm(daily_reports_world_files):
        report_date = os.path.split(csv_fpath)[-1][:-4]
        # print(report_date)
        df = pd.read_csv(csv_fpath)
        df.insert(0, "Date", [report_date]*len(df.index))
        # print(df)
        df = sanitise_column_names(df)
        # print(df)
        for col in combined_columns:
            if col not in df.columns:
                df.insert(0, col, [np.nan]*len(df.index))
        for index, row in df.iterrows():
            df['Incident_Rate'] = convert_float(row, 'Incident_Rate')
            df['Case_Fatality_Ratio'] = convert_float(row, 'Case_Fatality_Ratio')
        df = df[combined_columns]
        output_df = pd.concat([output_df, df])
        
    # print(output_df.shape)

    output_df = output_df.astype({
        'Confirmed': 'Int64',
        'Deaths': 'Int64',
        'Recovered': 'Int64',
        'Active': 'Int64'
    })
    output_df.to_csv('database/data/final.csv', index=False)
    print("Data processed and saved to database/data/final.csv")

if __name__ == '__main__':
    main()