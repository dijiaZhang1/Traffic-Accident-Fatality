import joblib
import pandas as pd
pipeline = joblib.load('svm_fullpipe_zhang.pkl')
X_test = pd.read_csv('x_test_data.csv')
X_test.drop(X_test.columns[X_test.columns.str.contains(
    'unnamed', case=False)], axis=1, inplace=True)

# predict using the best model
y_test_pred = pipeline.predict(X_test)
print(y_test_pred)
