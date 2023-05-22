import os
import getpass
import shutil
import csv
import logging
import subprocess
import glob
import re
import pyewf
import pytsk3
import sys
import json
import plistlib
import sqlite3
import datetime
import Modules.Basic.basic_functions as bf
import xml.etree.ElementTree as ET

from tqdm import tqdm
from pyfiglet import Figlet
from termcolor import colored
from io import BytesIO