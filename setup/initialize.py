from setup import config_setup
from setup import logging_setup
import os
import configparser
import logging

# Sets global variables like logger and config which can then imported into other modules
# This helps to keep the same logger instance in all functions across the project.
# all config parameters in [DIRECTORIES] and [FILES] are changed to absolute paths


#config: configparser.ConfigParser = config_setup.get_prod_config()
config: configparser.ConfigParser = config_setup.get_dev_config()

logger = logging_setup.init_logger(
    logger_name='project_logger',
    #logfile_name=f'logs\\{os.getlogin()}_logfile.log',
    logfile_name=os.path.join(config.get("DIRECTORIES", "logs"), f'{os.getlogin()}_logfile.log'),
    file_level=logging.INFO,
    console_level=logging.INFO,
    mail_handler=False,
    error_mail_subject="[Project]",
    error_mail_recipient=config.get('MAIN', 'error_mail_recipient'))
PROJECT_NAME = "project"

# ensure that absolute paths are used in the config
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