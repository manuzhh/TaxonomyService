import json


class ConfigReader:

    config_name = 'config.json'
    database_type_key = 'database-type'
    config_id_key = 'config-id'
    session_id_key = 'session-id'
    config_template_id_key = 'config-template-id'
    config_builder_type_key = 'config-builder-type'
    configs_location_key = 'configs-location'

    # expects a keyword, contained in the config
    # returns the corresponding value from the config
    @staticmethod
    def read_value(key):
        config_path = ConfigReader.config_name
        with open(config_path) as json_file:
            conf = json.load(json_file)
            return conf[key]

    # expects a list of keywords, contained in the config
    # returns the corresponding values from the config
    @staticmethod
    def read_values(keys):
        config_path = ConfigReader.config_name
        with open(config_path) as json_file:
            conf = json.load(json_file)
            values = list()
            for key in keys:
                values.append(conf[key])
            return values

    # returns database type
    @staticmethod
    def get_db_type():
        return ConfigReader.read_value(ConfigReader.database_type_key)

    # returns session id
    @staticmethod
    def get_session_id():
        return ConfigReader.read_value(ConfigReader.session_id_key)

    # returns config id
    @staticmethod
    def get_config_id():
        return ConfigReader.read_value(ConfigReader.config_id_key)

    # returns config template id
    @staticmethod
    def get_config_template_id():
        return ConfigReader.read_value(ConfigReader.config_template_id_key)

    # returns config builder type
    @staticmethod
    def get_config_builder_type():
        return ConfigReader.read_value(ConfigReader.config_builder_type_key)

    # returns configs location
    @staticmethod
    def get_configs_location():
        return ConfigReader.read_value(ConfigReader.configs_location_key)

    # expects a config in json format
    # sets the config
    @staticmethod
    def set_config(config_json):
        with open(ConfigReader.config_name, 'w+', encoding='utf8') as json_file:
            json.dump(config_json, json_file, ensure_ascii=False, indent=4)

    # returns the config as json
    @staticmethod
    def get_config():
        with open(ConfigReader.config_name, encoding='utf8') as json_file:
            return json.load(json_file)

    # expects a session config id
    # sets the config's session config id
    @staticmethod
    def set_session_config_id(config_id):
        conf = ConfigReader.get_config()
        conf[ConfigReader.config_id_key] = config_id
        ConfigReader.set_config(conf)
