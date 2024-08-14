import os
import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer


import sqlite3 ## pip install db-sqlite3
import mysql.connector # pip install --upgrade mysql-connector-python


DEFAULT_SERVER_IP = '0.0.0.0'
DEFAULT_SERVER_PORT = 12345


DEFAULT_MYSQL_SERVER_IP = '127.0.0.1'
DEFAULT_MYSQL_SEVER_PORT = '3306'
DEFAULT_MYSQL_SERVER_USER = 'root'
DEFAULT_MYSQL_SERVER_PASSWORD = 'changeme'  ## NOTE: This is bad practice. Never put passwords in code.  
DEFAULT_MYSQL_SERVER_SCHEMA = 'myapp1'


DEFAULT_SQLITE3_DB_FILE = os.path.join(os.path.expanduser('~'), 'myapp1.db')


def sqlite3_ncpDataTypes_byId(id):
    joData = {
            'id': id,
            'damageType': None,
           
            'requestPath': None,
            'statusCode': None,
            'statusText': None,
            'errors': None,
            }
    dbConn = None
    cur = None
    try:
        ## Connect to the database
        dbConn = sqlite3.connect(DEFAULT_SQLITE3_DB_FILE)
        ## Get cursor and run sql
        sql = 'SELECT * FROM npcDamageTypes WHERE id=%s;' % id
        cur = dbConn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        if len(results) != 1:
           joData['errors'] = '[ERROR] Failed to fetch data -- %s' % sql
        else:
            joData['damageType'] = results[0][1]            
    except Exception as e:
        if joData.get('errors') == None:
            joData['errors'] = '[ERROR] %s' % e
        else:
            joData['errors'] += '\n[ERROR] %s' % e
    finally:
        if cur != None:
            cur.close()
        if dbConn != None:
            dbConn.close()
    return joData






def mysql_users_byId(id,
                     dbUser=DEFAULT_MYSQL_SERVER_USER,
                     dbPassword=DEFAULT_MYSQL_SERVER_PASSWORD,
                     dbIp=DEFAULT_MYSQL_SERVER_IP,
                     dbPort=DEFAULT_MYSQL_SEVER_PORT,
                     dbSchema=DEFAULT_MYSQL_SERVER_SCHEMA
                     ):
    joData = {
            'id': id,
            'name': None,
            'age': None,
           
            'requestPath': None,
            'statusCode': None,
            'statusText': None,
            'errors': None,
            }
    dbConn = None
    cur = None
    try:
        dbConn = mysql.connector.connect(
                host=dbIp,
                port=dbPort,
                user=dbUser,
                password=dbPassword,
                database=dbSchema,
                )
       
        ## Get cursor and run sql


        ## @TODO - fix this so that it uses the correct SQL
        sql = 'SELECT * FROM tableDoesNotExist WHERE id=%s;' % id


        cur = dbConn.cursor()
        cur.execute(sql)  
        results = cur.fetchall()
        if len(results) != 1:
            joData['errors'] = '[ERROR] Failed to fetch data -- %s' % sql
        else:
            joData['name'] = results[0][1]
            joData['age'] = results[0][2]  
    except Exception as e:
        if joData.get('errors') == None:
            joData['errors'] = '[ERROR] %s' % e
        else:
            joData['errors'] += '\n[ERROR] %s' % e
    finally:
        if cur != None:
            cur.close()
        if dbConn != None:
            dbConn.close()
    return joData




class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info('path:  %s' % self.path)
        if self.path.lower().startswith('/api/users'):  ## mysql.myapp1.users
            id = self.path.split('/')[-1]
           
            joData = mysql_users_byId(id)
            joData['requestPath'] = self.path
            if joData.get('errors') == None:                
                logging.info('GET %s 200', self.path)
                joData['statusCode'] = 200
                joData['statusText'] = 'OK'
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                #sData = json.dumps(joData, indent=4, sort_keys=True).encode('utf-8')
                sData = json.dumps(joData, indent=4).encode('utf-8')
                self.wfile.write(sData)
            else:
                logging.info('GET %s 404', self.path)
                logging.info('%s' % joData.get('errors'))
                joData['statusCode'] = 404
                joData['statusText'] = 'Not Found'
                self.send_response(404, joData['statusText'])
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                sData = json.dumps(joData, indent=4).encode('utf-8')
                self.wfile.write(sData)
           
        elif self.path.lower().startswith('/api/npc/damage_types'):  ## sqlite3.myapp1.npcDamageTypes
            id = self.path.split('/')[-1]
            ## Retrieve data from DB            
            joData = sqlite3_ncpDataTypes_byId(id)
            joData['requestPath'] = self.path
            if joData.get('errors') == None:                
                logging.info('GET %s 200', self.path)
                joData['statusCode'] = 200
                joData['statusText'] = 'OK'
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                #sData = json.dumps(joData, indent=4, sort_keys=True).encode('utf-8')
                sData = json.dumps(joData, indent=4).encode('utf-8')
                self.wfile.write(sData)
            else:
                logging.info('GET %s 404', self.path)
                logging.info('%s' % joData.get('errors'))
                joData['statusCode'] = 404
                joData['statusText'] = 'Not Found'
                self.send_response(404, joData['statusText'])
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                sData = json.dumps(joData, indent=4).encode('utf-8')
                self.wfile.write(sData)


        elif self.path.lower().startswith('/api/npc/actions'):  ## sqlite3.myapp1.npcActions
            id = self.path.split('/')[-1]


            ## @TODO - Add the correct code and remove default error
            self.send_response(404, 'Not Found')      


        else:
            self.send_response(403)
        self.end_headers()


       
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting httpd:  %s:%s\n' % (DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT))
    server = HTTPServer((DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT), HTTPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    logging.info('Stopping httpd...\n')