
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from random import uniform
import time
import json
# import undetected_chromedriver as uc

import json
import random
import os
import pandas as pd
from urllib.parse import urlparse, parse_qs
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# import openpyxl
import requests
from concurrent.futures import ThreadPoolExecutor, wait
import re
from selenium import webdriver
import datetime
import csv