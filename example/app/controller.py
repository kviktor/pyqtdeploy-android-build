import logging
import sys
import sysconfig

from PyQt5.QtCore import (
    pyqtProperty,
    pyqtSignal,
    pyqtSlot,
    QJsonDocument,
    QObject,
    QOperatingSystemVersion,
    QSysInfo,
    PYQT_VERSION_STR,
    QT_VERSION_STR,
)
from sip import SIP_VERSION_STR


logger = logging.getLogger(__name__)


class Controller(QObject):
    """ this is not really a controller but a God object for sake of testing """
    click_signal = pyqtSignal()
    _signal = pyqtSignal()
    _click_count = 0

    @pyqtProperty(int, notify=click_signal)
    def click_count(self):
        return self._click_count

    @pyqtSlot()
    def click_event(self):
        logger.info('Clicked')

        self._click_count += 1
        self.click_signal.emit()

    @pyqtSlot(str)
    def send_notification(self, text):
        _klass = 'org/kviktor/example/ExampleActivity'

        try:
            from PyQt5.QtAndroidExtras import QAndroidJniObject
            logger.info('QtAndroidExtras/QAndroidJniObject import successful')

            logger.info(
                f'QAndroidJniObject.isClassAvailable({_klass}): '
                f'{QAndroidJniObject.isClassAvailable(_klass)}')

            json_doc = QJsonDocument({
                'text': text,
                'title': 'sent from Python',
            })
            retval = QAndroidJniObject.callStaticMethod(_klass, 'sendNotification', json_doc)
            logger.info('sendNotification call done, retval: %s', retval.object())
        except ImportError:
            logger.exception('Could not import QtAndroidExtras')

    @pyqtProperty(str, constant=True)
    def system_info(self):
        sys_info = QSysInfo()
        fields = [
            'buildAbi',
            'buildCpuArchitecture',
            'currentCpuArchitecture',
            'kernelType',
            'kernelVersion',
            'machineHostName',
            'prettyProductName',
            'productType',
            'productVersion',
        ]

        info = [f'{field}: {getattr(sys_info, field)()}' for field in fields]
        info.append(f'QOS name: {QOperatingSystemVersion.current().name()}')
        info.append(f'sysconfig.get_platform(): {sysconfig.get_platform()}')
        info.append(f'QT: {QT_VERSION_STR}')
        info.append(f'PyQt version: {PYQT_VERSION_STR}')
        info.append(f'sip version: {SIP_VERSION_STR}')
        info.append(f'sys.platform: {sys.platform}')
        info.append(f'Python version: {sys.version}')

        return '\n'.join(info)
