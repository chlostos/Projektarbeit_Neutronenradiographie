import logging
import logging.handlers
import win32com.client as win32  # for mail handler
import pythoncom  # for mail handler
from pathlib import Path
import os

# for more information visit https://docs.python.org/3/library/logging.html
# mail handler needs pywin32 package installed


def get_logger(logger_name, **kwargs):
    """
    Returns the wanted logger. A new one will be create if a logger with logger_name does not exists.
    Otherwise the existing logger will be returned.
    It is advised to call get_logger if you need logging abilities in different files.

    :param logger_name: str
    :param kwargs: all params from init_logger
    :return: logger instance
    """
    logger_dict = logging.root.manager.loggerDict
    if logger_name in logger_dict:
        logger = logging.getLogger(logger_name)
    else:
        logger = init_logger(logger_name, **kwargs)
    return logger


def init_logger(logger_name='default_logger', logfile_name='log.log', console_level=logging.INFO, file_level=logging.DEBUG,
                mail_handler=False,  mail_level=logging.WARNING,
                error_mail_recipient='', error_mail_subject="[Example]") -> logging.Logger:
    Path(os.path.dirname(logfile_name)).mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    logger.addHandler(
        get_console_handler(console_level))
    logger.addHandler(
        get_file_handler(logfile_name, file_level))
    if mail_handler:
        error_mail_recipient_list = error_mail_recipient.replace(' ', '').split(',')
        for recipient in error_mail_recipient_list:
            logger.addHandler(
                get_mail_handler(recipient, error_mail_subject, mail_level))
    return logger


def get_console_handler(level=logging.INFO) -> logging.Handler:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    return console_handler


def get_file_handler(filename, level=logging.DEBUG) -> logging.Handler:
    file_log_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=262144 * 8, backupCount=10)
    file_log_handler.setLevel(level)
    file_log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    return file_log_handler


def get_mail_handler(recipient, subject, level=logging.WARNING) -> logging.Handler:
    mail_handler = OutlookHandler(recipient, subject)
    mail_handler.setLevel(level)
    mail_handler.setFormatter(logging.Formatter('%(message)s'))
    return mail_handler


class OutlookHandler(logging.Handler):
    def __init__(self, toaddrs, subject):
        logging.Handler.__init__(self)
        if isinstance(toaddrs, str):
            toaddrs = [toaddrs]
        self.toaddrs = toaddrs
        self.subject = subject

    def get_subject(self, record):
        return self.subject + " " + record.levelname + " " + record.asctime

    def emit(self, record):
        try:
            pythoncom.CoInitialize()
            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = ','.join(self.toaddrs)
            mail.Subject = self.get_subject(record)
            mail.Body = self.format(record)
            mail.Send()
        except Exception:
            self.handleError(record)