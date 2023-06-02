from configparser import ConfigParser, NoSectionError, NoOptionError


class ConfigManager:
    """This class is responsible for reading and writing the config file"""
    def __init__(self, config_file='config.ini') -> None:
        self.config = ConfigParser()
        self.config_file = config_file
        self.config.read(config_file)

    def read_config(self, section, key) -> str | int | float:
        """
        Read a value from the config file
        :param section: Section of the config file
        :param key: Key of the config file
        :return: Value of the config file
        """
        try:
            value = self.config.get(section, key)
            if value.isdigit():
                return int(value)
            else:
                return value  #
        except (NoSectionError, NoOptionError) as e:
            raise e

    def write_config(self, section, key, value) -> None:
        """
        Write a value to the config file
        :param section: Section of the config file
        :param key: Key of the config file
        :param value: Value of the config file
        """
        if not self.config.has_section(section):
            raise NoSectionError(f"Section '{section}' not found in {self.config_file}")

        self.config.set(section, key, value)

        with open(self.config_file, 'w') as f:
            self.config.write(f)
