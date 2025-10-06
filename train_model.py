
#!/usr/bin/env python3
import os, pandas as pd, joblib, numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

def main(indices_dir='outputs/indices', out_dir='outputs/model'):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(os.path.join(indices_dir,'landsat_ndvi_summary.csv'))
    # synthetic target: combine ndvi and random noise as placeholder for 'health'
    df['health_score'] = 50 + 30*df['ndvi_mean']
    features = ['ndvi_mean']
    X = df[features].fillna(0)
    y = df['health_score']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train,y_train)
    preds = model.predict(X_test)
    print('R2:', r2_score(y_test,preds))
    print('RMSE:', mean_squared_error(y_test,preds,squared=False))
    joblib.dump({'model': model, 'features': features}, os.path.join(out_dir,'uvi_model.joblib'))

if __name__=='__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--indices_dir', default='outputs/indices')
    p.add_argument('--out_dir', default='outputs/model')
    args = p.parse_args()
    main(args.indices_dir, args.out_dir)
