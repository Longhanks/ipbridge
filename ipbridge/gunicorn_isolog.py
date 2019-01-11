# -*- coding: utf-8 -*-
from gunicorn.glogging import Logger
from ipbridge.isoformatter import IsoFormatter
from ipbridge.config import ProductionConfig


class IsoLogger(Logger):
    def setup(self, cfg):
        super().setup(cfg)
        self._set_handler(
            self.error_log,
            cfg.errorlog,
            IsoFormatter(ProductionConfig.ERROR_FMT),
        )
