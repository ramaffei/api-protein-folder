from os.path import abspath, dirname

# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))
PROPAGATE_EXCEPTIONS = True
ERROR_404_HELP = False
DEBUG = True
UPLOAD_FOLDER = '/upload'