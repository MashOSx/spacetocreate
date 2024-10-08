import json
import logging
from  http.server import BaseHTTPRequestHandler, HTTPServer

DEFAULT_FILE_CONFIG = "./ws_config.json"
DEFAULT_DIR_DATA_HTTPD = "./data/httpd"

def config_loadFromJson(fn=DEFAULT_FILE_CONFIG):
    jo = None
    with open(fn, 'r') as fConfig:
        jo = json.load(fConfig)
    return jo

def textFile_load(fn, baseDir=DEFAULT_DIR_DATA_HTTPD):
    sLines = None
    ## If this causes an error, try this instead: 
    #fnPath = ‘%s%s’ % (baseDir, fn)  ## Joins 2x strings without forward slash (i.e. filepath separator for linux) 
    fnPath = '%s/%s' % (baseDir, fn) ## Joins 2x strings including forward slash (i.e. filepath separator for linux) 
    try:
        with open(fnPath, 'r') as F:
            sLines = F.readlines()
    except Exception as e:
        logging.error('Failed to load file:  %s\n\t%s' % (fnPath, e))
    return sLines

def iconFile_load(fn, baseDir=DEFAULT_DIR_DATA_HTTPD):
    b = None
    fnPath = '%s/%s' % (baseDir, fn)
    try:
        with open(fnPath, 'rb') as F:
            b = F.read()
    except Exception as e:
        logging.error('Failed to load file:  %s\n\t%s' % (fnPath, e))
    return b

class httpdHandler(BaseHTTPRequestHandler):
    def do_ERR(self, errorMsg, errCode=404):
        self.send_response(errCode)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(errorMsg.encode('utf-8'))
       
    def do_GET(self):
        sRequestedFile = self.path
        if self.path == '/':  ## Get the root page (index.html)
            sRequestedFile = '/index.html'
        if sRequestedFile.endswith('.htm') or sRequestedFile.endswith('.html'):  ## Return html file
            sLines = textFile_load(sRequestedFile)
            if sLines != None:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(''.join(sLines).encode('utf-8'))
            else:
                self.do_ERR('[ERROR] 404 - Not Found (%s)' % sRequestedFile, 404)
        elif sRequestedFile.endswith('.css'): ## Return css file (content-type=’text/css’)
            sLines = textFile_load(sRequestedFile)
            if sLines != None:
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(''.join(sLines).encode('utf-8'))
        elif sRequestedFile.endswith('.js'): ## Return javascript file (content-type=’text/javascript’)
            sLines = textFile_load(sRequestedFile)
            if sLines != None:
                self.send_response(200)
                self.send_header('Content-type', 'text/javascript')
                self.end_headers()
                self.wfile.write(''.join(sLines).encode('utf-8'))
        elif sRequestedFile.endswith('.json'): ## Return json file (content-type=’application/json’ 
            sLines = textFile_load(sRequestedFile)
            if sLines != None:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(''.join(sLines).encode('utf-8'))
        elif sRequestedFile.endswith('.ico'): ## Return an icon (content-type=’image/png’)
            sLines = iconFile_load(sRequestedFile)
            if sLines != None:
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(sLines)
        else:
            self.do_ERR('[ERROR] 404 - Not Found (%s).' % sRequestedFile, 404)

def httpd_start(serverIp='0.0.0.0', serverPort=8080):
    #global DEFAULT_DIR_DATA_HTTPD //NOT A PART OF THE LOCAL FILE SYSTEM
    #DEFAULT_DIR_DATA_HTTPD = joConfig['dirDataHttpd']
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting httpd (%s:%s)...\n' % (serverIp, serverPort))
    serverIpAndPort = (serverIp, serverPort)
    httpd = HTTPServer(serverIpAndPort, httpdHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:  ## CTRL+C will interrupt the app (or CTRL+Pause for MS Windows)
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    joConfig = config_loadFromJson()
    httpd_start(joConfig['serverIp'], int(joConfig['serverPort']))