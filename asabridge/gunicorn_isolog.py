# -*- coding: utf-8 -*-
from gunicorn.glogging import Logger
from asabridge.isoformatter import IsoFormatter
from asabridge.app import ERROR_FMT


class IsoLogger(Logger):
    def setup(self, cfg):
        super().setup(cfg)
        self._set_handler(self.error_log, cfg.errorlog, IsoFormatter(ERROR_FMT))
