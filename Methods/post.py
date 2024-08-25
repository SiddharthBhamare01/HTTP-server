import os
import sys
import pathlib
import urllib.parse
import json
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join('/Post/post_data.json')))

from helper import *
import config as cfg

def do_post(parsed_req):
    req_info=parsed_req["req_info"]
    req_headers=parsed_req["req_headers"]
    file_uri=req_info["uri"]
    status_code='200'
    if Host_checking(parsed_req)==False:
        return request_with_error(parsed_req,'400')
    if Http_version_checking(parsed_req)==False:
        return request_with_error(parsed_req,'505')
    body=parsed_req["req_body"]
    if body=="":
        return request_with_error(parsed_req,'204')
    if 'content-md5' in req_headers:
        status_code=checksum_checking(body,req_headers['content-md5'],status_code)
        if status_code!='200':
            return request_with_error(parsed_req,status_code)
    extention=None
    if 'content-encoding' in req_headers:
        body=decompression_handler(body,req_headers['content-encoding'])
    if 'content-type' in req_headers:
        con_enc=req_headers['content-type']
        extention=content_type_from_extension(con_enc)
    post_handler=None
    if extention!=None:
        post_handler=post_req_function(extention)
    if post_handler!=None:
        body=body.decode()
        body=post_handler(body)
    root=cfg.DocumentRoot['root']
    root_dir=str(pathlib.Path().absolute())
    path=root_dir+"/Post"
    status_code='200'
    datenow=datetime.utcnow()
    timestamp=http_date_format(datenow)
    data=str({timestamp:body})
    #print(data)
    Explanation_body=""
    try:
        if os.path.exists(path+"/post_data.txt"):
            with open(path+"/post_data.txt","a") as file:
                last_modified_timestamp=http_date_format(last_modified_time(path+"/post_data.txt"))
                Etag=Etag_generation(last_modified_timestamp)
                #print("Etag: ",Etag)
                if 'if-match' in req_headers:
                    status_code=if_match_status(Etag,req_headers['if-match'].split(", "),status_code)
                else:
                    status_code=if_match_status(Etag,["*"],status_code)
                if status_code!='200':
                    return request_with_error(parsed_req,status_code)
                file.write("{\n")
                file.write("\t"+data)
                file.write("\n}\n")
                Explanation_body="Resource Logged."
        else:
            with open(path+"/post_data.txt","a") as file:
                status_code='201'
                last_modified_timestamp=http_date_format(last_modified_time(path+"/post_data.txt"))
                Etag=Etag_generation(last_modified_timestamp)
                #print("Etag: ",Etag)
                if 'if-match' in req_headers:
                    status_code=if_match_status(Etag,req_headers['if-match'].split(", "),status_code)
                else:
                    status_code=if_match_status(Etag,["*"],status_code)
                if status_code!='201':
                    return request_with_error(parsed_req,status_code)
                file.write("{")
                file.write("\t"+data)
                file.write("\n}\n")
                Explanation_body="Resource Created."

    except PermissionError:
        return request_with_error(parsed_req,'403')
    except:
        status_code='500'
        return request_with_error(parsed_req,'500')
    with open(root_dir+'/status_code/status-code.json') as js:
        status_code_msg=json.load(js)
    response_dict={'response-line':{'http-version':"HTTP/1.1",'statuscode':status_code,'status_code_msg':status_code_msg.get(status_code,"NOT FOUND Statuscode")},'responseHeaders':{"Connection":"close",'Date':http_date_format(datetime.utcnow()),'Server': "Shreeraj's Server","Content-length":str(len(Explanation_body)),"Set-Cookie":gen_cookie(),'Content-Language': 'en-US','ETag':Etag},'responseBody':Explanation_body.encode()}
    return response_dict
    
    
    
