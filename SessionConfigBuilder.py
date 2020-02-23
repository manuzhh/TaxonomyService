from SessionConfigBuilderCustom1 import SessionConfigBuilderCustom1
from ConfigReader import ConfigReader


class SessionConfigBuilder:

    config_builder_type_key = 'config-builder-type'
    config_builder_custom1 = 'custom1'

    # constructs a number of session configs, stores them
    # returns list with config identifiers
    @staticmethod
    def create_session_configs(configs_location=None):
        config_builder_type = ConfigReader.get_config_builder_type()
        if config_builder_type == SessionConfigBuilder.config_builder_custom1:
            SessionConfigBuilderCustom1.create_session_configs(configs_location)