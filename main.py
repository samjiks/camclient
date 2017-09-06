import socket
import sys
import os
import urllib3
from urllib3 import exceptions
import yaml
import logging

# s = socket.socket()
# s.connect(("localhost", 10000))

#Get the Current Path Directory
get_curr_path = os.path.dirname(os.path.abspath(__file__))

get_folder_path = get_curr_path + "/images"


logger = logging.getLogger(__name__)

def logger_settings():
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

logger_settings()

#create directory
def create_path():
    """
    Create Path to store the images to a folder retrieve
    :return:
    """
    logger.info('CREATE PATH FUNCTION')
    try:
        if not os.path.exists(get_folder_path):
             os.makedirs(get_folder_path)
             return get_folder_path
    except OSError as error:
        print(error)

def capture_image_and_save_file_to_disk():
    from datetime import datetime
    time = datetime.now().strftime('%Y%m%d%H%M%S')
    import picamera
    camera = picamera.PiCamera()
    path = create_path()
    file = time + '.jpg'
    os.chdir(get_folder_path)
    camera.capture(file)
    return file


def authenticate(url,username, password):
    logger.debug("Inside Authentication Function")
    try:
        http = urllib3.PoolManager()
        headers = urllib3.util.make_headers(basic_auth=username + ":" + password)
        request = http.request('GET',url, headers=headers)
    except exceptions.ConnectTimeoutError as e:
        print(e.with_traceback())
        logging.error("Connection Could not be established, Please check your internet connection and try again!")
    except Exception as e:
        print(e.with_traceback())

    if request.status == 200:
        return True
    else:
        return False;

def read_config():
    try:
        with open('config.yaml', 'r') as f:
            doc = yaml.load(f)
            return doc['url'], doc['username'], doc['password'], doc['aws_access_key_id'], doc['aws_secret_access_key']
    except IOError:
        print("File does not exist")
        return 0

def get_schedule_time():
    pass

def check_for_updates():
    pass

def upload_to_s3(accesskey,accessecretkey, file):
    try:
        from boto.s3.connection import S3Connection
        from boto.s3.key import Key
        import boto
        conn = boto.connect_s3(accesskey, accessecretkey)
        bucket_image = "camarcus"
        bucket = conn.get_bucket(bucket_image, validate=False)
        bucket_location = bucket.get_location()
        print(bucket_location)
        k = Key(bucket)
        k.key = file
        logger.debug(get_folder_path)
        full_key_name = os.path.join(get_folder_path, file)
        logger.debug(full_key_name)
        k = bucket.new_key(full_key_name)
        k.set_contents_from_filename(full_key_name)
    except Exception as e:
        logger.debug(e)


check = create_path()
url, username, password, accesskey, accessecretkey = read_config()
logger.debug('Authenticating Process Initiated....')
if authenticate(url, username, password) == True:
    logger.debug("Authentication Successful")
    get_file = capture_image_and_save_file_to_disk()
    upload_to_s3(accesskey,accessecretkey, get_file)
    #Need to retrieve session and schedule time every 1 day
else:
    print("Authentication not Successful")

