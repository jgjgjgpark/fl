import copy
import traceback

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psycopg2
import statsmodels.api as sm
from keras.metrics import MeanAbsoluteError

from statsmodels.formula.api import glm

"""
DB_USER = os.environ.get('MEDICAL_RECORDS_USER')
DB_PASSWORD = os.environ.get('MEDICAL_RECORDS_PW')
DB_URL = os.environ.get('MEDICAL_RECORDS_URL')
DB_DATABASE = os.environ.get('MEDICAL_RECORDS_DATABASE')
DB_SCHEMA = os.environ.get('MEDICAL_RECORDS_SCHEMA')
DB_HOST, DB_PORT = DB_URL.split(":")
"""

DB_USER = "readonlyuser"
DB_PASSWORD = "x741TuPDpO1y"
DB_URL = "203.245.2.199:5432"
DB_DATABASE = "omop"
DB_SCHEMA = "cdm_synpuf"
DB_HOST, DB_PORT = DB_URL.split(":")

pd.set_option("display.max_columns", None)


# %%
def connection_db():
    try:
        print("Connected")
        db = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_DATABASE,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT)

        return db

    except psycopg2.Error as e:
        print("Not connected")
        print("e: ", e)
        print("e.pgcode: ", e.pgcode)
        print("e.pgerror: ", e.pgerror)
        print("traceback: ", traceback.format_exc())


db_connection = connection_db()
cursor = db_connection.cursor()
cdmDatabaseSchema = DB_SCHEMA

# %%
# load data
# df_autoimmune = pd.read_csv("DM/autoimmune.csv", encoding="cp949")
df_autoimmune = pd.read_csv("script/DM/autoimmune.csv", encoding="cp949")
print("df_autoimmune size : ", df_autoimmune.size)

# df_drugs_1 = pd.read_csv("DM/dexamethasone_systemic_drug.csv")
df_drugs_1 = pd.read_csv("script/DM/dexamethasone_systemic_drug.csv")
# df_drugs_2 = pd.read_csv("DM/prednisolone_systemic_drug.csv")
df_drugs_2 = pd.read_csv("script/DM/prednisolone_systemic_drug.csv")
df_drugs = pd.concat([df_drugs_1["Id"], df_drugs_2["Id"]], ignore_index=True)
print("df_drugs size : ", df_drugs.size)

# df_type_1 = pd.read_csv("DM/steroidstudy - osteonecrosisDTdrug.csv")
df_type_1 = pd.read_csv("script/DM/steroidstudy - osteonecrosisDTdrug.csv")
# df_type_2 = pd.read_csv("DM/steroidstudy - boneFracture.csv")
df_type_2 = pd.read_csv("script/DM/steroidstudy - boneFracture.csv")
# df_type_3 = pd.read_csv("DM/steroidstudy - osteoporosis.csv")
df_type_3 = pd.read_csv("script/DM/steroidstudy - osteoporosis.csv")
df_type = pd.concat([df_type_1["Id"], df_type_2["Id"], df_type_3["Id"]])
print("df_type size : ", df_type.size)

# %%
column_list = ["DRUG_EXPOSURE_ID", "PERSON_ID", "DRUG_CONCEPT_ID", "DRUG_EXPOSURE_START_DATE",
               "DRUG_EXPOSURE_START_DATETIME",
               "DRUG_EXPOSURE_END_DATE", "DRUG_EXPOSURE_END_DATETIME", "VERBATIM_END_DATE", "DRUG_TYPE_CONCEPT_ID",
               "STOP_REASON",
               "REFILLS", "QUANTITY", "DAYS_SUPPLY", "SIG", "ROUTE_CONCEPT_ID",
               "LOT_NUMBER", "PROVIDER_ID", "VISIT_OCCURRENCE_ID", "DRUG_SOURCE_VALUE", "DRUG_SOURCE_CONCEPT_ID",
               "ROUTE_SOURCE_VALUE", "DOSE_UNIT_SOURCE_VALUE"]
sql = """
SELECT *
FROM {}.drug_exposure
where person_id IN 
    ( SELECT person_id
    FROM {}.condition_occurrence
    where condition_concept_id IN {})
AND drug_concept_id IN {}
""".format(cdmDatabaseSchema, cdmDatabaseSchema, tuple(df_autoimmune["Id"].values.tolist()),
           tuple(df_drugs.values.tolist()))
cursor.execute(sql)
result1 = cursor.fetchall()
# print("========== result1")
result1 = pd.DataFrame(result1, columns=column_list)
# print(result1.head())

# %%
sql = """
SELECT condition_concept_id, person_id, condition_start_date
FROM {}.condition_occurrence
WHERE person_id IN (
    SELECT person_id
    FROM {}.drug_exposure
    WHERE person_id IN ( 
        SELECT person_id
        FROM {}.condition_occurrence
        where condition_concept_id IN {})
AND drug_concept_id IN {})
AND condition_concept_id IN {} 
""".format(cdmDatabaseSchema, cdmDatabaseSchema, cdmDatabaseSchema, tuple(df_autoimmune["Id"].values.tolist()),
           tuple(df_drugs.values.tolist()),
           tuple(df_type.values.tolist()))

cursor.execute(sql)
result2 = cursor.fetchall()
# print("========== result2")
result2 = pd.DataFrame(result2, columns=["condition_concept_id", "person_id", "condition_start_date"])
# print(result2.head())

# %%
column_list = ["DRUG_CONCEPT_ID", "INGREDIENT_CONCEPT_ID", "AMOUNT_VALUE", "AMOUNT_UNIT_CONCEPT_ID",
               "NUMERATOR_VALUE", "NUMERATOR_UNIT_CONCEPT_ID", "DENOMINATOR_VALUE", "DENOMINATOR_UNIT_CONCEPT_ID",
               "BOX_SIZE", "VALID_START_DATE", "VALID_END_DATE", "INVALID_REASON"]
sql = """
SELECT *
FROM {}.drug_strength
WHERE drug_concept_id IN 
    {} AND ingredient_concept_id IN (1518254, 1550557)
""".format(cdmDatabaseSchema, tuple(df_drugs.values.tolist()))

cursor.execute(sql)
result3 = cursor.fetchall()
# print("========== result3")
result3 = pd.DataFrame(result3, columns=column_list)
# print(result3.head())
cursor.close()

db_connection.close()
# data read end from database

# %%
data_input = result1
data_failed = result2
data_translation = result3

data_input = data_input.rename(columns=str.lower)
data_failed = data_failed.rename(columns=str.lower)
data_translation = data_translation.rename(columns=str.lower)

# data_failed["condition_start_date"] = pd.to_datetime(data_failed["condition_start_date"])

# print(data_input.head())
# print(data_failed.head())
# print(data_translation.head())

data_translation["drug_value"] = data_translation["amount_value"].combine_first(data_translation["numerator_value"])
# print(data_translation.loc[data_translation["drug_concept_id"] == 41122201].values[0])
data_translation = data_translation[['drug_concept_id', 'ingredient_concept_id', 'drug_value']]

data_translation["drug_value"] = pd.to_numeric(data_translation["drug_value"])

data_translation.loc[data_translation["ingredient_concept_id"] == 1518254, "drug_value"] = \
    data_translation[data_translation["ingredient_concept_id"] == 1518254]["drug_value"] * 6.25
data_translated = data_translation

data_input = data_input[
    ["person_id", "drug_concept_id", "drug_exposure_start_date", "drug_exposure_end_date", "drug_type_concept_id",
     "quantity", "days_supply"]]
# print(data_input.head())

data_input = pd.merge(data_input, data_translated, on="drug_concept_id")
# print(data_input.head())

data_input["drug_value"] = pd.to_numeric(data_input["drug_value"])
data_input["quantity"] = pd.to_numeric(data_input["quantity"])
data_input["drug_value"] = data_input["quantity"] * data_input["drug_value"]


# print(data_input.head())


# %%
def make_data_output_total(temp2):
    date_temp_1 = temp2["drug_exposure_start_date"].min() + pd.to_timedelta(90, "d")  # datetime.date
    date_temp_2 = temp2["drug_exposure_start_date"].max() + pd.to_timedelta(90, "d")  # datetime.date

    temp2_failed = data_failed[(data_failed["person_id"] == temp2["person_id"].iloc(0)[0])
                               & (data_failed["condition_start_date"] >= date_temp_1)
                               & (data_failed["condition_start_date"] <= date_temp_2)
                               ]

    temp2 = pd.DataFrame({'person_id': [temp2["person_id"].iloc[0]],
                          'start_date': temp2["drug_exposure_start_date"].min(),
                          "end_date": temp2["drug_exposure_end_date"].max(),
                          'drug_sum': temp2["drug_value"].values.sum(),
                          "duration_sum": temp2["days_supply"].values.sum(),
                          "is_pulse": temp2["drug_value"].values.max() >= 250,
                          'bonefracture': 0,
                          'osteonecrosis': 0,
                          'osteoporosis': 0})

    if len(temp2_failed) >= 1:
        if np.isin(temp2_failed["condition_concept_id"].values, df_type_2["Id"].values).any():
            temp2["bonefracture"] = 1

        if np.isin(temp2_failed["condition_concept_id"].values, df_type_1["Id"].values).any():
            temp2["osteonecrosis"] = 1

        if np.isin(temp2_failed["condition_concept_id"].values, df_type_3["Id"].values).any():
            temp2["osteoporosis"] = 1

    return temp2


# %%
data_output_total = pd.DataFrame()
patient_unique = pd.unique(data_input["person_id"])

for i in range(len(patient_unique)):
    # for i in range(100):
    temp = data_input[data_input["person_id"] == patient_unique[i]]

    temp = temp.sort_values(by="drug_exposure_start_date")
    temp = temp.sort_values(by="drug_exposure_end_date")

    index_raw = temp["drug_exposure_start_date"][1: len(temp)].values - temp["drug_exposure_end_date"][
                                                                        0:len(temp) - 1].values
    index = np.where(index_raw > pd.Timedelta(90, "d"))
    index = list(index[0])

    if len(index) == 0:
        temp2 = temp
        temp2 = make_data_output_total(temp2)
        data_output_total = pd.concat([data_output_total, temp2], ignore_index=True)

    else:
        start_value = 0
        index.append(len(temp) - 1)

        for i in range(len(index)):
            temp2 = temp[start_value:index[i] + 1]
            temp2 = make_data_output_total(temp2)
            data_output_total = pd.concat([data_output_total, temp2], ignore_index=True)
            start_value = index[i] + 1

# %%
result = copy.deepcopy(data_output_total)
# %%
# print(len(result))
# print(result.head())

result["start_date"] = pd.to_datetime(result["start_date"])
result["end_date"] = pd.to_datetime(result["end_date"])
result["day_average"] = result["drug_sum"] / result["duration_sum"]
result["drug_sum_original"] = result["drug_sum"]
result["drug_sum"] = np.log(result["drug_sum"])

# print(result.dtypes)

# print(result.head())

# %%
# result.to_csv("python.csv")

# %%
# result["drug_sum"].loc[(result["drug_sum"] == np.inf)] = 0

# print(result.dtypes)
# print(result[result["person_id"] == 11732])
# print(result)

# %%
import tensorflow as tf
from sklearn.metrics import roc_curve, auc, mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
import random
from sklearn.linear_model import LinearRegression

seed_num = 19
np.random.seed(seed_num)
tf.random.set_seed(seed_num)
random.seed(seed_num)


def steroid_analysis(target, min_dose=0.0, end_dose=np.Inf, pulse=False, output_name="output"):
    output = []  # pd.DataFrame()
    output_p = []  # pd.DataFrame()
    output_n = []  # pd.DataFrame()
    output_all = []  # pd.DataFrame()

    if pulse:
        target = target[target["is_pulse"] == True]
    if not pulse:
        target = target[(target["day_average"] > min_dose)
                        & (target["day_average"] <= end_dose)]

    target.drop("start_date", axis=1, inplace=True)
    target.drop("end_date", axis=1, inplace=True)
    target.drop("drug_sum_original", axis=1, inplace=True)
    # target.drop("day_average", axis=1, inplace=True)

    print(target.columns)

    # print(target["bonefracture"].value_counts()) # 5498 / 35
    # print(target["osteonecrosis"].value_counts()) # 5529 / 4
    # print(target["osteoporosis"].value_counts()) # 5500 / 33

    plt.figure(figsize=(20, 18))

    column_name = ["bonefracture", "osteonecrosis", "osteoporosis"]

    for i in range(len(column_name)):
        output_n.insert(i, np.sum(target[column_name[i]]))

        if output_n[i] != 0:
            name = column_name[i]
            """
            title = name
            drug_sum_original = target[target[column_name[i]] == 1]["drug_sum_original"]
            plt.subplot(3, 5, i*5 + 1)
            #plt.hist(drug_sum_original, bins=np.arange(0, max(drug_sum_original) + 500, 500), edgecolor='k')
            plt.hist(drug_sum_original, edgecolor='k', histtype='bar')
            plt.xlabel("Prednisone (mg)")
            plt.xlim([int(min(drug_sum_original)), int(max(drug_sum_original)*1.1)])
            plt.title(title)

            # 2
            title = "{} (log)".format(column_name[i])
            drug_sum = target[target[column_name[i]] == 1]["drug_sum"]
            plt.subplot(3, 5, i*5 + 2)
            plt.xlabel("Prednisone log (mg)")
            #plt.hist(drug_sum, bins=np.arange(0, max(drug_sum) + 2, 1), edgecolor='k')
            plt.hist(drug_sum, edgecolor='k', histtype='bar')
            plt.xlim([int(min(drug_sum)), int(max(drug_sum) * 1.1)])
            plt.title(title)
            """

            # 3
            title = "ROC Curve"
            Y = target[column_name[i]]
            X = target
            # X = target.drop(["bonefracture", "osteonecrosis", "osteoporosis"], axis=1)

            # X = target.drop(column_name[i], axis=1)
            # bonefracture , osteonecrosis, osteoporosis

            # X.drop(["bonefracture", "osteonecrosis"], axis=1, inplace=True)

            X["day_average"] = X["day_average"].replace(np.inf, 99999)
            X["is_pulse"] = X["is_pulse"].astype(int)

            """
            GLM 
            """
            '''
            model = glm(formula="{} ~ drug_sum".format(column_name[i]),
                        family=sm.families.Binomial(), data=target).fit()
            '''
            '''
            model = glm(formula="{} ~ drug_sum".format(column_name[i]),
                        family=sm.families.Binomial(), data=target).fit()
            '''
            '''
            ANN
            '''

            # train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2, random_state=seed_num)

            """
            model = tf.keras.Sequential([
                tf.keras.layers.Dense(32, activation=tf.nn.relu),
                tf.keras.layers.Dense(64, activation=tf.nn.relu),
                tf.keras.layers.Dense(32, activation=tf.nn.relu),
                #tf.keras.layers.Dense(50, activation=tf.nn.relu),
                #tf.keras.layers.Dropout(0.5),
                #tf.keras.layers.Dense(10, activation=tf.nn.relu),
                #tf.keras.layers.Dropout(0.5),
                tf.keras.layers.Dense(1, activation="sigmoid")
            ])

            model.compile(optimizer=tf.keras.optimizers.Adam(),
                          #loss=tf.keras.losses.BinaryCrossentropy(),
                          loss="mse",
                          #metrics=["accuracy", tf.keras.metrics.AUC()]
                          metrics=["mae", "mse"]
                          )

            model.fit(X, Y, epochs=10)
            """

            model = LinearRegression()
            # model.fit(X, Y)

            coef = np.array([2.56286731e-22, 1.48522145e-16, -8.15455989e-18, -3.94391729e-17,
                             1.00000000e+00, 2.01103086e-16, -4.05133295e-16, 9.14795583e-20])

            model.coef_ = coef
            model.intercept_ = -1.177877240188252e-15

            print(model.coef_, model.intercept_)

            print("=====")

            p = model.predict(X)

            # print(p)

            mae = mean_absolute_error(Y, p)
            print("mae : ", mae)
            mse = mean_squared_error(Y, p)
            print("mse : ", mse)
            r2 = r2_score(Y, p)
            print("r2_score : ", r2)

            plt.subplot(3, 5, i * 5 + 3)
            plt.scatter(Y, p)

            fpr, tpr, thresholds = roc_curve(target[column_name[i]], p)
            # fpr, tpr, thresholds = roc_curve(Y, p)

            roc_auc = auc(fpr, tpr)
            print("auc : ", roc_auc)

            """            




            # cut-off youdens j
            J = np.argmax(tpr - fpr)

            roc_auc = auc(fpr, tpr)
            print("auc : ", roc_auc)

            plt.subplot(3, 5, i*5 + 3)
            plt.plot(fpr, tpr, roc_auc, label="auc : {}".format(roc_auc))
            plt.scatter(fpr[J], tpr[J])
            plt.xlim([0.0, 1.0])
            plt.title(title)
            plt.legend()

            # 4
            title = "cutoff analysis"
            sens = pd.DataFrame(tpr, index=thresholds)
            sens.drop(sens[sens.index.values > 1].index, inplace=True)  # 1넘는 값이 있음 ... ?
            spec = pd.DataFrame(1 - fpr, index=thresholds)
            spec.drop(spec[spec.index.values > 1].index, inplace=True)  # 1 넘는 값이 있음 ... ?


            plt.subplot(3, 5, i*5 + 4)
            plt.plot(sens, label="Sensitivity")
            plt.plot(spec, color="red", label="Specificity")
            plt.legend()
            plt.title(title)
            """

            """
            # 5
            title = "Probability Plot"
            out = (np.log(thresholds[J] / (1 - thresholds[J])) - model.params["Intercept"]) / model.params["drug_sum"]
            e_out = np.exp(out)

            x1_range = np.arange(min(target["drug_sum"]), max(target["drug_sum"]) * 1.05, 0.1)
            logits = model.params["Intercept"] + model.params["drug_sum"] * x1_range
            probs = np.exp(logits) / (1 + np.exp(logits))
            plt.subplot(3, 5, i*5 + 5)
            plt.plot(np.exp(x1_range), probs)
            plt.ylim([0, 1])
            plt.title(title)
            """

            """
            output_p.insert(i, thresholds[J])
            #output.insert(i, e_out)
            output.insert(i, 0)
            output_all.insert(i, len(target))
            """

    plt.savefig("data/results/{}.jpg".format(output_name))

    # print(output_p)
    # print(output)
    # print(output_n)
    # print(output_all)

    to_file = pd.DataFrame([output_p, output, output_n, output_all],
                           columns=['Bonefracture', 'Osteonecrosis', 'Osteoporosis'],
                           index=['Cutoff Probablity', 'Cutoff Value', 'Number of Items', 'Total Items']
                           )

    to_file.to_csv("data/results/{}.csv".format(output_name))


plt.close()

steroid_analysis(result, 0, np.Inf, pulse=False, output_name="linear_regression_all")
# steroid_analysis(result, min_dose=0, end_dose=7.5, output_name = '1_output_low_dose')
# steroid_analysis(result, min_dose=7.5, end_dose=30, output_name = '1_output_medium_dose')
# steroid_analysis(result, min_dose=30, end_dose=100, output_name = '1_output_high_dose')
# steroid_analysis(result, min_dose=100, end_dose=np.Inf, output_name = '1_output_very_high_dose')
# steroid_analysis(result, pulse=True, output_name='1_output_pulse')


# %%
