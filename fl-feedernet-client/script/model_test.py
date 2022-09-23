import json

import wtte.wtte as wtte
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import plot_model
from tensorflow.python.keras.layers import Masking, GRU, Dense, Activation
from tensorflow.python.keras.models import Sequential

import utils


def create_model():
    model = Sequential()

    model.add(Masking(mask_value= -99, input_shape=(None, 100)))
    model.add(GRU(32, activation='tanh', dropout = 0.25,return_sequences=True)) # 0.2/0.2
    model.add(GRU(20, activation='tanh', dropout = 0.25))  # returns a sequence of vectors of dimension 32
    model.add(Dense(2, kernel_initializer='uniform', activation='linear'))
    wtte_activation = wtte.output_activation(init_alpha=1.,max_beta_value=4.0).activation

    model.add(Activation(wtte_activation))


    loss = wtte.loss(kind='discrete',reduce_loss=True).loss_function
    model.compile(loss=loss, optimizer=Adam(lr=.001, clipvalue=0.5))
    return model


model = create_model()
model.summary()
print(model.get_weights())

with open("test_weight.json", "w") as json_file:
    weight_to_json = json.dumps(model.get_weights(), cls=utils.NumpyEncoder)
    json.dump(weight_to_json, json_file)

print("save json complete: ", len(weight_to_json))


#plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)