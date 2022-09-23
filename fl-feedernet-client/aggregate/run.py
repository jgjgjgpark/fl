import os
import traceback

import argparse

import numpy
import pandas as pd
import psycopg2
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import utils

#DB_USER = "readonlyuser"
#DB_PASSWORD = "x741TuPDpO1y"
#DB_URL = "203.245.2.199:5432"
#DB_DATABASE = "omop"
#DB_SCHEMA = "cdm_synpuf"
#DB_HOST, DB_PORT = DB_URL.split(":")

DB_USER = os.environ.get('MEDICAL_RECORDS_USER')
DB_PASSWORD = os.environ.get('MEDICAL_RECORDS_PW')
DB_URL = os.environ.get('MEDICAL_RECORDS_URL')
DB_DATABASE = os.environ.get('MEDICAL_RECORDS_DATABASE')
DB_SCHEMA = os.environ.get('MEDICAL_RECORDS_SCHEMA')
DB_HOST, DB_PORT = DB_URL.split(":")

print("database environment : {} / {} / {} / {} / {} ".format(DB_HOST, DB_PORT, DB_SCHEMA, DB_DATABASE, DB_USER))

DATA_SIZE = 30000

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


def get_data(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
    SELECT con.concept_name AS condition, gen.concept_name AS gender
    FROM cdm_synpuf.condition_occurrence occ
    LEFT JOIN cdm_synpuf.concept con ON occ.condition_concept_id=con.concept_id
    LEFT JOIN cdm_synpuf.person per ON occ.person_id=per.person_id
    LEFT JOIN cdm_synpuf.concept gen ON per.gender_concept_id=gen.concept_id
    ORDER BY RANDOM()
    LIMIT {}
    ;
    """.format(DATA_SIZE))
    result = cursor.fetchall()
    #print(result)
    cursor.close()

    result_pd = pd.DataFrame(result, columns=["condition", "gender"])

    return result_pd

"""
https://github.com/alan-turing-institute/ModMon/blob/e106f52dd3edab30b811d43631e8743ace7752fe/examples/README.md
"""
if __name__ == "__main__":

    parameter = argparse.ArgumentParser()
    parameter.add_argument("-val", default=False)

    args = parameter.parse_args()
    validation_status = args.val
    print("-validation_status: ", validation_status)

    db_connection = connection_db()

    df = get_data(db_connection)
    print(df.count())
    #print(df["condition"].value_counts())
    #print( df["gender"].value_counts())

    df["gender"] = pd.Categorical(df["gender"])
    df["gender"] = df.gender.cat.codes

    #y = df["gender"] == "MALE"
    y = df["gender"]

    df["condition"] = pd.Categorical(df["condition"])
    df["condition"] = df.condition.cat.codes

    X = df["condition"]

    scaler = MinMaxScaler()
    scaled_values = scaler.fit_transform(X.values.reshape(-1, 1))
    X = scaled_values

    #X = preprocess(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    print("size : {}, {} / {}, {}".format(len(X_train), len(y_train), len(X_test), len(y_test)))

    model = tf.keras.models.Sequential([
        tf.keras.layers.Input((1, )),
        tf.keras.layers.Dense(1024, activation=tf.nn.relu),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(512, activation=tf.nn.relu),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(256, activation=tf.nn.relu),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(128, activation=tf.nn.relu),
        tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)
    ])


    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss=tf.keras.losses.BinaryCrossentropy(),
                  metrics=['accuracy', tf.keras.metrics.AUC()] )

    if validation_status == "True":
        # test
        print("===== validation")
        total_acc = []
        total_classification_count = []
        for i in range(1, 11):
            global_weight_file = "global_weight_{}.json".format(i)
            print("global_weight_file : ", global_weight_file)
            global_weight = utils.read_weight_from_json("../script/{}".format(global_weight_file))
            model.set_weights(global_weight)

            y_evaluate = model.evaluate(X_train, y_train)
            total_acc.append(y_evaluate[1])

            y_predicts = model.predict_classes(X_test)

            unique, counts = numpy.unique(y_predicts, return_counts=True)
            predict_result = dict(zip(unique, counts))
            total_classification_count.append(predict_result)

        #print(total_acc)
        metrics = pd.DataFrame([total_acc, total_classification_count])
        print("metrics : ", metrics)
        with utils.FileWriter() as f:
            f.save_csv(file_name="total_scores.csv", data=metrics)


    else:
        print("===== train - load global weight =====")
        global_Weight = None
        weight_name = "global_weight.json"
        if os.path.isfile(weight_name):
            global_weight = utils.read_weight_from_json("global_weight.json")
            model.set_weights(global_weight)
            print("global weight exist: ", weight_name, len(global_weight))

        else:
            print("global weight not exist")

        model.fit(X_train, y_train, epochs= 30,  batch_size=16)
        y_evaluate = model.evaluate(X_test, y_test)

        print("y_evaluate : ", y_evaluate[1])

        # Create df of test metrics
        metrics = pd.DataFrame([y_evaluate[1]])

        # Save local_weight
        with utils.FileWriter() as f:
            f.write_json(file_name="local_weight.json", json_body=model.get_weights())
            f.save_csv(file_name="scores.csv", data=metrics)




