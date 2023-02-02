import threading

import psycopg2
import skimage.io
import skimage
from flask import Flask, request, render_template
from werkzeug.datastructures import ImmutableMultiDict
import random
from PIL import Image
import numpy as np
from numpy import load, save, dot
from numpy.linalg import norm
import yaml
import logging
import logging.handlers
from colorlog import ColoredFormatter
import datetime
import base64
import cv2
from multiprocessing.dummy import Pool
from pathlib import Path
import uuid
import os
import json
import traceback
import string
import time
import json
import sys
import requests
from utils import model
import boto3
from sqlalchemy import create_engine
from awscli.errorhandler import ClientError

global shared_data
global lock_shared_data
global data_folder

script_path = os.path.dirname(os.path.realpath(__file__))
# os.makedirs('volatile_logs', exist_ok=True) # For linux, map a folder to /tmpfs (memory) to reduce harddisk overhead
os.makedirs('logs', exist_ok=True)

LOG_LEVEL = logging.INFO
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT = "%(asctime)s.%(msecs)03d - %(levelname)s - %(name)s - %(message)s"
LOG_FORMAT_COLORED = "%(log_color)s%(asctime)s.%(msecs)03d - %(levelname)s - %(name)s - %(message)s%(reset)s"

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(LOG_LEVEL)
stream_handler.setFormatter(formatter)

with open(os.path.join(script_path, configFilePath)) as f:
	config = yaml.safe_load(f)

reid_model_path = config['reid']['model_path']
reid_config_path = config['reid']['config_path']
resnet50_model_dir = config['reid']['resnet50_model_dir']
resnet50_model_file_name = config['reid']['resnet50_model_file_name']

app = Flask(__name__, template_folder='webpage', static_folder='webpage', static_url_path='')

# for monitoring metrics
@app.route('/api/metrics', methods=['GET'])
def api_metrics():
	global shared_data

	try:
		if_success = True
		json_str = {
			"system_datetime": get_system_datetime(),
			"size_matching_queue": len(matching_queue),
			"size_image_queue": len(image_queue),
			"if_success": if_success,
			}
		json_str = json.dumps(json_str, indent=4, default=str)
		return json_str
	except:
		logger.error(str(traceback.format_exc()))
		if_success = False
		json_str = {
			"system_datetime": get_system_datetime(),
			"if_success": if_success,
			"detail": str(traceback.format_exc()),
			}
		json_str = json.dumps(json_str, indent=4, default=str)
		return json_str

# for checking if the endpoint is workable
@app.route('/health_check', methods=['GET'])
def health_check():
	return





