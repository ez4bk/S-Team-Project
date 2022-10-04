import logging.handlers

log_file = 'test.mylog'

time_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=0)
time_handler.suffix = '%Y-%m-%d.mylog'
time_handler.setLevel('ERROR')  # error以上的内容输出到文件里面

fmt = '%(asctime)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)
time_handler.setFormatter(formatter)

logger = logging.getLogger('updateSecurity')
logger.setLevel('INFO')
logger.addHandler(time_handler)

logger.info("bbbbbb")
# logging.debug("aaaaaa")