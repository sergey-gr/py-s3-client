import yaml
import os
import sys
import logging
import logging.handlers
import datetime

from s3.client import S3Browser

# General
app_name = os.path.basename(__file__)
# Directories
app_dir = os.path.dirname(os.path.realpath(__file__))
app_config_dir = os.path.join(app_dir, 'config')
app_logging_dir = os.path.join(app_dir, 'logs')
# Files
app_config_file = os.path.join(app_config_dir, 'config.yml')
app_logging_file = os.path.join(app_logging_dir, f"{datetime.datetime.now().strftime('%Y-%m-%d')}.log")

# Read configuration from main.yml file
try:
    with open(app_config_file, mode='r') as f:
        config = yaml.safe_load(f.read())
except FileNotFoundError:
    print(f"{app_config_file} file not found!")
    sys.exit(1)

# Configure script logging
def log_setup():
    """ Function that sets up basic logging configuration """
    if config['logging']['output'] == 'file':
        # Check if logs dir does not exist
        if not os.path.exists(app_logging_dir):
            os.makedirs(app_logging_dir)
        handler = logging.handlers.WatchedFileHandler(app_logging_file)
    else:
        handler = logging.StreamHandler(sys.stdout)

    # Log format
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s {}[%(process)d]: %(message)s'.format(app_name),
        '%Y-%m-%d %H:%M:%S'
    )

    # Display log time in UTC format
    try:
        if config['logging']['utc_datetime']:
            import time
            formatter.converter = time.gmtime
    except KeyError:
        pass

    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(eval(f"logging.{config['logging']['level']}"))

# Init logging
log_setup()

def main():
    proxy = config['proxy']
    if proxy['enabled'] is True:
        logging.info(f"Proxy enabled, using proxy address: {proxy['address']}:{proxy['port']}")

    data = config['data']
    s3 = S3Browser(config['s3'], proxy)

    if s3.bucket_exists() is True:
        # s3.list_buckets()
        s3.list_objects()
        s3.fput_object(data['name'], f"{data['upload_dir']}/{data['file']}")
        s3.stat_object(data['name'])
        s3.fget_object(data['name'], f"{data['download_dir']}/downloaded_{data['file']}")
        s3.remove_object(data['name'])

if __name__ == '__main__':
    logging.info(f"Starting S3 Browser ...")
    main()
    logging.info(f"S3 Browser Done!")
