from SessionConfigBuilderCustom1 import SessionConfigBuilderCustom1
from ConfigReader import ConfigReader


class SessionConfigBuilder:

    config_builder_type_key = 'config-builder-type'
    config_builder_custom1 = 'custom1'

    # constructs a number of session configs, stores them
    # returns list with config identifiers
    @staticmethod
    def create_session_configs(configs_location=None, delete_old_configs=1):
        config_builder_type = ConfigReader.get_config_builder_type()
        if config_builder_type == SessionConfigBuilder.config_builder_custom1:
            return SessionConfigBuilderCustom1.create_session_configs(configs_location, delete_old_configs=delete_old_configs)

    # returns the configs location
    @staticmethod
    def get_configs_location():
        config_builder_type = ConfigReader.get_config_builder_type()
        if config_builder_type == SessionConfigBuilder.config_builder_custom1:
            return SessionConfigBuilderCustom1.get_configs_location()

    # returns the general config name
    @staticmethod
    def get_configs_name():
        config_builder_type = ConfigReader.get_config_builder_type()
        if config_builder_type == SessionConfigBuilder.config_builder_custom1:
            return SessionConfigBuilderCustom1.get_configs_name()
