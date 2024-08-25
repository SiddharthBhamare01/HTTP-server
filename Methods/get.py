from genericpath import isfile
import pathlib
from datetime import datetime
import os
import json
import sys
from urllib.parse import urlparse
sys.path.append(os.path.abspath(os.path.join('/media_types')))

from media_types.content_type import content_type_decision
from helper import *
import config as cfg
def do_get(parsed_req):
    req_info=parsed_req["req_info"]
    req_headers=parsed_req["req_headers"]
    file_uri=req_info["uri"]
    if Host_checking(parsed_req)==False:
        return request_with_error(parsed_req,'400')
    if Http_version_checking(parsed_req)==False:
        return request_with_error(parsed_req,'505')
    file_uri=parse_geturl(file_uri)
    root=cfg.DocumentRoot['root']
    root_dir=str(pathlib.Path().absolute())
    status_code='200'
    #file_uri=file_uri.lstrip('/')
    path=urlparse(file_uri).path
    #print("After urlparsing:",path)
    path=path.lstrip('/')
    path= "/"+path
    if path=="/":
        path="/index.html"
    path=root+path
    if not os.path.isfile(path):
        return request_with_error(parsed_req,'404')
    extension=path.rstrip(pathlib.Path(path).suffix)
    if 'accept-encoding' in req_headers:
        content_enc=decide_encoding(req_headers['accept-encoding'])
        if content_enc==None:
            return request_with_error(parsed_req,'406')
    else:
        content_enc='identity'
    if 'accept' in req_headers:
        if '*/*' in req_headers['accept']:
            extension=both_star_accept(path)
        else:
            extension=check_file(path,req_headers['accept'])
    if extension==-1:
        return request_with_error(parsed_req,'415')
    if extension==None:
        return request_with_error(parsed_req,'404')
    if extension!=path.rstrip(pathlib.Path(path).suffix):
        path=path.rsplit(pathlib.Path(path).suffix)[0]+extension
    #path=parse_geturl(path)
    #print(path)
    #print("path:",path)
    if os.path.isfile(path):
        last_modified_timestamp=http_date_format(last_modified_time(path))
    else:
        status_code='404'
    if status_code!='404':
        Etag=Etag_generation(last_modified_timestamp,content_enc)
        #print("Etag: ",Etag)
        if 'if-match' in req_headers:
            status_code=if_match_status(Etag,req_headers['if-match'].split(", "),status_code)
        else:
            status_code=if_match_status(Etag,["*"],status_code)
        if status_code!='200':
            return request_with_error(parsed_req,status_code)
        if 'if-none-match' in req_headers:
            status_code=if_none_match_status(Etag,req_headers['if-none-match'].split(", "),status_code)
        else:
            status_code=if_none_match_status(Etag,[],status_code)
        if status_code!='200':
            return request_with_error(parsed_req,status_code)
    #print(last_modified_timestamp)
    if 'if-modified-since' in req_headers and status_code!='404':
        if_mod=req_headers['if-modified-since']
        flag=0
    else:
        if_mod=http_date_format(datetime.fromtimestamp(0))
        flag=1
    if 'if-unmodified-since' in req_headers and status_code!='404':
        if_unmod=req_headers['if-unmodified-since']
    else:
        if_unmod=http_date_format(datetime.utcnow())
    if status_code!='404':
        status_code=if_modified_check(if_mod,last_modified_timestamp,http_date_format(datetime.utcnow()),status_code,flag)
        status_code=if_unmodified_check(if_unmod,last_modified_timestamp,status_code)
    
    with open(root_dir+'/media_types/content-type.json') as js:
        content_type_dict=json.load(js)
        key_dict=list(content_type_dict.keys())
        value_dict=list(content_type_dict.values())
    content_type_list=content_type_decision()
    
    if not os.path.isfile(path):
        return request_with_error(parsed_req,'404')
    try:
        with open(path,'rb') as file:
            content_bytes=file.read()
    except PermissionError:
        return request_with_error(parsed_req,'403')
    suffix=pathlib.Path(path).suffix
    ext=suffix.replace(".","")
    with open(root_dir+'/status_code/status-code.json') as js:
        status_code_msg=json.load(js)
    if status_code=='412':
        request_with_error(parsed_req,'412')
    if status_code!='200':
        return request_with_error(parsed_req,status_code)
    if content_enc and status_code=='200':
        content_bytes=compression_handler(content_bytes,content_enc)
    #print(status_code)
    response_dict={'response-line':{'http-version':"HTTP/1.1",'statuscode':status_code,'status_code_msg':status_code_msg.get(status_code,"NOT FOUND Statuscode")},'responseHeaders':{"Connection":"close",'Date':http_date_format(datetime.utcnow()),'Server': "Shreeraj's Server","Content-length":str(len(content_bytes)),"Content-type":content_type_list[suffix],"Content-Encoding":content_enc,'Last-Modified':last_modified_timestamp,"Set-Cookie":gen_cookie(),'Content-Language': 'en-US','ETag':Etag},'responseBody':content_bytes}
    return response_dict
