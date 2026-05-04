from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.compose import ColumnTransformer

import pandas as pd
import numpy as np

def preprocess(path):
    data = pd.read_csv(path)

    data = data[['sensor_periodo','datetime','PM2_5_ugm3','PM10_ugm3','O3_ppm','NO2_ppm','SO2_ppm','CO_ppm']]
    data = data[data['sensor_periodo'].str.contains('D')]

    contaminant_cols = ['PM2_5_ugm3', 'PM10_ugm3', 'O3_ppm', 'NO2_ppm', 'SO2_ppm', 'CO_ppm']

    data = data.drop(columns=['sensor_periodo'])
    data = data.set_index("datetime")
    data = data.resample("1min").mean()

    data = data.interpolate(method="linear", limit=5)
    data = data.dropna()

    for col in contaminant_cols:
        rolling_mean = data[col].rolling(30).mean()
        rolling_std  = data[col].rolling(30).std()
        z_scores     = (data[col] - rolling_mean) / rolling_std
        data.loc[z_scores.abs() > 4, col] = np.nan

    data = data.interpolate(method="linear", limit=5)
    data = data.dropna()

    data.to_csv('../Data/datos_limpios.csv')

    log_transform = FunctionTransformer(np.log1p, inverse_func=np.expm1)

    preprocessor = ColumnTransformer(transformers=[
        ('log_scale', Pipeline([
            ('log',   log_transform),
            ('scale', StandardScaler())
        ]), contaminant_cols)
    ], remainder='passthrough')

    preprocessor.fit(data)
