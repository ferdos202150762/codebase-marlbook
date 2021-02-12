import json
import logging
from hashlib import sha256
from typing import Dict

import wandb
from hydra.conf import HydraConf
from omegaconf import DictConfig, OmegaConf

logging.basicConfig(
    level=logging.INFO,
    format="(%(process)d) [%(levelname).1s] - (%(asctime)s) - %(name)s >> %(message)s",
    datefmt="%m/%d %H:%M:%S",
)


class Logger:
    def __init__(self, project_name, cfg: DictConfig) -> None:
        config_hash = sha256(
            json.dumps(
                {k: v for k, v in OmegaConf.to_container(cfg).items() if k != "seed"},
                sort_keys=True,
            ).encode("utf8")
        ).hexdigest()[-10:]
        self._run = wandb.init(
            project=project_name, config=OmegaConf.to_container(cfg), monitor_gym=True, group=config_hash
        )

    def log_metrics(self, d: Dict):
        self._run.log(d)

    def watch(self, model):
        self._run.watch(model)

    def debug(self, *args, **kwargs):
        return logging.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        return logging.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return logging.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        return logging.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        return logging.critical(*args, **kwargs)