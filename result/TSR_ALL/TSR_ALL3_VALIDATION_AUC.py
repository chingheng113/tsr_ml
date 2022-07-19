import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import os
import numpy as np
import joblib
from sklearn.metrics import auc, roc_curve
from sklearn.ensemble import ExtraTreesClassifier
from xgboost import XGBClassifier
from sklearn.calibration import CalibratedClassifierCV
import matplotlib.pyplot as plt

def algorithms(X_train, X_validation, y_train, y_validation, based, tuned, calibrated, model_selected):
    # BASED
    y_validation_pred = based.predict_proba(X_validation)
    fpr, tpr, thresholds = roc_curve(y_validation, y_validation_pred[:, 1])
    validation_auroc = auc(fpr, tpr)
    print('AUC of validation set:', round(validation_auroc, 3))

    # TUNED
    print('--> Tuned Parameters Best Score: ', tuned.best_score_)
    print('--> Best Parameters: \n', tuned.best_params_)

    y_validation_pred = tuned.predict_proba(X_validation)
    fpr, tpr, thresholds = roc_curve(y_validation, y_validation_pred[:, 1])
    validation_auroc_tuned = auc(fpr, tpr)
    print('AUC of validation set:', round(validation_auroc_tuned, 3))

    # CALIBRATED
    y_validation_pred = calibrated.predict_proba(X_validation)
    fpr, tpr, thresholds = roc_curve(y_validation, y_validation_pred[:, 1])
    validation_auroc_cc = auc(fpr, tpr)
    print('AUC of validation set:', round(validation_auroc_cc, 3))

    #### Selected Columns
    model_fi = calibrated.base_estimator._final_estimator.feature_importances_
    model_fi_df = pd.DataFrame(model_fi)
    model_fi_df.index = X_validation.columns
    model_fi_df.columns = (["Value"])
    model_fi_df = model_fi_df.reset_index(drop=False)
    model_fi_df.columns = (["Feature", "Value"])
    model_fi_df = model_fi_df.sort_values(["Value"], ascending=False)

    ### sigma threshold
    model_fi_df_noZERO = model_fi_df[~model_fi_df.Value.isin([0])]
    model_fi_df_noZERO_mean = model_fi_df_noZERO.Value.mean()
    model_fi_df_noZERO_std = model_fi_df_noZERO.Value.std()
    sigma_n = len(model_fi_df_noZERO[model_fi_df_noZERO.Value > model_fi_df_noZERO_mean + model_fi_df_noZERO_std])
    print(sigma_n)

    validation_auroc_list = []
    validation_auroc_tuned_list = []
    validation_auroc_cc_list = []

    for i in sigma_n, 10, 20, 30:
        model_fi_index = model_fi_df[0:i].index

        X_train_selected = X_train.iloc[:, model_fi_index]
        X_validation_selected = X_validation.iloc[:, model_fi_index]

        # base et_selected
        BASED_selected = model_selected.fit(X_train_selected, y_train)

        y_validation_pred = BASED_selected.predict_proba(X_validation_selected)
        fpr, tpr, thresholds = roc_curve(y_validation, y_validation_pred[:, 1])
        validation_auroc_selected = auc(fpr, tpr)
        validation_auroc_list.append(validation_auroc_selected)
        print('AUC of validation set:', round(validation_auroc_selected, 3))

        # tune et_selected
        rscv_selected = tuned.best_estimator_
        TUNED_selected = rscv_selected.fit(X_train_selected, y_train)

        y_validation_pred = TUNED_selected.predict_proba(X_validation_selected)
        fpr, tpr, thresholds = roc_curve(y_validation, y_validation_pred[:, 1])
        validation_auroc_selected_tuned = auc(fpr, tpr)
        validation_auroc_tuned_list.append(validation_auroc_selected_tuned)
        print('AUC of validation set:', round(validation_auroc_selected_tuned, 3))

        # calibrate et_selected
        cccv_selected = CalibratedClassifierCV(base_estimator=TUNED_selected, cv=5)
        CALIBRATED_selected = cccv_selected.fit(X_train_selected, y_train)

        y_validation_pred = CALIBRATED_selected.predict_proba(X_validation_selected)
        fpr, tpr, thresholds = roc_curve(y_validation, y_validation_pred[:, 1])
        validation_auroc_selected_cc = auc(fpr, tpr)
        validation_auroc_cc_list.append(validation_auroc_selected_cc)
        print('AUC of validation set:', round(validation_auroc_selected_cc, 3))

    validation_auroc_list.append(validation_auroc)
    validation_auroc_tuned_list.append(validation_auroc_tuned)
    validation_auroc_cc_list.append(validation_auroc_cc)

    return validation_auroc_list, validation_auroc_tuned_list, validation_auroc_cc_list, CALIBRATED_selected

if __name__ == '__main__':
    # Import datasets
    csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL3", "TSR_ALL3G_X_TRAIN.csv")
    G_X_train = pd.read_csv(csv_path)

    csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL3", "TSR_ALL3G_y_TRAIN.csv")
    G_y_train = pd.read_csv(csv_path)
    G_y_train = np.ravel(G_y_train)

    csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL3", "TSR_ALL3G_X_VALIDATION.csv")
    G_X_validation = pd.read_csv(csv_path)

    csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL3", "TSR_ALL3G_y_VALIDATION.csv")
    G_y_validation = pd.read_csv(csv_path)
    G_y_validation = np.ravel(G_y_validation)

    csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL3", "TSR_ALL3B_X_TRAIN.csv")
    B_X_train = pd.read_csv(csv_path)

    csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL3", "TSR_ALL3B_y_TRAIN.csv")
    B_y_train = pd.read_csv(csv_path)
    B_y_train = np.ravel(B_y_train)

    csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL3", "TSR_ALL3B_X_VALIDATION.csv")
    B_X_validation = pd.read_csv(csv_path)

    csv_path = os.path.join("..", "..", "data", "LINKED_DATA", "TSR_ALL", "TSR_ALL3", "TSR_ALL3B_y_VALIDATION.csv")
    B_y_validation = pd.read_csv(csv_path)
    B_y_validation = np.ravel(B_y_validation)

    ## Based models
    et_selected = ExtraTreesClassifier(random_state=19)
    xgbc_selected = XGBClassifier(booster="gbtree", random_state=19, use_label_encoder=False, eval_metric="auc",
                                  tree_method="hist", n_jobs=-1)

    # GOOD when Discharge
    ### Extra trees
    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3G_ET_BASED.pkl")
    G_ET_BASED = joblib.load(pkl_path)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3G_ET_TUNED.pkl")
    G_ET_TUNED = joblib.load(pkl_path)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3G_ET_CALIBRATED.pkl")
    G_ET_CALIBRATED = joblib.load(pkl_path)

    G_validation_auroc_list, G_validation_auroc_tuned_list, G_validation_auroc_cc_list, G_ET_CALIBRATED_selected = algorithms(G_X_train,
                                                                                                                              G_X_validation,
                                                                                                                              G_y_train,
                                                                                                                              G_y_validation,
                                                                                                                              G_ET_BASED,
                                                                                                                              G_ET_TUNED,
                                                                                                                              G_ET_CALIBRATED,
                                                                                                                              et_selected)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3G_ET_CALIBRATED_selected.pkl")
    joblib.dump(G_ET_CALIBRATED_selected, pkl_path)

    x = "sigma", "10", "20", "30", "310"
    plt.plot(x, G_validation_auroc_list, label="based")
    plt.plot(x, G_validation_auroc_tuned_list, label="tuned")
    plt.plot(x, G_validation_auroc_cc_list, label="calibrated")
    plt.legend()
    for i in range(len(x)):
        plt.annotate(round(G_validation_auroc_list[i], 3), (x[i], G_validation_auroc_list[i]))
        plt.annotate(round(G_validation_auroc_tuned_list[i], 3), (x[i], G_validation_auroc_tuned_list[i]))
        plt.annotate(round(G_validation_auroc_cc_list[i], 3), (x[i], G_validation_auroc_cc_list[i]))
    plt.title('TSR_ALL3_ET_G', fontsize=15)
    # plt.savefig('PLOT/TSR_ALL3/TSR_ALL3_ET_G.png')
    plt.show()

    ### XGBClassifier
    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3G_XGBC_BASED.pkl")
    G_XGBC_BASED = joblib.load(pkl_path)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3G_XGBC_TUNED.pkl")
    G_XGBC_TUNED = joblib.load(pkl_path)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3G_XGBC_CALIBRATED.pkl")
    G_XGBC_CALIBRATED = joblib.load(pkl_path)

    G_validation_auroc_list, G_validation_auroc_tuned_list, G_validation_auroc_cc_list, G_XGBC_CALIBRATED_selected = algorithms(G_X_train,
                                                                                                                                G_X_validation,
                                                                                                                                G_y_train,
                                                                                                                                G_y_validation,
                                                                                                                                G_XGBC_BASED,
                                                                                                                                G_XGBC_TUNED,
                                                                                                                                G_XGBC_CALIBRATED,
                                                                                                                                xgbc_selected)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3G_XGBC_CALIBRATED_selected.pkl")
    joblib.dump(G_XGBC_CALIBRATED_selected, pkl_path)

    x = "sigma", "10", "20", "30", "310"
    plt.plot(x, G_validation_auroc_list, label="based")
    plt.plot(x, G_validation_auroc_tuned_list, label="tuned")
    plt.plot(x, G_validation_auroc_cc_list, label="calibrated")
    plt.legend()
    for i in range(len(x)):
        plt.annotate(round(G_validation_auroc_list[i], 3), (x[i], G_validation_auroc_list[i]))
        plt.annotate(round(G_validation_auroc_tuned_list[i], 3), (x[i], G_validation_auroc_tuned_list[i]))
        plt.annotate(round(G_validation_auroc_cc_list[i], 3), (x[i], G_validation_auroc_cc_list[i]))
    plt.title('TSR_ALL3_XGBC_G', fontsize=15)
    # plt.savefig('PLOT/TSR_ALL3/TSR_ALL3_XGBC_G.png')
    plt.show()

    ### Logistic Regression
    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3G_LR_BASED.pkl")
    G_LR_BASED = joblib.load(pkl_path)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3G_LR_TUNED.pkl")
    G_LR_TUNED = joblib.load(pkl_path)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3G_LR_CALIBRATED.pkl")
    G_LR_CALIBRATED = joblib.load(pkl_path)

    # BASED
    y_validation_pred = G_LR_BASED.predict_proba(G_X_validation)
    fpr, tpr, thresholds = roc_curve(G_y_validation, y_validation_pred[:, 1])
    validation_auroc = auc(fpr, tpr)
    print('AUC of validation set:', round(validation_auroc, 3))

    # TUNED
    print('--> Tuned Parameters Best Score: ', G_LR_TUNED.best_score_)
    print('--> Best Parameters: \n', G_LR_TUNED.best_params_)
    y_validation_pred = G_LR_TUNED.predict_proba(G_X_validation)
    fpr, tpr, thresholds = roc_curve(G_y_validation, y_validation_pred[:, 1])
    validation_auroc_tuned = auc(fpr, tpr)
    print('AUC of validation set:', round(validation_auroc_tuned, 3))

    # CALIBRATED
    y_validation_pred = G_LR_CALIBRATED.predict_proba(G_X_validation)
    fpr, tpr, thresholds = roc_curve(G_y_validation, y_validation_pred[:, 1])
    validation_auroc_cc = auc(fpr, tpr)
    print('AUC of validation set:', round(validation_auroc_cc, 3))

    # BAD when Discharge
    ### Extra trees
    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3B_ET_BASED.pkl")
    B_ET_BASED = joblib.load(pkl_path)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3B_ET_TUNED.pkl")
    B_ET_TUNED = joblib.load(pkl_path)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3B_ET_CALIBRATED.pkl")
    B_ET_CALIBRATED = joblib.load(pkl_path)

    B_validation_auroc_list, B_validation_auroc_tuned_list, B_validation_auroc_cc_list, B_ET_CALIBRATED_selected = algorithms(B_X_train,
                                                                                                                              B_X_validation,
                                                                                                                              B_y_train,
                                                                                                                              B_y_validation,
                                                                                                                              B_ET_BASED,
                                                                                                                              B_ET_TUNED,
                                                                                                                              B_ET_CALIBRATED,
                                                                                                                              et_selected)
    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3B_ET_CALIBRATED_selected.pkl")
    joblib.dump(B_ET_CALIBRATED_selected, pkl_path)

    x = "sigma", "10", "20", "30", "310"
    plt.plot(x, B_validation_auroc_list, label="based")
    plt.plot(x, B_validation_auroc_tuned_list, label="tuned")
    plt.plot(x, B_validation_auroc_cc_list, label="calibrated")
    plt.legend()
    for i in range(len(x)):
        plt.annotate(round(B_validation_auroc_list[i], 3), (x[i], B_validation_auroc_list[i]))
        plt.annotate(round(B_validation_auroc_tuned_list[i], 3), (x[i], B_validation_auroc_tuned_list[i]))
        plt.annotate(round(B_validation_auroc_cc_list[i], 3), (x[i], B_validation_auroc_cc_list[i]))
    plt.title('TSR_ALL3_ET_B', fontsize=15)
    # plt.savefig('PLOT/TSR_ALL3/TSR_ALL3_ET_B.png')
    plt.show()

    ### XGBClassifier
    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3B_XGBC_BASED.pkl")
    B_XGBC_BASED = joblib.load(pkl_path)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3B_XGBC_TUNED.pkl")
    B_XGBC_TUNED = joblib.load(pkl_path)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3B_XGBC_CALIBRATED.pkl")
    B_XGBC_CALIBRATED = joblib.load(pkl_path)

    B_validation_auroc_list, B_validation_auroc_tuned_list, B_validation_auroc_cc_list, B_XGBC_CALIBRATED_selected = algorithms(B_X_train,
                                                                                                                                B_X_validation,
                                                                                                                                B_y_train,
                                                                                                                                B_y_validation,
                                                                                                                                B_XGBC_BASED,
                                                                                                                                B_XGBC_TUNED,
                                                                                                                                B_XGBC_CALIBRATED,
                                                                                                                                xgbc_selected)
    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3B_XGBC_CALIBRATED_selected.pkl")
    joblib.dump(B_XGBC_CALIBRATED_selected, pkl_path)

    x = "sigma", "10", "20", "30", "310"
    plt.plot(x, B_validation_auroc_list, label="based")
    plt.plot(x, B_validation_auroc_tuned_list, label="tuned")
    plt.plot(x, B_validation_auroc_cc_list, label="calibrated")
    plt.legend()
    for i in range(len(x)):
        plt.annotate(round(B_validation_auroc_list[i], 3), (x[i], B_validation_auroc_list[i]))
        plt.annotate(round(B_validation_auroc_tuned_list[i], 3), (x[i], B_validation_auroc_tuned_list[i]))
        plt.annotate(round(B_validation_auroc_cc_list[i], 3), (x[i], B_validation_auroc_cc_list[i]))
    plt.title('TSR_ALL3_XGBC_B', fontsize=15)
    # plt.savefig('PLOT/TSR_ALL3/TSR_ALL3_XGBC_B.png')
    plt.show()

    ### Logistic Regression
    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3B_LR_BASED.pkl")
    B_LR_BASED = joblib.load(pkl_path)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3B_LR_TUNED.pkl")
    B_LR_TUNED = joblib.load(pkl_path)

    pkl_path = os.path.join("..", "..", "model", "model_pickle", "MICE5", "TSR_ALL3B_LR_CALIBRATED.pkl")
    B_LR_CALIBRATED = joblib.load(pkl_path)

    # BASED
    y_validation_pred = B_LR_BASED.predict_proba(B_X_validation)
    fpr, tpr, thresholds = roc_curve(B_y_validation, y_validation_pred[:, 1])
    validation_auroc = auc(fpr, tpr)
    print('AUC of validation set:', round(validation_auroc, 3))

    # TUNED
    print('--> Tuned Parameters Best Score: ', B_LR_TUNED.best_score_)
    print('--> Best Parameters: \n', B_LR_TUNED.best_params_)
    y_validation_pred = B_LR_TUNED.predict_proba(B_X_validation)
    fpr, tpr, thresholds = roc_curve(B_y_validation, y_validation_pred[:, 1])
    validation_auroc_tuned = auc(fpr, tpr)
    print('AUC of validation set:', round(validation_auroc_tuned, 3))

    # CALIBRATED
    y_validation_pred = B_LR_CALIBRATED.predict_proba(B_X_validation)
    fpr, tpr, thresholds = roc_curve(B_y_validation, y_validation_pred[:, 1])
    validation_auroc_cc = auc(fpr, tpr)
    print('AUC of validation set:', round(validation_auroc_cc, 3))