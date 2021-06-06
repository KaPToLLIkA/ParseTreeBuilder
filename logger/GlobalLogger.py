import enum
import time


class EventType(enum.Enum):
    ERROR = enum.auto(),
    INFO = enum.auto(),
    WARNING = enum.auto(),


class GlobalLogger:
    enabled = True
    console_log_enabled = True

    @staticmethod
    def on():
        GlobalLogger.enabled = True

    @staticmethod
    def off():
        GlobalLogger.enabled = False

    @staticmethod
    def log(event_type: EventType, msg: str):
        if GlobalLogger.enabled:
            time_str = time.strftime('%H:%M:%S', time.localtime())
            max_time_str_len = len(time_str)
            max_event_type_str_len = 0
            for name, member in EventType.__members__.items():
                max_event_type_str_len = max(max_event_type_str_len, len(name))

            pre_result_msg = '{0:%d} ## {1:%d} ## {2}' % (max_event_type_str_len, max_time_str_len)
            result_msg = pre_result_msg.format(event_type.name, time_str, msg)

            if GlobalLogger.console_log_enabled:
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
