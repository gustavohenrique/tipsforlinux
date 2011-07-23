# -*- coding:utf-8 -*-
import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

from settings import *

MAIN_TEMPLATE_DIR=os.path.join(PROJECT_ROOT_PATH, 'templates')
WEB_TEMPLATE_DIR=os.path.join(MAIN_TEMPLATE_DIR, 'mobile')
TEMPLATE_DIRS = (
    WEB_TEMPLATE_DIR,
    os.path.join(WEB_TEMPLATE_DIR, 'tips')
)

