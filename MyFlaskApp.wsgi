#!/usr/bin/python
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/Users/sudhanshumishra/Desktop/tf_exercise/MyFlaskApp")

from flask_app import app as application