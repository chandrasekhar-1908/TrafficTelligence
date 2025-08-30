import pandas as pd
import joblib, os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

DATA_PATH = 'data/traffic_sample.csv'
MODEL_PATH = 'models/traffic_model.joblib'

def ensure_dataset():
    if not os.path.exists(DATA_PATH):
        import pandas as pd, numpy as np
        from datetime import datetime, timedelta
        rows = []
        start = datetime(2025,1,1)
        for h in range(48):
            t = start + timedelta(hours=h)
            rows.append({
                'datetime': t.isoformat(),
                'hour': t.hour,
                'day_of_week': t.weekday(),
                'month': t.month,
                'weather': np.random.choice(['Sunny','Rainy','Cloudy']),
                'temperature_c': np.random.uniform(15,35),
                'precip_mm': np.random.uniform(0,5),
                'is_holiday': np.random.choice([0,1]),
                'num_lanes': np.random.choice([2,3,4]),
                'speed_avg_kmh': np.random.uniform(20,80),
                'near_school_zone': np.random.choice([0,1]),
                'traffic_volume': np.random.randint(100,2000)
            })
        pd.DataFrame(rows).to_csv(DATA_PATH,index=False)

def train():
    ensure_dataset()
    df = pd.read_csv(DATA_PATH)
    y = df['traffic_volume']
    X = df.drop(columns=['traffic_volume','datetime'])

    cat = ['weather','is_holiday','near_school_zone','day_of_week','month','hour','num_lanes']
    num = ['temperature_c','precip_mm','speed_avg_kmh']

    pre = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat),
        ('num', StandardScaler(), num)
    ])

    pipe = Pipeline([('prep', pre), ('model', RandomForestRegressor(n_estimators=100, random_state=42))])
    Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=0.2,random_state=42)
    pipe.fit(Xtr,ytr)
    preds = pipe.predict(Xte)
    print('MAE:', mean_absolute_error(yte,preds))
    os.makedirs(os.path.dirname(MODEL_PATH),exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)
    print('Model saved at', MODEL_PATH)

if __name__=='__main__':
    train()
