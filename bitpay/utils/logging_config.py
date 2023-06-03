import logging
from bitpay.services.config_manager import ConfigManager


def setup_logger():
    """
    Setup the logger
    :return:
    """
    config = ConfigManager()
    log_file = config.read_config("LOGGING", "log_file")

    logging.basicConfig(filename=log_file,
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

