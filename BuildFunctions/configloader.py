"""
config.py
@author - Ryan Malacina (xNifty)

Handles all config based functions
"""

# Imports for ConfigLoader
import os
import configparser
import errno


def get_config_filename(default_filename):
    """Return the filename; probably not needed at this point."""
    return default_filename


def load_config(default_filename):
    """Read in the config file."""
    config = configparser.ConfigParser()
    return config.read(default_filename)


class ConfigLoader:
    """ConfigLoader"""
    def __init__(self):
        """Initialize some variables"""
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        self.config = load_config('%s.ini' % (os.path.join(self.path, 'config')),)

        self.parser = configparser.ConfigParser()

        self.errors_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../errors')
        )

    def create_directory(self):
        """Create an errors directory if needed."""
        try:
            os.mkdir(self.errors_path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def load_config_setting(self, section, var):
        """Load a config setting from the bot config."""
        self.parser.read(self.config)
        return self.parser.get(section, var)

    def load_config_setting_int(self, section, var):
        """Load int setting from bot config."""
        self.parser.read(self.config)
        return int(self.parser.get(section, var))

    def load_config_string_setting(self, section, var):
        """Load string setting from bot config."""
        self.parser.read(self.config)
        return str(self.parser.get(section, var))

    def load_config_setting_boolean(self, section, var):
        """Load a boolean bot config setting."""
        self.parser.read(self.config)
        return self.parser.getboolean(section, var)
