import os
import json
import base64
import config as cfg
import pathlib
import shutil
from datetime import datetime
from urllib.parse import urlparse

from helper import *
import config as cfg
def do_delete(parsed_req):
    req_info=parsed_req["req_info"]
    req_headers=parsed_req["req_headers"]
    file_uri=req_info["uri"]
    if Host_checking(parsed_req)==False:
        return request_with_error(parsed_req,'400')
    if Http_version_checking(parsed_req)==False:
        return request_with_error(parsed_req,'505')
    root=cfg.DocumentRoot['root']
    root_dir=str(pathlib.Path().absolute())
    acess_auth=cfg.Autherization
    if 'authorization' in req_headers:
        type,credential=req_headers['authorization'].split()
        if type!=acess_auth['type']:
            #print("Type Not matched")
            return request_with_error(parsed_req,'401')
        else:
            username,password=base64.b64decode(credential.encode('ascii')).decode('ascii').split(":")
            #print(username,":",password)
    else:
        return request_with_error(parsed_req,'401')
    path=urlparse(file_uri).path
    #print("After urlparsing:",path)
    path=path.lstrip('/')
    path= "/"+path
    index_file_flag=0
    if path=="/":
        if os.path.exists(root+path+'index.html'):
            path+='index.html'
        else:
            return request_with_error(parsed_req,'404')
    path=parse_geturl(path)
    path=root+path
    status_code='200'
    #print(path)
    #print(path)
    if 'index.html' in path:
        if not (username==acess_auth['username'] and password==acess_auth['password']):
            return request_with_error(parsed_req,'401')
        else:
            if os.path.exists(path):
                last_modified_timestamp=http_date_format(last_modified_time(path))
                Etag=Etag_generation(last_modified_timestamp)
                #print("Etag: ",Etag)
                if 'if-match' in req_headers:
                    status_code=if_match_status(Etag,req_headers['if-match'].split(", "),status_code)
                else:
                    status_code=if_match_status(Etag,["*"],status_code)
                if status_code!='200':
                    return request_with_error(parsed_req,status_code)
                if 'if-unmodified-since' in req_headers:
                    if_unmod=req_headers['if-unmodified-since']
                else:
                    if_unmod=http_date_format(datetime.utcnow())
                status_code=if_unmodified_check(if_unmod,last_modified_timestamp,status_code)
                #print(status_code)
                if status_code=='412':
                    return request_with_error(parsed_req,'412')
                try:
                    shutil.move(path,cfg.Delete_Root)
                    #print("Deleted by shutil")
                except shutil.Error:
                    os.remove(path)
                    #print("Removed By Os")
                #print("Index File Deleted")
                index_file_flag=1
                #print("Flag=",index_file_flag)
                status_code='200'
                with open(root_dir+'/status_code/status-code.json') as js:
                    status_code_msg=json.load(js)
                response_body="Resource Deleted"
                response_dict={'response-line':{'http-version':"HTTP/1.1",'statuscode':status_code,'status_code_msg':status_code_msg.get(status_code,"NOT FOUND Statuscode")},'responseHeaders':{"Connection":"close",'Date':http_date_format(datetime.utcnow()),'Server': "Shreeraj's Server","Content-length":str(len(response_body))},'responseBody':response_body.encode()}
                return response_dict
            else:
                #print("Index not present")
                return request_with_error(parsed_req,'404')
    if index_file_flag==0 and os.path.exists(path):
        if os.path.isfile(path):
            try:
                last_modified_timestamp=http_date_format(last_modified_time(path))
                Etag=Etag_generation(last_modified_timestamp)
                #print("Etag: ",Etag)
                if 'if-match' in req_headers:
                    status_code=if_match_status(Etag,req_headers['if-match'].split(", "),status_code)
                else:
                    status_code=if_match_status(Etag,["*"],status_code)
                if status_code!='200':
                    return request_with_error(parsed_req,status_code)
                if 'if-unmodified-since' in req_headers:
                    if_unmod=req_headers['if-unmodified-since']
                else:
                    if_unmod=http_date_format(datetime.utcnow())
                status_code=if_unmodified_check(if_unmod,last_modified_timestamp,status_code)
                if status_code=='412':
                    return request_with_error(parsed_req,'412')
                try:
                    shutil.move(path,cfg.Delete_Root)
                    #print("Deleted by shutil")
                except shutil.Error:
                    os.remove(path)
                    #print("Removed By Os")
            except PermissionError:
                return request_with_error(parsed_req,'403')
            except:
                status_code='500'
                return request_with_error(parsed_req,'500')
    else:
        #print("In else")
        status_code='404'
        return request_with_error(parsed_req,'404')
    with open(root_dir+'/status_code/status-code.json') as js:
        status_code_msg=json.load(js)
    response_body="Resource Deleted"
    response_dict={'response-line':{'http-version':"HTTP/1.1",'statuscode':status_code,'status_code_msg':status_code_msg.get(status_code,"NOT FOUND Statuscode")},'responseHeaders':{"Connection":"close",'Date':http_date_format(datetime.utcnow()),'Server': "Shreeraj's Server","Content-length":str(len(response_body)),"Set-Cookie":gen_cookie(),'Content-Language': 'en-US','ETag':Etag},'responseBody':response_body.encode()}
    return response_dict
