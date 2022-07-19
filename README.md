# TSR_ML

* script names contained "combined" meant that the dataset was not split into GOOD group or POOR group

Based on whether mrs_tx_3 were included in the feature list
  - YES => TSR_ALL31 
  - NO  => TSR_ALL1 (Example in this file)

## data cleaning step (cleaning file)
TSR_ALL1 wnet through feature selection (TSR_ALL1_EXTRACTION.py), data preprocessing (TSR_ALL1_PREPROCESS.py), data imputation (TSR_ALL_IMPUTATION.R), and TSR_ALL1 were split into train, validation and test sets (TSR_ALL1_SPLIT.py). 
  - For TSR_ALL31 -> GOOD group's MICE is 4, while POOR group's MICE is 1
  - For TSR_ALL1 -> GOOD group's MICE is 1, while POOR group's MICE is 5

## data modelling step (model file)
Fed dataset into ET (extra trees), LR (logistic regression), XGBC (xgb classifier), Clinical (clinical scores)

## result step (result)
- For AUROC, utilisied TSR_ALL1_VALIDATION_AUC.py and TSR_ALL1_TEST_AUC.py
  * AUROC plot, utilised TSR_ALL_AUROC.ipynb
- For Feature Importance and SHAP, utilised TSR_ALL1_FI.ipynb
- For ROC curve, utillised TSR_ALL_ROC.py
- For evaluation performance, utilised TSR_ALL_SCORE.py
