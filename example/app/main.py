import logging
import os
import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import (
    QFileInfo,
    QMessageLogger,
    QUrl,
)

from controller import Controller


class QtHandler(logging.Handler):
    def emit(self, record):
        level = record.levelname.lower()
        record = self.format(record)

        if level == 'error':
            level = 'critical'

        qt_message_logger = QMessageLogger()
        getattr(qt_message_logger, level)(record.encode("utf-8"))


qtHandler = QtHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
qtHandler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(qtHandler)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    controller = Controller()

    engine.rootContext().setContextProperty("controller", controller)

    _root = QFileInfo(__file__).absolutePath()
    _root_url = 'qrc:' if _root.startswith(':') else _root
    logger.info('Root url is %s', str(_root_url))

    qml_path = QUrl(os.path.join(_root_url, 'qml/main.qml'))
    engine.load(qml_path)

    sys.exit(app.exec_())
