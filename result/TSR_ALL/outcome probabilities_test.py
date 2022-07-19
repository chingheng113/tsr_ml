import pandas as pd
import os
import joblib

# 1 month
## GOOD
csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL1", "TSR_ALL1G_X_TEST_withID.csv")
G_X_test_id = pd.read_csv(csv_path)
G_X_test = G_X_test_id.drop(["idcase_id"], axis = 1)

csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL1", "TSR_ALL1G_y_TEST_withID.csv")
G_y_test = pd.read_csv(csv_path)

### XGBClassifier
pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE1", "TSR_ALL1G_XGBC_CALIBRATED.pkl")
G_XGBC_CALIBRATED = joblib.load(pkl_path)
y_test_xgbc_G_pred = G_XGBC_CALIBRATED.predict_proba(G_X_test)[:, 1]

### Logistic Regression
pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE3", "TSR_ALL1G_LR_CALIBRATED.pkl")
G_LR_CALIBRATED = joblib.load(pkl_path)
y_test_lr_G_pred = G_LR_CALIBRATED.predict_proba(G_X_test)[:, 1]

one_month_G_probabilities_test = pd.concat([G_X_test_id["idcase_id"], G_y_test, pd.DataFrame(y_test_xgbc_G_pred), pd.DataFrame(y_test_lr_G_pred)], axis = 1)
one_month_G_probabilities_test.columns = ["idcase_id", "group truth", "xgbc probabilities", "lr probabilities"]
one_month_G_probabilities_test.to_csv("outcome probabilities/one_month_G_probabilities_test.csv", index = False)

# POOR
csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL1", "TSR_ALL1B_X_TEST_withID.csv")
P_X_test_id = pd.read_csv(csv_path)
P_X_test = P_X_test_id.drop(["idcase_id"], axis = 1)

csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL1", "TSR_ALL1B_y_TEST_withID.csv")
P_y_test = pd.read_csv(csv_path)

### XGBClassifier
pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL1B_XGBC_CALIBRATED.pkl")
P_XGBC_CALIBRATED = joblib.load(pkl_path)
y_test_xgbc_P_pred = P_XGBC_CALIBRATED.predict_proba(P_X_test)[:, 1]

### Logistic Regression
pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL1B_LR_CALIBRATED.pkl")
P_LR_CALIBRATED = joblib.load(pkl_path)
y_test_lr_P_pred = P_LR_CALIBRATED.predict_proba(P_X_test)[:, 1]

one_month_P_probabilities_test = pd.concat([P_X_test_id["idcase_id"], P_y_test, pd.DataFrame(y_test_xgbc_P_pred), pd.DataFrame(y_test_lr_P_pred)], axis = 1)
one_month_P_probabilities_test.columns = ["idcase_id", "group truth", "xgbc probabilities", "lr probabilities"]
one_month_P_probabilities_test.to_csv("outcome probabilities/one_month_P_probabilities_test.csv", index = False)

# 3+1 month
## GOOD
csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL31", "TSR_ALL31G_X_TEST_withID.csv")
G_X_test_id = pd.read_csv(csv_path)
G_X_test = G_X_test_id.drop(["idcase_id"], axis = 1)

csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL31", "TSR_ALL31G_y_TEST_withID.csv")
G_y_test = pd.read_csv(csv_path)

### XGBClassifier
pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE2", "TSR_ALL31G_XGBC_CALIBRATED.pkl")
G_XGBC_CALIBRATED = joblib.load(pkl_path)
y_test_xgbc_G_pred = G_XGBC_CALIBRATED.predict_proba(G_X_test)[:, 1]

### Logistic Regression
pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE3", "TSR_ALL31G_LR_CALIBRATED.pkl")
G_LR_CALIBRATED = joblib.load(pkl_path)
y_test_lr_G_pred = G_LR_CALIBRATED.predict_proba(G_X_test)[:, 1]

three_month_G_probabilities_test = pd.concat([G_X_test_id["idcase_id"], G_y_test, pd.DataFrame(y_test_xgbc_G_pred), pd.DataFrame(y_test_lr_G_pred)], axis = 1)
three_month_G_probabilities_test.columns = ["idcase_id", "group truth", "xgbc probabilities", "lr probabilities"]
three_month_G_probabilities_test.to_csv("outcome probabilities/three_month_G_probabilities_test.csv", index = False)

# POOR
csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL31", "TSR_ALL31B_X_TEST_withID.csv")
P_X_test_id = pd.read_csv(csv_path)
P_X_test = P_X_test_id.drop(["idcase_id"], axis = 1)

csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL31", "TSR_ALL31B_y_TEST_withID.csv")
P_y_test = pd.read_csv(csv_path)

### XGBClassifier
pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE3", "TSR_ALL31B_XGBC_CALIBRATED.pkl")
P_XGBC_CALIBRATED = joblib.load(pkl_path)
y_test_xgbc_P_pred = P_XGBC_CALIBRATED.predict_proba(P_X_test)[:, 1]

### Logistic Regression
pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE3", "TSR_ALL31B_LR_CALIBRATED.pkl")
P_LR_CALIBRATED = joblib.load(pkl_path)
y_test_lr_P_pred = P_LR_CALIBRATED.predict_proba(P_X_test)[:, 1]

three_month_P_probabilities_test = pd.concat([P_X_test_id["idcase_id"], P_y_test, pd.DataFrame(y_test_xgbc_P_pred), pd.DataFrame(y_test_lr_P_pred)], axis = 1)
three_month_P_probabilities_test.columns = ["idcase_id", "group truth", "xgbc probabilities", "lr probabilities"]
three_month_P_probabilities_test.to_csv("outcome probabilities/three_month_P_probabilities_test.csv", index = False)