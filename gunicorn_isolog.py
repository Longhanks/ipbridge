# -*- coding: utf-8 -*-
from gunicorn.glogging import Logger
from asabridge.isoformatter import IsoFormatter


class IsoLogger(Logger):
    def setup(self, cfg):
        super().setup(cfg)
        self._set_handler(self.error_log, cfg.errorlog, IsoFormatter(self.error_fmt))
