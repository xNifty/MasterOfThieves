from .configloader import ConfigLoader


class Directory(object):
    def __init__(self):
        self.dir = ConfigLoader().load_config_string_setting('GameSettings', 'game_directory')

    def get_directory(self):
        return self.dir
