import enum
import time


class EventType(enum.Enum):
    ERROR = enum.auto(),
    INFO = enum.auto(),
    WARNING = enum.auto(),


class GlobalLogger:
    enabled = True

    @staticmethod
    def log(event_type: EventType, msg: str):
        if GlobalLogger.enabled:
            result_msg = '{0:10}:{1:15} {2}\n'.format(event_type, time.ctime(time.time()), msg)

            print(result_msg)

    @staticmethod
    def log_warning(msg):
        GlobalLogger.log(EventType.WARNING, msg)

    @staticmethod
    def log_error(msg):
        GlobalLogger.log(EventType.ERROR, msg)

    @staticmethod
    def log_info(msg):
        GlobalLogger.log(EventType.INFO, msg)
