from tornado.websocket import websocket_connect
from tornado.gen import coroutine, sleep
import logging
import logging.handlers
import json
from tornado.ioloop import IOLoop

__author__ = "Ennis"
SERVER_URL = "wss://m2m.vaillant.com.cn:8880/ws/dev/v1"


def init_logging():
    """
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    sh = logging.StreamHandler()
    file_log = logging.handlers.TimedRotatingFileHandler('scooter_notify.log', 'MIDNIGHT', 1, 0)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)-7s] [%(module)s:%(filename)s-%(funcName)s-%(lineno)d] %(message)s')
    sh.setFormatter(formatter)
    file_log.setFormatter(formatter)


    logger.addHandler(sh)
    logger.addHandler(file_log)


    logging.info("Current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))


class Communicator:
    """
    """
    close_door_timer = None


    def __init__(self):
        self._websocket_client = None


    @coroutine
    def on_recv_msg(self, message):
        try:
            if message is None:
                logging.info("web socket connection have disconnect, reconnect")
                yield self.on_websocket_close()
                return


            logging.info("receive message = %s", message)


        except Exception as err_info:
            logging.error("handle websocket message failed:%s", err_info)


    @coroutine
    def on_websocket_close(self):
        while True:
            try:
                self._websocket_client = None
                yield sleep(1)
                self._websocket_client = yield websocket_connect(SERVER_URL, on_message_callback=self.on_recv_msg)
                break


            except Exception as err_info:
                print(err_info)
                continue
        logging.info("connect server success:%s", SERVER_URL)


    @coroutine
    def start(self):
        """


        :return:
        """
        try:
            websocket_connect(SERVER_URL, on_message_callback=self.on_recv_msg)
            self._websocket_client = yield websocket_connect(SERVER_URL, on_message_callback=self.on_recv_msg)
            logging.info("connect server success:%s", SERVER_URL)


        except Exception as err_info:
            logging.error("start device controller failed: %s", err_info)
            yield self.on_recv_msg(None)


    @coroutine
    def send_data(self, data):
        try:
            logging.info("will post device central :%s", data)
            if self._websocket_client is None:
                return False


            self._websocket_client.write_message(data)
            return True


        except Exception as err_info:
            logging.error("send dat to service failed: %s", err_info)
            return False