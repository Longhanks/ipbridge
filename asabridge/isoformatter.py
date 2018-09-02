# -*- coding: utf-8 -*-
from logging import Formatter
import time


class IsoFormatter(Formatter):
    def formatTime(self, record, datefmt=None):
        timestamp = time.localtime(record.created)
        msec_s = '%03d' % record.msecs
        raw_timezone_s = time.strftime('%z', timestamp)
        timezone_s = raw_timezone_s[:3] + ':' + raw_timezone_s[3:]
        return time.strftime(f'%Y-%m-%dT%H:%M:%S.{msec_s}{timezone_s}', timestamp)
