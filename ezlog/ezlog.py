import ConfigParser
import logging
import os
import random
import re
import sys
import threading
import time

_msgtype_prefixes = {
    'status'       : '\033[95mx\033[0m',
    'success'      : '\033[92m+\033[0m',
    'failure'      : '\033[91m-\033[0m',
    'debug'        : '\033[91mDEBUG\033[0m',
    'info'         : '\033[94m*\033[0m',
    'warning'      : '\033[93m!\033[0m',
    'error'        : '\033[91mERROR\033[0m',
    'exception'    : '\033[91mERROR\033[0m',
    'critical'     : '\033[91mCRITICAL\033[0m',
    'info_once'    : '\033[94m*\033[0m',
    'warning_once' : '\033[93m!\033[0m',
    }
class Logger(object):
    _one_time_infos    = set()
    _one_time_warnings = set()

    def __init__(self, logger=None):
        if logger is None:
            module = self.__module__

            logger_name = '%s.%s.%s' % (module, self.__class__.__name__, id(self))
            logger = logging.getLogger(logger_name)

        self._logger = logger

    def _getlevel(self, levelString):
        if isinstance(levelString, int):
            return levelString
        return logging._levelNames[levelString.upper()]

    def _log(self, level, msg, args, kwargs, msgtype):
        extra = kwargs.get('extra', {})
        extra.setdefault('msgtype', msgtype)
        kwargs['extra'] = extra
        self._logger.log(level, msg, *args, **kwargs)

    def indented(self, message, *args, **kwargs):
        level = self._getlevel(kwargs.pop('level', logging.INFO))
        self._log(level, message, args, kwargs, 'indented')

    def success(self, message, *args, **kwargs):
        self._log(logging.INFO, message, args, kwargs, 'success')

    def failure(self, message, *args, **kwargs):
        self._log(logging.INFO, message, args, kwargs, 'failure')

    def info_once(self, message, *args, **kwargs):
        m = message % args
        if m not in self._one_time_infos:
            if self.isEnabledFor(logging.INFO):
                self._one_time_infos.add(m)
            self._log(logging.INFO, message, args, kwargs, 'info_once')

    def warning_once(self, message, *args, **kwargs):
        m = message % args
        if m not in self._one_time_warnings:
            if self.isEnabledFor(logging.WARNING):
                self._one_time_warnings.add(m)
            self._log(logging.WARNING, message, args, kwargs, 'warning_once')

    def warn_once(self, *args, **kwargs):
        return self.warning_once(*args, **kwargs)

    def debug(self, message, *args, **kwargs):
        self._log(logging.DEBUG, message, args, kwargs, 'debug')

    def info(self, message, *args, **kwargs):
        self._log(logging.INFO, message, args, kwargs, 'info')

    def warning(self, message, *args, **kwargs):
        self._log(logging.WARNING, message, args, kwargs, 'warning')

    def warn(self, *args, **kwargs):
        return self.warning(*args, **kwargs)

    def error(self, message, *args, **kwargs):
        self._log(logging.ERROR, message, args, kwargs, 'error')
        raise Exception(message % args)

    def exception(self, message, *args, **kwargs):
        kwargs["exc_info"] = 1
        self._log(logging.ERROR, message, args, kwargs, 'exception')
        raise

    def critical(self, message, *args, **kwargs):
        self._log(logging.CRITICAL, message, args, kwargs, 'critical')

    def log(self, level, message, *args, **kwargs):
        self._log(level, message, args, kwargs, None)

    def isEnabledFor(self, level):
        effectiveLevel = self._logger.getEffectiveLevel()

        if effectiveLevel == 1:
            effectiveLevel = context.log_level
        return effectiveLevel <= level

    def setLevel(self, levelString):
        if isinstance(levelString, int):
            self._logger.setLevel(levelString)
        else:
            level = logging._levelNames[levelString.upper()]
            self._logger.setLevel(level)
        

    def addHandler(self, handler):
        self._logger.addHandler(handler)

    def removeHandler(self, handler):
        self._logger.removeHandler(handler)

    @property
    def level(self):
        return self._logger.level
    @level.setter
    def level(self, levelString):
        if isinstance(levelString, int):
            self._logger.level = levelString
        else:
            level = logging._levelNames[levelString.upper()]
            self._logger.level = level

        
        
class Formatter(logging.Formatter):
    indent    = '    '
    nlindent  = '\n' + indent

    def format(self, record):
        msg = super(Formatter, self).format(record)
        msgtype = getattr(record, 'msgtype', None)

        if msgtype is None:
            return msg

        if msgtype in _msgtype_prefixes:
            prefix = '[%s] ' % _msgtype_prefixes[msgtype]
        elif msgtype == 'indented':
            prefix = self.indent
        elif msgtype == 'animated':
            prefix = ''
        else:
            prefix = '[?] '

        msg = prefix + msg
        msg = self.nlindent.join(msg.splitlines())
        return msg
def initLogger(name='', stream=sys.stderr, log_file='', level='info'):
    logger = Logger(logging.getLogger(name))
    stream_handler = logging.StreamHandler(stream)
    format = Formatter()
    stream_handler.setFormatter(format)
    logger.addHandler(stream_handler)
    if log_file != '':
        iso_8601 = '%Y-%m-%dT%H:%M:%S'
        fmt      = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(fmt, iso_8601))
        logger.addHandler(file_handler)
    logger.setLevel(level)
    return logger
    
def getLogger(name=''):
    return Logger(logging.getLogger(name))