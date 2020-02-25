from keras.models import Sequential
from keras.layers import Dense, Conv1D, Activation, LeakyReLU
from Storage import Storage
from SessionLogger import SessionLogger
from SessionConfigReader import SessionConfigReader
import numpy as np


class ClassifierKerasNN:

    fv_col_name = 'document vector'
    cat_v_col_name = 'categories vector'
    model_id_key = 'keras_nn_model_id'
    dimension_key = 'feature_vec_dim'
    layers_key = 'keras_nn_layers'
    loss_key = 'keras_nn_loss'
    optimizer_key = 'keras_nn_optimizer'
    metrics_key = 'keras_nn_metrics'
    epochs_key = 'keras_nn_epochs'
    batch_size_key = 'keras_nn_batch_size'
    layer_type_dense = 'dense'
    layer_type_conv1d = 'conv1d'
    class_out_col_name = 'classification output'
    ext_classified = '_classified'

    # returns the model identifier, specified in the session config
    @staticmethod
    def get_model_id():
        return SessionConfigReader.read_value(ClassifierKerasNN.model_id_key)

    # expects pandas data frame, optionally an identifier for the model to train and column names referencing the vectors used for training
    # returns the model identifier
    @staticmethod
    def train_model(data_frame, model_id=None, fv_col_name=fv_col_name, cat_v_col_name=cat_v_col_name):

        # read config params
        config_keys = list()
        config_keys.append(ClassifierKerasNN.model_id_key)
        config_keys.append(ClassifierKerasNN.epochs_key)
        config_keys.append(ClassifierKerasNN.batch_size_key)
        config = SessionConfigReader.read_values(config_keys)
        if model_id is None:
            model_id = config[0]
        epochs = config[1]
        batch_size = config[2]

        # extract vector lists from data frame
        doc_vectors = data_frame[fv_col_name].tolist()
        cat_vectors = data_frame[cat_v_col_name].tolist()

        # load the model
        model = Storage.load_h5_model(model_id)
        # train the model
        model.fit(np.asarray(doc_vectors), np.asarray(cat_vectors), epochs=epochs, batch_size=batch_size)
        # store the model
        Storage.store_h5_model(model, model_id)

        # make log entry
        SessionLogger.log('Trained keras neural network \'' + model_id + '\' with ' + str(len(data_frame.index)) + ' new entries.')

        return model_id

    # expects a model, a layer type, a layer size and optionally an input dimension
    # adds a layer to the model
    # returns the model
    @staticmethod
    def add_layer(model, layer_type, layer_size, input_dim=None):
        if layer_type == ClassifierKerasNN.layer_type_conv1d:
            model.add(Conv1D(layer_size, input_dim=input_dim))
        if layer_type == ClassifierKerasNN.layer_type_dense:
            model.add(Dense(layer_size, input_dim=input_dim))
        return model

    # expects pandas data frame, optionally an identifier for the new model and column names referencing the vectors used for training
    # creates a neural network model and trains the model with the vectors from the the data frame
    # returns the identifier of the new model
    @staticmethod
    def create_model(data_frame, new_model_id=None, fv_col_name=fv_col_name, cat_v_col_name=cat_v_col_name):

        # read config params
        config_keys = list()
        config_keys.append(ClassifierKerasNN.model_id_key)
        config_keys.append(ClassifierKerasNN.dimension_key)
        config_keys.append(ClassifierKerasNN.layers_key)
        config_keys.append(ClassifierKerasNN.loss_key)
        config_keys.append(ClassifierKerasNN.optimizer_key)
        config_keys.append(ClassifierKerasNN.metrics_key)
        config = SessionConfigReader.read_values(config_keys)
        model_id = config[0]
        dimension = config[1]
        layers = config[2]
        loss = config[3]
        optimizer = config[4]
        metrics = config[5]

        # add layers to the model
        model = Sequential()
        layer_n = 0
        for layer in layers:
            layer_type = layer[0][0]
            layer_size = layer[1][0]
            layer_activation_type = layer[2][0]
            if layer_type == ClassifierKerasNN.layer_type_dense:
                if layer_n == 0:
                    model = ClassifierKerasNN.add_layer(model, layer_type, layer_size, input_dim=dimension)
                    if layer_activation_type == 'LeakyReLU':
                        model.add(LeakyReLU(alpha=0.3))
                    else:
                        model.add(Activation(layer_activation_type))
                else:
                    model = ClassifierKerasNN.add_layer(model, layer_type, layer_size)
                    if layer_activation_type == 'LeakyReLU':
                        model.add(LeakyReLU(alpha=0.3))
                    else:
                        model.add(Activation(layer_activation_type))
            layer_n = layer_n + 1

        # compile the model
        model.compile(loss=loss, optimizer=optimizer, metrics=[metrics])

        # store the  model
        if new_model_id is None:
            new_model_id = model_id
        Storage.store_h5_model(model, new_model_id)

        # make log entry
        SessionLogger.log('Created keras neural network \'' + model_id + '\'.')

        # train the model
        new_model_id = ClassifierKerasNN.train_model(data_frame, model_id=new_model_id, fv_col_name=fv_col_name, cat_v_col_name=cat_v_col_name)

        return new_model_id

    # expects pandas data frame
    # adds a column to the data frame, containing the classification output
    # returns expanded data frame
    @staticmethod
    def classify(data_frame, model_id=None, col_name=fv_col_name, new_col_name=class_out_col_name, storage_level=0, storage_name='', log=1):
        df = data_frame.copy()
        if model_id is None:
            model_id = ClassifierKerasNN.get_model_id()
        model = Storage.load_h5_model(model_id)
        df[new_col_name] = df.apply(lambda x: model.predict(np.asarray([x[col_name]]))[0], axis=1)
        log_text = 'Classified documents (' + str(len(df.index)) + ' entries).'
        if storage_level >= 1 and storage_name != '':
            storage_name = storage_name + ClassifierKerasNN.ext_classified
            Storage.store_pd_frame(df, storage_name)
            log_text = log_text + ' Stored in \'' + storage_name + '\' (column: \'' + new_col_name + '\').'
        if log:
            SessionLogger.log(log_text)
        return df
