import numpy as np
import pandas as pd
from datetime import datetime as dt


def format_api_dataset(api_calls):
    data = {
        'created_on': []
    }
    for call in api_calls:
        data['created_on'].append(dt.fromisoformat(call['created_on']))

    df = pd.DataFrame(data)
    df = df.groupby(df['created_on'].dt.date).size().reset_index(name='y')
    df.columns = ['x', 'y']
    return df.to_dict('records')


def format_client_dataset(images):
    data = {
        'created_on': []
    }
    for image in images:
        data['created_on'].append(dt.fromisoformat(image['created_on']))

    df = pd.DataFrame(data)
    df = df.groupby(df['created_on'].dt.date).size().reset_index(name='y')
    df.columns = ['x', 'y']
    return df.to_dict('records')
