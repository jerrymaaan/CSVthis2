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

    # changes time colum to datetime format if it has one and set as index
    x_col = config['time_col_name']
    if config['time_col_format'] is not None:
        df[x_col] = pd.to_datetime(df[x_col], format=config['time_col_format'])
    df = df.set_index(x_col)

    return df
