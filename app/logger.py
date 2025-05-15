import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name='app'):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # 先にレベル設定
    if not logger.handlers:
        # ファイルに出すハンドラ
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, f"{name}.log"), maxBytes=1_000_000, backupCount=3
        )
        file_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
        ))
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        # コンソールにも出すハンドラ
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
        ))
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

    return logger
