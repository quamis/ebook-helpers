import os, sys
import logging
import argparse

# handle args
parser = argparse.ArgumentParser(description='Convert any file to epub file')
parser.add_argument('--input',  '-i',  dest='input',   action='store', type=str, default=None,  help='TODO')
parser.add_argument('--output', '-o',  dest='output',  action='store', type=str, default=None,  help='TODO')
parser.add_argument('--fromformat', dest='fromformat',   action='store', type=str, default=None,    help='TODO')
parser.add_argument('--toformat',   dest='toformat',     action='store', type=str, default="epub",  help='TODO')
args = vars(parser.parse_args())

if args['input'] is None:
    parser.error('No input file specified, add --input=/path/to/file')
    
if args['output'] is None:
    args['output'] = "%s.%s" % (os.path.splitext(os.path.basename(args['input']))[0], args['toformat'])

logging.basicConfig(level=logging.INFO)

# load the cloudconvert library
logging.info('Import python-cloudconvert') 
lib_path = os.path.abspath('python-cloudconvert')
sys.path.append(lib_path)
import CloudConvert

apikey = os.environ['CLOUDCONVERT_API_KEY']         # api-key from cloudconvert
process = CloudConvert.ConversionProcess(apikey)

# This should autodetect file extension
logging.info('Initialize convertor')
process.init(args['input'], os.path.basename(args['output']), fromformat = args['fromformat'], toformat = args['toformat'])

# This step uploads the file and starts the conversion
logging.info('Start convertor')
process.start()

# Will block until file is done processing. You can set
# the interval between checks.
logging.info('Wait for convertor to finish')
process.wait_for_completion(check_interval=1)

logging.info('Write data to %s' % args['output'])
# Returns a file-like obj to download the processed file
download = process.download()
if args['output']=="-":
    print download.read()
else:
    with open(args['output'], "wb") as f:  # Important to set mode to wb
        f.write(download.read())
