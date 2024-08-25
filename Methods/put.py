import os
import sys
import pathlib
import stat
import json
import secrets
from urllib.parse import urlparse
from datetime import datetime


from helper import *
import config as cfg

def do_put(parsed_req):
    req_info=parsed_req["req_info"]
    req_headers=parsed_req["req_headers"]
    file_uri=req_info["uri"]
    if Host_checking(parsed_req)==False:
        return request_with_error(parsed_req,'400')
    if Http_version_checking(parsed_req)==False:
        return request_with_error(parsed_req,'505')
    file_uri=file_uri.lstrip("/")
    file_uri='/'+file_uri
    file_uri=parse_geturl(file_uri)
    body=parsed_req["req_body"]
    status_code='200'
    if body=="":
        return request_with_error(parsed_req,'204')
    if 'content-md5' in req_headers:
        status_code=checksum_checking(body,req_headers['content-md5'],status_code)
        if status_code!='200':
            return request_with_error(parsed_req,status_code)
    if 'content-encoding' in req_headers:
        body=decompression_handler(body,req_headers['content-encoding'])
    if 'content-type' in req_headers:
        con_enc=req_headers['content-type']
        extention=content_type_from_extension(con_enc)
    else:
        return request_with_error(parsed_req,'400')#Bad Request
    root=cfg.DocumentRoot['root']
    root_dir=str(pathlib.Path().absolute())
    path=urlparse(file_uri).path
    path=path.lstrip("/")
    path='/'+path
    if os.path.isdir(root_dir+path):
        path=path+'/'+secrets.token_urlsafe(6)+"."+extention
    dir,file_name=os.path.split(root_dir+path)
    if extention==file_name.rsplit('.')[1]:
        pass
    else:
        return request_with_error(parsed_req,'415') # Unsupported media ; content type and body not matches
    #dir_path=dir
    #print("Dir-path",dir_path)
    #print(root_dir+file_uri)
    Explanation_body=""
    if os.path.exists(dir)==False:
        #print("New Folder Created")
        os.makedirs(dir)
    Etag=None
    try:
        if os.path.exists(root_dir+path):
            status_code='200'
            last_modified_timestamp=http_date_format(last_modified_time(root_dir+file_uri))
            Etag=Etag_generation(last_modified_timestamp)
            #print("Etag: ",Etag)
            if 'if-match' in req_headers:
                status_code=if_match_status(Etag,req_headers['if-match'].split(", "),status_code)
            else:
                status_code=if_match_status(Etag,["*"],status_code)
            if status_code!='200':
                return request_with_error(parsed_req,status_code)
            Explanation_body="Resource Modified."
        else:
            status_code='201'
            Explanation_body="Resource Created."
            #print("path:",dir+file_name)
        with open(dir+'/'+file_name,"wb") as file:
            #print("Writing")
            file.write(body)
            if Etag==None:
                last_modified_timestamp=http_date_format(last_modified_time(root_dir+file_uri))
                Etag=Etag_generation(last_modified_timestamp)
    except PermissionError:
        return request_with_error(parsed_req,'403')

    except:
        status_code='500'
        return request_with_error(parsed_req,'500')
    with open(root_dir+'/status_code/status-code.json') as js:
        status_code_msg=json.load(js)
    response_dict={'response-line':{'http-version':"HTTP/1.1",'statuscode':status_code,'status_code_msg':status_code_msg.get(status_code,"NOT FOUND Statuscode")},'responseHeaders':{"Connection":"close",'Date':http_date_format(datetime.utcnow()),'Server': "Shreeraj's Server","Content-length":str(len(Explanation_body)),"Set-Cookie":gen_cookie(),'Content-Language': 'en-US','ETag':Etag},'responseBody':Explanation_body.encode()}
    if Etag:
        response_dict['responseHeaders']['ETag']=Etag
    return response_dict
    
    
    
