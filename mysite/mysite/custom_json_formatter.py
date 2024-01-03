from django.utils.datetime_safe import datetime
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """ часть настройки логгирования """
    def add_fields(self, log_record, record, message_dict):
        """ стандартная функция описание форматтера """
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().strftime('%d-%m-%Y|%H:%M:%S|%fZ')

        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

        log_record['module'] = record.module
        log_record['message'] = log_record.pop('message', None)
