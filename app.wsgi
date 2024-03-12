import sys 
import os
os.environ['APP_SETTINGS_MODULE'] =  'prodconfig'
sys.path.insert(0,"/home/clownstech.com/public_html/api-protein-folder/.venv/lib/python3.8/site-packages")
sys.path.insert(0, '/home/clownstech.com/public_html/api-protein-folder')
from app import app as application