import logging
import json
logging.basicConfig(level=logging.INFO, format="%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


class Logger:
    def __init__(self, request_id):
        super().__init__()
        self.id = request_id
        self.module = None
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def format(self, message):
        message = json.dumps(message)
        return f"{self.id}:{message}"

    def info(self, message):
        self.logger.info(self.format(message))
    
    def error(self, message):
        self.logger.error(self.format(message))

    def debug(self, message):
        self.logger.debug(self.format(message))

    def warning(self, message):
        self.logger.warning(self.format(message))

    def critical(self, message):
        self.logger.critical(self.format(message))
