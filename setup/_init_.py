from setup import config_setup
from setup import logging_setup
import os
import configparser
import logging

# Sets global variables like logger and config which can then imported into other modules
# This helps to keep the same logger instance in all functions across the project.
# all config parameters in [DIRECTORIES] and [FILES] are changed to absolute paths


config: configparser.ConfigParser = config_setup.get_config("./config.ini")
logger: logging.Logger = logging_setup.init_logger(
    logger_name='example_logger',
    logfile_name='logs\\example.log',
    console_level=logging.INFO,  # available levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
    file_level=logging.DEBUG,
    mail_handler=False)
PROJECT_NAME = "Projektarbeit_Neutronenradiographie"

# ensure that absolute paths are used in the config
if config.has_section("DIRECTORIES"):
    for key, directory in config["DIRECTORIES"].items():
        path = ""
        if "./" in directory[:2]:
            name = os.path.dirname(__file__)
            var = name.split("\\")[:-1]
            p1 = "/".join(var)
            path = os.path.abspath(os.path.join(p1, directory[2:]))
        elif directory != "":
            path = os.path.abspath(directory)
        config["DIRECTORIES"][key] = path
        if path != "":
            os.makedirs(path, exist_ok=True)
if config.has_section("FILES"):
    for key, file in config["FILES"].items():
        path = ""
        if "./" in file[:2]:
            name = os.path.dirname(__file__)
            var = name.split("\\")[:-1]
            p1 = "/".join(var)
            path = os.path.abspath(os.path.join(p1, file[2:]))
        elif file != "":
            path = os.path.abspath(file)
        config["FILES"][key] = path