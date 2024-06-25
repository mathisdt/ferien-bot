import configparser
import os
import logging


class Config:
    _config: configparser.ConfigParser
    _section: str

    def __init__(self, section="DEFAULT"):
        self._section = section
        configfile = f"{os.path.realpath(os.path.dirname(__file__))}/config.ini"
        if not os.path.isfile(configfile):
            logging.log(logging.ERROR, f"{configfile} not found")
            exit(1)
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        if section not in self._config:
            raise Exception(f"section [{section}] not found in config file")

    def __getattr__(self, name):
        if name in self._config[self._section]:
            return self._config[self._section][name]
        else:
            return ""

    def __getitem__(self, name):
        return self.__getattr__(name)
