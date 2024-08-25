import sys
import os
import time
import posixpath
import urllib.parse
import urllib
import hashlib
import gzip
import pathlib
import zlib
import brotli
import json
import secrets
import config as cfg
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join('/status_code')))
sys.path.append(os.path.abspath(os.path.join('/media_types')))


from status_code.status_code import error_code_dict
from media_types.content_type import a
from media_types.content_type import content_type_decision
from responseBuilder import blank_error_msg

def http_date_format(date):
    formeted_date=""
    days={0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}
    month={1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
    formeted_date="%s, %02d %s %04d %02d:%02d:%02d GMT" % (days.get(date.weekday(),None), date.day,month.get(date.month,None), date.year, date.hour, date.minute, date.second)
    return formeted_date

def request_with_error(parsed_req,statuscode,head_req_status=False):
    err_msg=blank_error_msg()
    status_code_dict=error_code_dict()
    error_body=err_msg%{'code':statuscode,'message':status_code_dict[str(statuscode)]['message'],'explain':status_code_dict[str(statuscode)]['explaination']}
    if head_req_status != True:
        response_dict={'response-line':{'http-version':"HTTP/1.1",'statuscode':statuscode,'status_code_msg':status_code_dict[str(statuscode)]['message']},'responseHeaders':{"Connection":"close",'Date':http_date_format(datetime.utcnow()),'Server': "Shreeraj's Server","Content-length":str(len(error_body)),"Content-type":'text/html'},'responseBody':error_body.encode()}
    else:
        error_body=''
        response_dict={'response-line':{'http-version':"HTTP/1.1",'statuscode':statuscode,'status_code_msg':status_code_dict[str(statuscode)]['message']},'responseHeaders':{"Connection":"close",'Date':http_date_format(datetime.utcnow()),'Server': "Shreeraj's Server","Content-length":str(len(error_body)),'Content-Language': 'en-US'},'responseBody':''.encode()}
    return response_dict
def parse_geturl(resource_path):
		
		resource_path = resource_path.split('?',1)[0]
		resource_path = resource_path.split('#',1)[0]
		resource_path = posixpath.normpath(urllib.parse.unquote(resource_path))

	
		return resource_path

def last_modified_time(path): # Forming time stamp for given file
    time_strct=time.gmtime(os.path.getmtime(path))
    time_sec=time.mktime(time_strct)
    time_stamp=datetime.fromtimestamp(time_sec)
    return time_stamp

def if_modified_check(ifmod, lastmod,currdate,statuscode,flag):
	ifmod_sec = time.mktime(time.strptime(ifmod,'%a, %d %b %Y %H:%M:%S %Z'))
	lastmod_sec = time.mktime(time.strptime(lastmod,'%a, %d %b %Y %H:%M:%S %Z'))
	currdate_sec = time.mktime(time.strptime(currdate,'%a, %d %b %Y %H:%M:%S %Z'))
	if ifmod_sec < lastmod_sec or ifmod_sec > currdate_sec:
		if flag:
			return statuscode
		else:
			return '200'
	else:
		return '304'

def if_unmodified_check(ifunmod, lastmod,statuscode):
	ifunmod_sec = time.mktime(time.strptime(ifunmod,'%a, %d %b %Y %H:%M:%S %Z'))
	lastmod_sec = time.mktime(time.strptime(lastmod,'%a, %d %b %Y %H:%M:%S %Z'))
	if ifunmod_sec > lastmod_sec:
		return statuscode
	else:
		return '412'

def make_enc_dict(str_enc):
    enc_poosible = ["gzip","br",'compress',"deflate","identity"]
    enc_dict={}
    enc_list=str_enc.strip().split(', ')
    #print(enc_list)
    star_flag=0
    for enc_given in enc_list:
        enc_type=enc_given.split(';')
        if enc_type[0]=='*':
            star_flag=1
            q_value='1' if len(enc_type)==1 else enc_type[1]
        if len(enc_type)==1:
            if enc_type[0] in enc_poosible:
                enc_dict[enc_type[0]]='1.0'
        else:
            if enc_type[0] in enc_poosible:
                enc_dict[enc_type[0]]=enc_type[1].replace('q=','')
    if star_flag:
        enc_dict=star_encode(enc_dict,q_value)
    return enc_dict


def star_encode(enc_dict,q_value):
    enc_poosible = ["gzip","br",'compress',"deflate","identity"]
    for enc in enc_poosible:
        enc_dict.setdefault(enc,q_value)
    return enc_dict



def decide_encoding(accept_encoding):
    all_enc_list=make_enc_dict(accept_encoding)
    if len(all_enc_list)==1 and ('identity' in all_enc_list):
        if all_enc_list['identity']=='0.0':
            return None
    content_enc=max(all_enc_list.items(),key=lambda x:x[1])
    return content_enc[0]

def compression_handler(body,enc_style):
	handler={'gzip':gzip.compress,'br':brotli.compress,'deflate':zlib.compress}
	try:
		compress_fun=handler[enc_style]
		compressed_body=compress_fun(body)
	except KeyError:
		compressed_body=body
	return compressed_body

def decompression_handler(body,dec_style):
	handler={'gzip':gzip.decompress,'br':brotli.decompress,'deflate':zlib.decompress}
	try:
		decompress_fun=handler[dec_style]
		decompressed_body=decompress_fun(body)
	except KeyError:
		decompressed_body=body
	return decompressed_body

def content_type_from_extension(content_type):
	root_dir=str(pathlib.Path().absolute())
	with open(root_dir+'/media_types/content-type.json') as js:
		content_type_dict=json.load(js)
	try:
		if content_type_dict[content_type]:
			return content_type_dict[content_type]
	except KeyError:
		return None
	
def reverse_dict(dictonary):
	updated_dict={}
	for i in dictonary.items():
		updated_dict[i[1]]=updated_dict[i[0]]
	return updated_dict

def post_req_function(extention):
	possible_handler={'json':json.loads,'x-www-form-urlencoded': urllib.parse.parse_qs}
	try:
		if possible_handler[extention]:
			return possible_handler[extention]
	except KeyError:
		return None

def Host_checking(parsed_req):
	req_headers=parsed_req["req_headers"]
	if 'host' not in req_headers:
		return False
	else:
		return True

def Http_version_checking(parsed_req):
	req_headers=parsed_req["req_info"]
	if req_headers['http_version'] !='HTTP/1.1':
		return False
	else:
		return True

def Etag_generation(date_timestamp,content_enc=""):
	body=date_timestamp+content_enc
	enc_etag=body.encode()
	etag_hash=hashlib.md5(enc_etag).hexdigest() #Etag format= date + content encoding hash cause many browder support this scheme
	return etag_hash

def if_match_status(Etag_actual,if_match_list,status_code):
	old_status=status_code
	for etag in if_match_list:
		if etag==Etag_actual or etag=="*":
			status_code=old_status
			break
		else:
			status_code='412'
	else:
		status_code='412'
	return status_code

def if_none_match_status(Etag_actual,if_none_match_list,status_code):
	if if_none_match_list==[]:
		return status_code
	for etag in if_none_match_list:
		if etag=="*" or etag==Etag_actual:
			status_code= '304'
	return status_code

def q_val_dict():
    c=dict()
    for i in range(len(a)):
        if a[i][1] in c.keys():
            c[a[i][1]].append(a[i][0])
        else:
            c[a[i][1]]=[0.0,a[i][0]]
    return c
def star_subtype(availanle_cnt_type,type,q_value):
    main_type=type.split('/')[0]
    new_dict={type:[q_value]}
    #availanle_cnt_type[type]=[q_value]
    for i in availanle_cnt_type:
        if i.split('/')[0]==main_type:
            new_dict[type].extend(availanle_cnt_type[i][1:])
    availanle_cnt_type.update(new_dict)
    #print("Created: ",availanle_cnt_type)
    return availanle_cnt_type


def make_accept_decision(accept_str):
    accept_list=accept_str.split(", ")
    #print(accept_list)
    available_cnt_type=q_val_dict()
    #print(available_cnt_type)
    for i in range(len(accept_list)):
        pair=accept_list[i].split(";")
        #print(pair)
        if len(pair)==1:
            pair.append('q=1.0')
        #print(pair)
        pair[1]=pair[1].replace("q=",'')
        try:
            available_cnt_type[pair[0]][0]=float(pair[1])
        except KeyError:
            available_cnt_type[pair[0]]=[float(pair[1])]
        #print(available_cnt_type)
        if pair[0].split('/')[1]=="*":
            available_cnt_type= star_subtype(available_cnt_type,pair[0],float(pair[1]))
    sorted_dict=sorted(available_cnt_type.items(),key=lambda x:x[1][0],reverse=True)
    s=[]
    #print("Sortedduct",sorted_dict)
    for i in range(len(sorted_dict)):
        if sorted_dict[i][1][0]==0.0:
            break
        if len(sorted_dict[i][1])>1:
            s.extend(sorted_dict[i][1][1:])
    return s


def check_file(path,accept_str):
    ext_possible=make_accept_decision(accept_str)
    file=path.rstrip(pathlib.Path(path).suffix)
    for i in ext_possible:
        if os.path.isfile(file+i):
            ext=i
            break
    else:
        ext=-1
    return ext

def both_star_accept(path):
    if os.path.isfile(path):
        return pathlib.Path(path).suffix
    ext=content_type_decision()
    file=path.rstrip(pathlib.Path(path).suffix)
    for i in ext:
        if os.path.isfile(file+i):
            ext=i
            break
    else:
        ext=None
    return ext

def store_cookie(address, random_cookie_num):
    lines=[]
    with open(cfg.Root+'/cookies.txt','r') as file:
        lines=[line.split('----') for line in file.readlines()]
    #print(lines)
    innerflag=0
    for i in range(len(lines)):
        if lines[i][0]==str(address):
            innerflag=1
            lines[i][1]=str(int(lines[i][1])+1)
            lines[i][2]=random_cookie_num+'\n'
    if innerflag:
        with open(cfg.Root+'/cookies.txt','w') as file:
            for i in lines:
                file.write("----".join(i))
    else:
        with open(cfg.Root+'/cookies.txt','a+') as file:
            file.write("----".join([str(address),'1',random_cookie_num])+'\n')
    return
def gen_cookie():
		cookie_value = secrets.token_urlsafe(16)
		return cookie_value 

def checksum_creater(body,content_md_5,status_code):
    checksum=hashlib.md5(body)
    checksum=checksum.hexdigest()
    if checksum!=content_md_5:
        return '400'
    else:
        return status_code