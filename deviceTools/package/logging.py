import logging

def log(logname):
    # 创建一个logger  
    logger = logging.getLogger('mylogger')  
    logger.setLevel(logging.DEBUG)  
  
    # 创建一个handler，用于写入日志文件  
    fh = logging.FileHandler(logname)  
    fh.setLevel(logging.DEBUG)  
    # 定义handler的输出格式  
    formatter = logging.Formatter('%(asctime)s:%(filename)s:%(threadName)s:[line:%(lineno)d] %(levelname)s %(message)s')  
    fh.setFormatter(formatter)  
  
    # 给logger添加handler  
    logger.addHandler(fh)  
    return(logger)
