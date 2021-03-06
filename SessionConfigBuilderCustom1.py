from SessionConfigReader import SessionConfigReader
from SessionLogger import SessionLogger
from ConfigReader import ConfigReader
from Storage import Storage
import copy


class SessionConfigBuilderCustom1:

    config_template = 'session_config_template.json'
    configs_location = 'session_configs'
    config_name = 'conf'

    corpus_importer_key = 'corpus_importer'
    corpus_identifier_key = 'corpus_identifier'
    categories_identifier_key = 'categories_identifier'

    preprocessor_key = 'preprocessor'
    noise_remover_key = 'noise_remover'
    stopword_remover_key = 'stopword_remover'
    stopwords_identifier_key = 'stopwords_identifier'
    additional_stopwords_key = 'additional_stopwords'
    lemmatizer_key = 'lemmatizer'

    train_test_splitter_key = 'train_test_splitter'
    train_test_split_ratio_key = 'train_test_split_ratio'
    train_test_split_random_state_key = 'train_test_split_random_state'

    vectorizer_key = 'vectorizer'
    vec_model_id_key = 'vec_model_id'
    word2vec_size_key = 'word2vec_size'
    word2vec_window_key = 'word2vec_window'
    word2vec_min_count_key = 'word2vec_min_count'
    word2vec_workers_key = 'word2vec_workers'

    vectorizer_gensim_word2vec = 'gensim-word2vec'

    word_vec_to_doc_vec_key = 'word-vec_to_doc-vec'
    feature_vec_dim_key = 'feature_vec_dim'

    classifier_key = 'classifier'
    classifier_keras_nn = 'keras_nn'
    classification_interpreter_key = 'classification_interpreter'
    keras_nn_default_output_layer_size_key = 'keras_nn_default_output_layer_size'
    keras_nn_model_id_key = 'keras_nn_model_id'

    classification_interpreter_custom1 = 'custom1'
    classification_interpreter_custom2 = 'custom2'
    classification_interpreter_output_threshold_key = 'classification_interpreter_output_threshold'
    similarity_function_key = 'similarity_function'

    keras_nn_loss_key = 'keras_nn_loss'
    keras_nn_optimizer_key = 'keras_nn_optimizer'
    keras_nn_metrics_key = 'keras_nn_metrics'
    keras_nn_epochs_key = 'keras_nn_epochs'
    keras_nn_batch_size_key = 'keras_nn_batch_size'

    keras_nn_default_activation_key = 'keras_nn_default_activation'
    keras_nn_default_output_activation_key = 'keras_nn_default_output_activation'
    keras_nn_default_layer_size_key = 'keras_nn_default_layer_size'
    keras_nn_default_layer_type_key = 'keras_nn_default_layer_type'
    keras_nn_default_layer_count_key = 'keras_nn_default_layer_count'
    keras_nn_layers_key = 'keras_nn_layers'

    # expects a config json list
    # adds keras layers info to configs
    # returns a list with new configs
    @staticmethod
    def add_keras_layers_info(configs):
        new_configs = list()
        for conf in configs:
            new_conf = copy.deepcopy(conf)
            classifier_type = new_conf[SessionConfigBuilderCustom1.classifier_key][0]
            conf_has_output_dim = SessionConfigBuilderCustom1.keras_nn_default_output_layer_size_key in new_conf
            if classifier_type != SessionConfigBuilderCustom1.classifier_keras_nn:
                if SessionConfigBuilderCustom1.keras_nn_layers_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_layers_key)
                if SessionConfigBuilderCustom1.keras_nn_default_activation_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_activation_key)
                if SessionConfigBuilderCustom1.keras_nn_default_output_activation_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_output_activation_key)
                if SessionConfigBuilderCustom1.keras_nn_default_layer_size_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_layer_size_key)
                if SessionConfigBuilderCustom1.keras_nn_default_layer_count_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_layer_count_key)
                if conf_has_output_dim:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_output_layer_size_key)
                new_configs.append(new_conf)
            else:
                conf_layers = list()
                if SessionConfigBuilderCustom1.keras_nn_layers_key in new_conf:
                    conf_layers = new_conf[SessionConfigBuilderCustom1.keras_nn_layers_key]
                output_dim = new_conf[SessionConfigBuilderCustom1.keras_nn_default_output_layer_size_key][0]
                new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_output_layer_size_key)
                # individual layers
                idx = 0
                n_custom_layers = len(conf_layers)
                while idx < n_custom_layers:
                    new_c_conf = copy.deepcopy(new_conf)
                    layers_list = copy.deepcopy(conf_layers)
                    layers = layers_list.pop(idx)
                    last_layer = layers[len(layers)-1]
                    last_layer_out_dim = last_layer[1]
                    if last_layer_out_dim == output_dim:
                        new_c_conf[SessionConfigBuilderCustom1.keras_nn_layers_key] = [layers]
                        new_configs.append(new_c_conf)
                    idx = idx + 1
                # constructed layers
                if (
                    SessionConfigBuilderCustom1.keras_nn_layers_key in new_conf and
                    SessionConfigBuilderCustom1.keras_nn_default_output_activation_key in new_conf and
                    SessionConfigBuilderCustom1.keras_nn_default_layer_size_key in new_conf and
                    SessionConfigBuilderCustom1.keras_nn_default_layer_type_key in new_conf and
                    SessionConfigBuilderCustom1.keras_nn_default_layer_count_key in new_conf and
                    conf_has_output_dim
                ):
                    def_activations = new_conf[SessionConfigBuilderCustom1.keras_nn_default_activation_key]
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_activation_key)
                    def_out_activations = new_conf[SessionConfigBuilderCustom1.keras_nn_default_output_activation_key]
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_output_activation_key)
                    def_layer_sizes = new_conf[SessionConfigBuilderCustom1.keras_nn_default_layer_size_key]
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_layer_size_key)
                    layer_types = new_conf[SessionConfigBuilderCustom1.keras_nn_default_layer_type_key]
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_layer_type_key)
                    def_layer_counts = new_conf[SessionConfigBuilderCustom1.keras_nn_default_layer_count_key]
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_layer_count_key)
                    for activation in def_activations:
                        for out_activation in def_out_activations:
                            for layer_size in def_layer_sizes:
                                for layer_type in layer_types:
                                    for layer_count in def_layer_counts:
                                        new_c_conf = copy.deepcopy(new_conf)
                                        layers = []
                                        idx = 0
                                        while idx < layer_count:
                                            layer = []
                                            layer.append([layer_type])
                                            if idx == layer_count-1:
                                                layer.append([output_dim])
                                                layer.append([out_activation])
                                            else:
                                                layer.append([layer_size])
                                                layer.append([activation])
                                            layers.append(layer)
                                            idx = idx + 1
                                        new_c_conf[SessionConfigBuilderCustom1.keras_nn_layers_key] = [layers]
                                        new_configs.append(new_c_conf)
                else:
                    new_configs.append(new_conf)
        return new_configs

    # expects a config json list
    # adds batch size info to configs
    # returns a list with new configs
    @staticmethod
    def add_keras_batchsize_info(configs):
        new_configs = list()
        for conf in configs:
            classifier_type = conf[SessionConfigBuilderCustom1.classifier_key][0]
            if classifier_type != SessionConfigBuilderCustom1.classifier_keras_nn:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.keras_nn_batch_size_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_batch_size_key)
                new_configs.append(new_conf)
            else:
                conf_batchsizes = conf[SessionConfigBuilderCustom1.keras_nn_batch_size_key]
                idx = 0
                while idx < len(conf_batchsizes):
                    new_conf = copy.deepcopy(conf)
                    batchsizes = copy.deepcopy(conf_batchsizes)
                    batchsize = batchsizes.pop(idx)
                    new_conf[SessionConfigBuilderCustom1.keras_nn_batch_size_key] = [batchsize]
                    new_configs.append(new_conf)
                    idx = idx + 1
        return new_configs

    # expects a config json list
    # adds epochs info to configs
    # returns a list with new configs
    @staticmethod
    def add_keras_epochs_info(configs):
        new_configs = list()
        for conf in configs:
            classifier_type = conf[SessionConfigBuilderCustom1.classifier_key][0]
            if classifier_type != SessionConfigBuilderCustom1.classifier_keras_nn:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.keras_nn_epochs_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_epochs_key)
                new_configs.append(new_conf)
            else:
                conf_epochs_list = conf[SessionConfigBuilderCustom1.keras_nn_epochs_key]
                idx = 0
                while idx < len(conf_epochs_list):
                    new_conf = copy.deepcopy(conf)
                    epochs_list = copy.deepcopy(conf_epochs_list)
                    epochs = epochs_list.pop(idx)
                    new_conf[SessionConfigBuilderCustom1.keras_nn_epochs_key] = [epochs]
                    new_configs.append(new_conf)
                    idx = idx + 1
        return new_configs

    # expects a config json list
    # adds nn metrics info to configs
    # returns a list with new configs
    @staticmethod
    def add_keras_metrics_info(configs):
        new_configs = list()
        for conf in configs:
            classifier_type = conf[SessionConfigBuilderCustom1.classifier_key][0]
            if classifier_type != SessionConfigBuilderCustom1.classifier_keras_nn:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.keras_nn_metrics_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_metrics_key)
                new_configs.append(new_conf)
            else:
                conf_metrics_list = conf[SessionConfigBuilderCustom1.keras_nn_metrics_key]
                idx = 0
                while idx < len(conf_metrics_list):
                    new_conf = copy.deepcopy(conf)
                    metrics_list = copy.deepcopy(conf_metrics_list)
                    metrics = metrics_list.pop(idx)
                    new_conf[SessionConfigBuilderCustom1.keras_nn_metrics_key] = [metrics]
                    new_configs.append(new_conf)
                    idx = idx + 1
        return new_configs

    # expects a config json list
    # adds optimizer info to configs
    # returns a list with new configs
    @staticmethod
    def add_keras_optimizer_info(configs):
        new_configs = list()
        for conf in configs:
            classifier_type = conf[SessionConfigBuilderCustom1.classifier_key][0]
            if classifier_type != SessionConfigBuilderCustom1.classifier_keras_nn:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.keras_nn_optimizer_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_optimizer_key)
                new_configs.append(new_conf)
            else:
                conf_optimizers = conf[SessionConfigBuilderCustom1.keras_nn_optimizer_key]
                idx = 0
                while idx < len(conf_optimizers):
                    new_conf = copy.deepcopy(conf)
                    optimizers = copy.deepcopy(conf_optimizers)
                    optimizer = optimizers.pop(idx)
                    new_conf[SessionConfigBuilderCustom1.keras_nn_optimizer_key] = [optimizer]
                    new_configs.append(new_conf)
                    idx = idx + 1
        return new_configs

    # expects a config json list
    # adds loss function info to configs
    # returns a list with new configs
    @staticmethod
    def add_keras_loss_function_info(configs):
        new_configs = list()
        for conf in configs:
            classifier_type = conf[SessionConfigBuilderCustom1.classifier_key][0]
            if classifier_type != SessionConfigBuilderCustom1.classifier_keras_nn:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.keras_nn_loss_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_loss_key)
                new_configs.append(new_conf)
            else:
                conf_loss_functions = conf[SessionConfigBuilderCustom1.keras_nn_loss_key]
                idx = 0
                while idx < len(conf_loss_functions):
                    new_conf = copy.deepcopy(conf)
                    loss_functions = copy.deepcopy(conf_loss_functions)
                    loss_function = loss_functions.pop(idx)
                    new_conf[SessionConfigBuilderCustom1.keras_nn_loss_key] = [loss_function]
                    new_configs.append(new_conf)
                    idx = idx + 1
        return new_configs

    # expects a config json list
    # adds similarity function info to configs
    # returns a list with new configs
    @staticmethod
    def add_similarity_function_info(configs):
        new_configs = list()
        for conf in configs:
            if SessionConfigBuilderCustom1.classification_interpreter_key in conf:
                classification_interpreter_type = conf[SessionConfigBuilderCustom1.classification_interpreter_key][0]
                if classification_interpreter_type != SessionConfigBuilderCustom1.classification_interpreter_custom1:
                    new_conf = copy.deepcopy(conf)
                    if SessionConfigBuilderCustom1.similarity_function_key in new_conf:
                        new_conf.pop(SessionConfigBuilderCustom1.similarity_function_key)
                    new_configs.append(new_conf)
                else:
                    conf_similarity_functions = conf[SessionConfigBuilderCustom1.similarity_function_key]
                    idx = 0
                    while idx < len(conf_similarity_functions):
                        new_conf = copy.deepcopy(conf)
                        similarity_functions = copy.deepcopy(conf_similarity_functions)
                        similarity_function = similarity_functions.pop(idx)
                        new_conf[SessionConfigBuilderCustom1.similarity_function_key] = [similarity_function]
                        new_configs.append(new_conf)
                        idx = idx + 1
            else:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.similarity_function_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.similarity_function_key)
                new_configs.append(new_conf)
        return new_configs

    # expects a config json list
    # adds evaluation threshold for classification output info to configs
    # returns a list with new configs
    @staticmethod
    def add_evaluation_threshold_info(configs):
        new_configs = list()
        for conf in configs:
            if SessionConfigBuilderCustom1.classification_interpreter_key in conf:
                classification_interpreter_type = conf[SessionConfigBuilderCustom1.classification_interpreter_key][0]
                if classification_interpreter_type != SessionConfigBuilderCustom1.classification_interpreter_custom2:
                    new_conf = copy.deepcopy(conf)
                    if SessionConfigBuilderCustom1.classification_interpreter_output_threshold_key in conf:
                        new_conf.pop(SessionConfigBuilderCustom1.classification_interpreter_output_threshold_key)
                    new_configs.append(new_conf)
                else:
                    if SessionConfigBuilderCustom1.classification_interpreter_output_threshold_key in conf:
                        conf_interpreter_thresholds = conf[SessionConfigBuilderCustom1.classification_interpreter_output_threshold_key]
                        idx = 0
                        while idx < len(conf_interpreter_thresholds):
                            new_conf = copy.deepcopy(conf)
                            interpreter_thresholds = copy.deepcopy(conf_interpreter_thresholds)
                            interpreter_threshold = interpreter_thresholds.pop(idx)
                            new_conf[SessionConfigBuilderCustom1.classification_interpreter_output_threshold_key] = [interpreter_threshold]
                            new_configs.append(new_conf)
                            idx = idx + 1
                    else:
                        new_conf = copy.deepcopy(conf)
                        new_configs.append(new_conf)
            else:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.classification_interpreter_output_threshold_key in conf:
                    new_conf.pop(SessionConfigBuilderCustom1.classification_interpreter_output_threshold_key)
                new_configs.append(new_conf)
        return new_configs

    # expects a config json list
    # adds classification output layer info to configs
    # returns a list with new configs
    @staticmethod
    def add_classification_output_layer_info(configs):
        new_configs = list()
        for conf in configs:
            if SessionConfigBuilderCustom1.classification_interpreter_key in conf:
                conf_classification_interpreters = conf[SessionConfigBuilderCustom1.classification_interpreter_key]
                classifier_type = conf[SessionConfigBuilderCustom1.classifier_key][0]
                idx = 0
                while idx < len(conf_classification_interpreters):
                    new_conf = copy.deepcopy(conf)
                    classification_interpreters = copy.deepcopy(conf_classification_interpreters)
                    classification_interpreter = classification_interpreters.pop(idx)
                    new_conf[SessionConfigBuilderCustom1.classification_interpreter_key] = [classification_interpreter]

                    if classifier_type == SessionConfigBuilderCustom1.classifier_keras_nn:
                        if SessionConfigBuilderCustom1.keras_nn_default_output_layer_size_key in new_conf:
                            keras_nn_default_output_layer_sizes = copy.deepcopy(conf[SessionConfigBuilderCustom1.keras_nn_default_output_layer_size_key])
                            if len(keras_nn_default_output_layer_sizes) > idx:
                                keras_nn_default_output_layer_size = keras_nn_default_output_layer_sizes.pop(idx)
                            else:
                                keras_nn_default_output_layer_size = keras_nn_default_output_layer_sizes.pop(0)
                            new_conf[SessionConfigBuilderCustom1.keras_nn_default_output_layer_size_key] = [keras_nn_default_output_layer_size]
                    else:
                        if SessionConfigBuilderCustom1.keras_nn_default_output_layer_size_key in new_conf:
                            new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_output_layer_size_key)

                    if classifier_type == SessionConfigBuilderCustom1.classifier_keras_nn:
                        keras_nn_model_ids = copy.deepcopy(conf[SessionConfigBuilderCustom1.keras_nn_model_id_key])
                        if len(keras_nn_model_ids) > idx:
                            keras_nn_model_id = keras_nn_model_ids.pop(idx)
                        else:
                            keras_nn_model_id = keras_nn_model_ids.pop(0)
                        new_conf[SessionConfigBuilderCustom1.keras_nn_model_id_key] = [keras_nn_model_id]
                    else:
                        new_conf.pop(SessionConfigBuilderCustom1.keras_nn_model_id_key)
                    new_configs.append(new_conf)
                    idx = idx + 1
            else:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.keras_nn_default_output_layer_size_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_default_output_layer_size_key)
                if SessionConfigBuilderCustom1.keras_nn_model_id_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.keras_nn_model_id_key)
                new_configs.append(new_conf)
        return new_configs

    # expects a config json list
    # adds word vector to document vector info to configs
    # returns a list with new configs
    @staticmethod
    def add_wv2dv_info(configs):
        new_configs = list()
        for conf in configs:
            if SessionConfigBuilderCustom1.word_vec_to_doc_vec_key in conf:
                conf_wv2dvs = conf[SessionConfigBuilderCustom1.word_vec_to_doc_vec_key]
                idx = 0
                while idx < len(conf_wv2dvs):
                    new_conf = copy.deepcopy(conf)
                    wv2dvs = copy.deepcopy(conf_wv2dvs)
                    wv2dv = wv2dvs.pop(idx)
                    new_conf[SessionConfigBuilderCustom1.word_vec_to_doc_vec_key] = [wv2dv]

                    feature_vec_dims = copy.deepcopy(conf[SessionConfigBuilderCustom1.feature_vec_dim_key])
                    if len(feature_vec_dims) > idx:
                        feature_vec_dim = feature_vec_dims.pop(idx)
                    else:
                        feature_vec_dim = feature_vec_dims.pop(0)
                    new_conf[SessionConfigBuilderCustom1.feature_vec_dim_key] = [feature_vec_dim]
                    new_configs.append(new_conf)
                    idx = idx + 1
            else:
                new_conf = copy.deepcopy(conf)
                new_configs.append(new_conf)
        return new_configs

    # expects a config json list
    # adds word2vec model workers info to configs
    # returns a list with new configs
    @staticmethod
    def add_w2v_workers_info(configs):
        new_configs = list()
        for conf in configs:
            if SessionConfigBuilderCustom1.vectorizer_key in conf:
                vectorizer_type = conf[SessionConfigBuilderCustom1.vectorizer_key][0]
                if vectorizer_type != SessionConfigBuilderCustom1.vectorizer_gensim_word2vec:
                    new_conf = copy.deepcopy(conf)
                    if SessionConfigBuilderCustom1.word2vec_workers_key in new_conf:
                        new_conf.pop(SessionConfigBuilderCustom1.word2vec_workers_key)
                    new_configs.append(new_conf)
                else:
                    conf_w2v_model_worker_counts = conf[SessionConfigBuilderCustom1.word2vec_workers_key]
                    idx = 0
                    while idx < len(conf_w2v_model_worker_counts):
                        new_conf = copy.deepcopy(conf)
                        w2v_model_worker_counts = copy.deepcopy(conf_w2v_model_worker_counts)
                        w2v_model_worker_count = w2v_model_worker_counts.pop(idx)
                        new_conf[SessionConfigBuilderCustom1.word2vec_workers_key] = [w2v_model_worker_count]
                        new_configs.append(new_conf)
                        idx = idx + 1
            else:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.word2vec_workers_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.word2vec_workers_key)
                new_configs.append(new_conf)
        return new_configs

    # expects a config json list
    # adds word2vec model min count info to configs
    # returns a list with new configs
    @staticmethod
    def add_w2v_min_count_info(configs):
        new_configs = list()
        for conf in configs:
            if SessionConfigBuilderCustom1.vectorizer_key in conf:
                vectorizer_type = conf[SessionConfigBuilderCustom1.vectorizer_key][0]
                if vectorizer_type != SessionConfigBuilderCustom1.vectorizer_gensim_word2vec:
                    new_conf = copy.deepcopy(conf)
                    if SessionConfigBuilderCustom1.word2vec_min_count_key in new_conf:
                        new_conf.pop(SessionConfigBuilderCustom1.word2vec_min_count_key)
                    new_configs.append(new_conf)
                else:
                    conf_w2v_model_min_counts = conf[SessionConfigBuilderCustom1.word2vec_min_count_key]
                    idx = 0
                    while idx < len(conf_w2v_model_min_counts):
                        new_conf = copy.deepcopy(conf)
                        w2v_model_mincounts = copy.deepcopy(conf_w2v_model_min_counts)
                        w2v_model_mincount = w2v_model_mincounts.pop(idx)
                        new_conf[SessionConfigBuilderCustom1.word2vec_min_count_key] = [w2v_model_mincount]
                        new_configs.append(new_conf)
                        idx = idx + 1
            else:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.word2vec_min_count_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.word2vec_min_count_key)
                new_configs.append(new_conf)
        return new_configs

    # expects a config json list
    # adds word2vec model window size info to configs
    # returns a list with new configs
    @staticmethod
    def add_w2v_window_info(configs):
        new_configs = list()
        for conf in configs:
            if SessionConfigBuilderCustom1.vectorizer_key in conf:
                vectorizer_type = conf[SessionConfigBuilderCustom1.vectorizer_key][0]
                if vectorizer_type != SessionConfigBuilderCustom1.vectorizer_gensim_word2vec:
                    new_conf = copy.deepcopy(conf)
                    if SessionConfigBuilderCustom1.word2vec_window_key in new_conf:
                        new_conf.pop(SessionConfigBuilderCustom1.word2vec_window_key)
                    new_configs.append(new_conf)
                else:
                    conf_w2v_model_window_sizes = conf[SessionConfigBuilderCustom1.word2vec_window_key]
                    idx = 0
                    while idx < len(conf_w2v_model_window_sizes):
                        new_conf = copy.deepcopy(conf)
                        w2v_model_window_sizes = copy.deepcopy(conf_w2v_model_window_sizes)
                        w2v_model_window_size = w2v_model_window_sizes.pop(idx)
                        new_conf[SessionConfigBuilderCustom1.word2vec_window_key] = [w2v_model_window_size]
                        new_configs.append(new_conf)
                        idx = idx + 1
            else:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.word2vec_window_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.word2vec_window_key)
                new_configs.append(new_conf)
        return new_configs

    # expects a config json list
    # adds word2vec model size info to configs
    # returns a list with new configs
    @staticmethod
    def add_w2v_size_info(configs):
        new_configs = list()
        for conf in configs:
            if SessionConfigBuilderCustom1.vectorizer_key in conf:
                vectorizer_type = conf[SessionConfigBuilderCustom1.vectorizer_key][0]
                if vectorizer_type != SessionConfigBuilderCustom1.vectorizer_gensim_word2vec:
                    new_conf = copy.deepcopy(conf)
                    if SessionConfigBuilderCustom1.word2vec_size_key in new_conf:
                        new_conf.pop(SessionConfigBuilderCustom1.word2vec_size_key)
                    new_configs.append(new_conf)
                else:
                    conf_w2v_model_sizes = conf[SessionConfigBuilderCustom1.word2vec_size_key]
                    idx = 0
                    while idx < len(conf_w2v_model_sizes):
                        new_conf = copy.deepcopy(conf)
                        w2v_model_sizes = copy.deepcopy(conf_w2v_model_sizes)
                        w2v_model_size = w2v_model_sizes.pop(idx)
                        new_conf[SessionConfigBuilderCustom1.word2vec_size_key] = [w2v_model_size]
                        new_configs.append(new_conf)
                        idx = idx + 1
            else:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.word2vec_size_key in new_conf:
                    new_conf.pop(SessionConfigBuilderCustom1.word2vec_size_key)
                new_configs.append(new_conf)
        return new_configs

    # expects a config json list
    # adds vectorizer info to configs
    # returns a list with new configs
    @staticmethod
    def add_vectorizer_info(configs):
        new_configs = list()
        for conf in configs:
            if SessionConfigBuilderCustom1.vectorizer_key in conf:
                conf_vectorizers = conf[SessionConfigBuilderCustom1.vectorizer_key]
                idx = 0
                while idx < len(conf_vectorizers):
                    new_conf = copy.deepcopy(conf)
                    vectorizers = copy.deepcopy(conf_vectorizers)
                    vectorizer = vectorizers.pop(idx)
                    new_conf[SessionConfigBuilderCustom1.vectorizer_key] = [vectorizer]

                    if SessionConfigBuilderCustom1.vec_model_id_key in conf:
                        vectorizer_model_ids = copy.deepcopy(conf[SessionConfigBuilderCustom1.vec_model_id_key])
                        if len(vectorizer_model_ids) > idx:
                            vectorizer_model_id = vectorizer_model_ids.pop(idx)
                        else:
                            vectorizer_model_id = vectorizer_model_ids.pop(0)
                        new_conf[SessionConfigBuilderCustom1.vec_model_id_key] = [vectorizer_model_id]
                    new_configs.append(new_conf)
                    idx = idx + 1
            else:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.vec_model_id_key in new_conf:
                    new_conf[SessionConfigBuilderCustom1.vec_model_id_key] = [new_conf[SessionConfigBuilderCustom1.vec_model_id_key][0]]
                new_configs.append(new_conf)
        return new_configs

    # expects a config json list
    # adds stopword removal info to configs
    # returns a list with new configs
    @staticmethod
    def add_stopword_removal_info(configs):
        new_configs = list()
        for conf in configs:
            if SessionConfigBuilderCustom1.stopword_remover_key in conf:
                conf_stopword_removers = conf[SessionConfigBuilderCustom1.stopword_remover_key]
                idx = 0
                while idx < len(conf_stopword_removers):
                    new_conf = copy.deepcopy(conf)
                    stopword_removers = copy.deepcopy(conf_stopword_removers)
                    stopword_remover = stopword_removers.pop(idx)
                    new_conf[SessionConfigBuilderCustom1.stopword_remover_key] = [stopword_remover]

                    if SessionConfigBuilderCustom1.stopwords_identifier_key in conf:
                        stopwords_ids = copy.deepcopy(conf[SessionConfigBuilderCustom1.stopwords_identifier_key])
                        if len(stopwords_ids) > idx:
                            stopwords_id = stopwords_ids.pop(idx)
                        else:
                            stopwords_id = stopwords_ids.pop(0)
                        new_conf[SessionConfigBuilderCustom1.stopwords_identifier_key] = [stopwords_id]

                    if SessionConfigBuilderCustom1.additional_stopwords_key in conf:
                        additional_stopwords_list = copy.deepcopy(conf[SessionConfigBuilderCustom1.additional_stopwords_key])
                        if len(additional_stopwords_list) > idx:
                            additional_stopwords = additional_stopwords_list.pop(idx)
                        else:
                            additional_stopwords = additional_stopwords_list.pop(0)
                        new_conf[SessionConfigBuilderCustom1.additional_stopwords_key] = [additional_stopwords]
                    new_configs.append(new_conf)
                    idx = idx + 1
            else:
                new_conf = copy.deepcopy(conf)
                if SessionConfigBuilderCustom1.stopwords_identifier_key in conf:
                    new_conf.pop(SessionConfigBuilderCustom1.stopwords_identifier_key)
                if SessionConfigBuilderCustom1.additional_stopwords_key in conf:
                    new_conf.pop(SessionConfigBuilderCustom1.additional_stopwords_key)
                new_configs.append(new_conf)
        return new_configs

    # expects a config json list
    # adds corpus info to configs
    # returns a list with new configs
    @staticmethod
    def add_corpus_info(configs):
        new_configs = list()
        for conf in configs:
            if SessionConfigBuilderCustom1.corpus_importer_key in conf:
                conf_corpus_importers = conf[SessionConfigBuilderCustom1.corpus_importer_key]
                idx = 0
                while idx < len(conf_corpus_importers):
                    new_conf = copy.deepcopy(conf)
                    corpus_importers = copy.deepcopy(conf_corpus_importers)
                    importer = corpus_importers.pop(idx)
                    new_conf[SessionConfigBuilderCustom1.corpus_importer_key] = [importer]

                    corpus_ids = copy.deepcopy(conf[SessionConfigBuilderCustom1.corpus_identifier_key])
                    if len(corpus_ids) > idx:
                        corpus_id = corpus_ids.pop(idx)
                    else:
                        corpus_id = corpus_ids.pop(0)
                    new_conf[SessionConfigBuilderCustom1.corpus_identifier_key] = [corpus_id]

                    categories_ids = copy.deepcopy(conf[SessionConfigBuilderCustom1.categories_identifier_key])
                    if len(categories_ids) > idx:
                        categories_id = categories_ids.pop(idx)
                    else:
                        categories_id = categories_ids.pop(0)
                    new_conf[SessionConfigBuilderCustom1.categories_identifier_key] = [categories_id]
                    new_configs.append(new_conf)
                    idx = idx + 1
            else:
                new_conf = copy.deepcopy(conf)
                new_configs.append(new_conf)
        return new_configs

    # expects a config json list and a parameter key
    # adds simple config info to configs
    # returns a list with new configs
    @staticmethod
    def add_simple_config_info(configs, key):
        new_configs = list()
        for conf in configs:
            if key in conf:
                conf_values = conf[key]
                idx = 0
                while idx < len(conf_values):
                    new_conf = copy.deepcopy(conf)
                    values = copy.deepcopy(conf_values)
                    value = values.pop(idx)
                    new_conf[key] = [value]
                    new_configs.append(new_conf)
                    idx = idx + 1
            else:
                new_conf = copy.deepcopy(conf)
                new_configs.append(new_conf)
        return new_configs

    # expects a list of configs
    # adds the complex config information to all configs
    # returns a list of configs
    @staticmethod
    def add_all_config_info(configs):
        configs = SessionConfigBuilderCustom1.add_corpus_info(configs)
        configs = SessionConfigBuilderCustom1.add_simple_config_info(configs, SessionConfigBuilderCustom1.preprocessor_key)
        configs = SessionConfigBuilderCustom1.add_simple_config_info(configs, SessionConfigBuilderCustom1.noise_remover_key)
        configs = SessionConfigBuilderCustom1.add_stopword_removal_info(configs)
        configs = SessionConfigBuilderCustom1.add_simple_config_info(configs, SessionConfigBuilderCustom1.lemmatizer_key)
        configs = SessionConfigBuilderCustom1.add_simple_config_info(configs, SessionConfigBuilderCustom1.train_test_splitter_key)
        configs = SessionConfigBuilderCustom1.add_simple_config_info(configs, SessionConfigBuilderCustom1.train_test_split_ratio_key)
        configs = SessionConfigBuilderCustom1.add_simple_config_info(configs, SessionConfigBuilderCustom1.train_test_split_random_state_key)
        configs = SessionConfigBuilderCustom1.add_vectorizer_info(configs)
        configs = SessionConfigBuilderCustom1.add_w2v_size_info(configs)
        configs = SessionConfigBuilderCustom1.add_w2v_window_info(configs)
        configs = SessionConfigBuilderCustom1.add_w2v_min_count_info(configs)
        configs = SessionConfigBuilderCustom1.add_w2v_workers_info(configs)
        configs = SessionConfigBuilderCustom1.add_wv2dv_info(configs)
        configs = SessionConfigBuilderCustom1.add_simple_config_info(configs, SessionConfigBuilderCustom1.lemmatizer_key)
        configs = SessionConfigBuilderCustom1.add_classification_output_layer_info(configs)
        configs = SessionConfigBuilderCustom1.add_evaluation_threshold_info(configs)
        configs = SessionConfigBuilderCustom1.add_similarity_function_info(configs)
        configs = SessionConfigBuilderCustom1.add_keras_loss_function_info(configs)
        configs = SessionConfigBuilderCustom1.add_keras_optimizer_info(configs)
        configs = SessionConfigBuilderCustom1.add_keras_metrics_info(configs)
        configs = SessionConfigBuilderCustom1.add_keras_epochs_info(configs)
        configs = SessionConfigBuilderCustom1.add_keras_batchsize_info(configs)
        configs = SessionConfigBuilderCustom1.add_keras_layers_info(configs)
        return configs

    # constructs a number of session configs, stores them
    # returns list with config identifiers
    @staticmethod
    def create_session_configs(configs_location=None, delete_old_configs=1):
        if configs_location is None:
            configs_location = ConfigReader.get_configs_location()
        if delete_old_configs:
            Storage.delete_location(configs_location)

        configs = [SessionConfigReader.get_config_template()]

        configs = SessionConfigBuilderCustom1.add_all_config_info(configs)

        n_configs = len(configs)

        SessionLogger.log('Constructed ' + str(n_configs) + ' new session configs from template: \'' + ConfigReader.get_config_template_id() + '\'.')

        config_ids = list()
        idx = 0
        for conf in configs:
            config_id = configs_location + '/' + SessionConfigBuilderCustom1.config_name + str(idx+1)
            SessionConfigReader.set_config(conf, config_id)
            config_ids.append(config_id)
            idx = idx + 1

        SessionLogger.log('Stored ' + str(n_configs) + ' session configs in \'' + configs_location + '\'.')

        return config_ids

    # returns the configs location
    @staticmethod
    def get_configs_location():
        return ConfigReader.get_configs_location()

    # returns the general config name
    @staticmethod
    def get_configs_name():
        return SessionConfigBuilderCustom1.config_name
