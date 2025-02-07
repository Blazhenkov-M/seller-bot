import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# Функция для получения логгера в любом файле
def get_logger(name: str):
    return logging.getLogger(name)
