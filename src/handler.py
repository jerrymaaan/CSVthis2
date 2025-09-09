import pandas as pd
import base64
import io


def stored_data_to_df(config, stored_data):
    # base 64 to dataframe
    content_type, content_string = stored_data.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('latin1')),
                     sep=config['csv_separator'],
                     decimal=config['csv_decimal']
                     )

    # changes time colum to datetime format and set as index
    col = config['time_col_name']
    df[col] = pd.to_datetime(df[col], format=config['time_col_format'])
    df = df.set_index(col)

    return df
