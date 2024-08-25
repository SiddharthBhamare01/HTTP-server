import requests
from threading import Thread
import unittest
import json
import time
import sys
from requests import auth
from requests.auth import HTTPBasicAuth
from datetime import datetime
from helper import http_date_format


def header_dic_formatting(header_dict):
    str=""
    for key_header in header_dict:
        str+=key_header+" : "+header_dict[key_header]+'\n'
    return str

class Tester_GET(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Tester_GET,self).__init__( *args, **kwargs)
        self.total_recv=0
    def test_get_01(self):
        print("\nMaking a Normal GET Request\n")
        try:
            response = requests.get(my_server_url + "/")
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            self.assertEqual(response.status_code,200)
            print("\n\tGET Test - 01 Pass..!!!\n")
        except Exception as ex:
            print('\n\tGET Test - 01 Fail..!!!!\n', ex)
    def test_get_02(self):
        print("\nMaking a (404: NOT FOUND) GET Request\n")
        try:
            response = requests.get(my_server_url + "/bdhjsbh.html")
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\tHeaders:", header_dic_formatting(response.headers))
            self.assertEqual(response.status_code,404)
            print("\n\tGET Test - 02 Pass..!!!\n")
        except Exception as ex:
            print('\n\tGET Test - 02 Fail..!!!!', ex)
    def test_get_03(self):
        print("\nMaking a Conditional GET Request from If-Modified-since\n")
        try:
            custom_header={}
            response = requests.get(my_server_url + "/bye.html")
            print("\tLast-Modified : ",response.headers['Last-Modified'])
            date=http_date_format(datetime.utcnow())
            print('\n\n\tIf-Modified-Since :',date)
            custom_header['If-Modified-Since']=date
            response = requests.get(my_server_url + "/bye.html",headers=custom_header)
            self.assertEqual(response.status_code,304)
            print(f"\n\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tGET Test - 03 Pass..!!!\n")
        except Exception as ex:
            print('\n\tGET Test - 03 Fail..!!!!', ex)
    def test_get_04(self):
        print("\nMaking a (412:Precondition Failed) GET Request from If-Unmodified-since\n")
        try:
            custom_header={}
            custom_header['If-Unmodified-Since']='Fri, 12 Nov 2021 09:05:24 GMT'
            response = requests.get(my_server_url + "/bye.html",headers=custom_header)
            self.assertEqual(response.status_code,412)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tGET Test - 04 Pass..!!!\n")
        except Exception as ex:
            print('\n\tGET Test - 04 Fail..!!!!', ex)
    def test_get_05(self):
        print("\nMaking a (406 Not Acceptable) GET Request from Accept-Encoding\n")
        try:
            custom_header={}
            custom_header['Accept-Encoding']='identity;q=0.0'
            response = requests.get(my_server_url + "/",headers=custom_header)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            self.assertEqual(response.status_code,406)
            print("\n\tGET Test - 05 Pass..!!!\n")
        except Exception as ex:
            print('\n\tGET Test - 05 Fail..!!!!\n', ex)
    def test_get_06(self):
        print("\nMaking a (Content-Negotiated) GET Request from Accept Header\n")
        try:
            custom_header={}
            custom_header['Accept']='image/png'
            response = requests.get(my_server_url + "/image.jpg",headers=custom_header)
            self.assertEqual(response.status_code,415)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tGET Test - 05.5 Pass..!!!\n")
            custom_header['Accept']='image/*'
            response = requests.get(my_server_url + "/image.jpg",headers=custom_header)
            self.assertEqual(response.status_code,200)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            
            print("\n\tGET Test - 06 Pass..!!!\n")
        except Exception as ex:
            print('\n\tGET Test - 06 Fail..!!!!\n', ex)
    def multiple_get_request(self,num):
        for i in range(num):
            response=requests.get(my_server_url+'/')
            if response.status_code==200:
                self.total_recv+=1
        return self.total_recv
    def test_get_07(self):
        print("\nMaking a MultiClient GET Request\n")
        get_thread=[]
        for i in range(4):
            thread=Thread(target=self.multiple_get_request,args=(5,))
            get_thread.append(thread)
            thread.start()
        for thd in get_thread:
            thd.join() 
        try:
            self.assertEqual(self.total_recv,20)
            print('\n\tGET Multi-Client-Test - 07 Pass..!!!!\n')
        except Exception as ex:
            print('\n\tGET Multi-Client-Test - 07 Fail..!!!!\n', ex)
        self.total_recv=0
    def test_head_01(self):
        print("\nMaking a Normal HEAD Request\n")
        try:
            response = requests.head(my_server_url + "/")
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            self.assertEqual(response.status_code,200)
            print("\n\tHEAD Test - 01 Pass..!!!\n")
        except Exception as ex:
            print('\n\tHEAD Test - 01 Fail..!!!!\n', ex)
    def test_head_02(self):
        print("\nMaking a (404: NOT FOUND) HEAD Request\n")
        try:
            response = requests.head(my_server_url + "/bdhjsbh.html")
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\tHeaders:", header_dic_formatting(response.headers))
            self.assertEqual(response.status_code,404)
            print("\n\tHEAD Test - 02 Pass..!!!\n")
        except Exception as ex:
            print('\n\tHEAD Test - 02 Fail..!!!!', ex)
    def test_head_03(self):
        print("\nMaking a Conditional HEAD Request from If-Modified-since\n")
        try:
            custom_header={}
            response = requests.head(my_server_url + "/bye.html")
            
            print("\tLast-Modified : ",response.headers['Last-Modified'])
            date=http_date_format(datetime.utcnow())
            print('\n\n\tIf-Modified-Since :',date)
            custom_header['If-Modified-Since']=date
            response = requests.head(my_server_url + "/bye.html",headers=custom_header)
            self.assertEqual(response.status_code,304)
            print(f"\n\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tHEAD Test - 03 Pass..!!!\n")
        except Exception as ex:
            print('\n\tHEAD Test - 03 Fail..!!!!', ex)
    def test_head_04(self):
        print("\nMaking a (412:Precondition Failed) HEAD Request from If-Unmodified-since\n")
        try:
            custom_header={}
            custom_header['If-Unmodified-Since']='Fri, 12 Nov 2021 09:05:24 GMT'
            response = requests.head(my_server_url + "/bye.html",headers=custom_header)
            self.assertEqual(response.status_code,412)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tHEAD Test - 04 Pass..!!!\n")
        except Exception as ex:
            print('\n\tHEAD Test - 04 Fail..!!!!', ex)
    def test_head_05(self):
        print("\nMaking a (406 Not Acceptable) HEAD Request from Accept-Encoding\n")
        try:
            custom_header={}
            custom_header['Accept-Encoding']='identity;q=0.0'
            response = requests.head(my_server_url + "/",headers=custom_header)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            self.assertEqual(response.status_code,406)
            print("\n\tHEAD Test - 05 Pass..!!!\n")
        except Exception as ex:
            print('\n\tHEAD Test - 05 Fail..!!!!\n', ex)
    def test_head_06(self):
        print("\nMaking a (Content-Negotiated) HEAD Request from Accept Header\n")
        try:
            custom_header={}
            custom_header['Accept']='image/png'
            response = requests.head(my_server_url + "/image.jpg",headers=custom_header)
            self.assertEqual(response.status_code,415)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tHEAD Test - 05.5 Pass..!!!\n")
            custom_header['Accept']='image/*'
            response = requests.head(my_server_url + "/image.jpg",headers=custom_header)
            self.assertEqual(response.status_code,200)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            
            print("\n\tHEAD Test - 06 Pass..!!!\n")
        except Exception as ex:
            print('\n\tHEAD Test - 06 Fail..!!!!\n', ex)
    def multiple_head_request(self,num):
        for i in range(num):
            response=requests.head(my_server_url+'/')
            if response.status_code==200:
                self.total_recv+=1
        return self.total_recv
    def test_head_07(self):
        print("\nMaking a MultiClient HEAD Request\n")
        head_thread=[]
        for i in range(4):
            thread=Thread(target=self.multiple_head_request,args=(5,))
            head_thread.append(thread)
            thread.start()
        for thd in head_thread:
            thd.join() 
        try:
            self.assertEqual(self.total_recv,20)
            print('\n\tHEAD Multi-Client-Test - 07 Pass..!!!!\n')
        except Exception as ex:
            print('\n\tHEAD Multi-Client-Test - 07 Fail..!!!!\n', ex)
        self.total_recv=0
    def test_post_01(self):
        print("\nMaking a POST Request \n")
        try:
            custom_header={}
            data_dict=json.dumps({'testkey':'testdata'})
            custom_header['Content-Type']='application/json'
            response = requests.post(my_server_url + "/",data=data_dict,headers=custom_header)
            self.assertEqual(response.status_code,200)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tPOST Test - 01 Pass..!!!\n")
        except Exception as ex:
            print('\n\tPOST Test - 01 Fail..!!!!\n', ex)
    def test_post_02(self):
        print("\nMaking a Conditional POST (412: Forbidden) Request with If-Match \n")
        try:
            custom_header={}
            data_dict=json.dumps({'testkey':'testdata'})
            custom_header['Content-Type']='application/json'
            custom_header['If-Match']='b1a158edc0298f17b70d230e3163f03b'
            response = requests.post(my_server_url + "/",data=data_dict,headers=custom_header)
            self.assertEqual(response.status_code,412)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tPOST Test - 02 Pass..!!!\n")
        except Exception as ex:
            print('\n\tPOST Test - 02 Fail..!!!!\n', ex)
    def test_post_03(self):
        print("\nMaking a No Content POST (204:No Content) \n")
        try:
            custom_header={}
            #data_dict=json.dumps({'testkey':'testdata'})
            custom_header['Content-Type']='application/json'
            #custom_header['If-Match']='b1a158edc0298f17b70d230e3163f03b'
            response = requests.post(my_server_url + "/",data='',headers=custom_header)
            self.assertEqual(response.status_code,204)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tPOST Test - 03 Pass..!!!\n")
        except Exception as ex:
            print('\n\tPOST Test - 03 Fail..!!!!\n', ex)
    def multiple_post_request(self,num):
        custom_header={}
        data_dict=json.dumps({'multiclientkey':'multiclientdata'})
        custom_header['Content-Type']='application/json'
        for i in range(num):
            response=requests.post(my_server_url+'/',data=data_dict,headers=custom_header)
            if response.status_code==200:
                self.total_recv+=1
        return self.total_recv
    def test_post_04(self):
        print("\nMaking a MultiClient POST Request\n")
        post_thread=[]
        for i in range(4):
            thread=Thread(target=self.multiple_post_request,args=(5,))
            post_thread.append(thread)
            thread.start()
        for thd in post_thread:
            thd.join() 
        try:
            self.assertEqual(self.total_recv,20)
            print('\n\tPOST Multi-Client-Test - 04 Pass..!!!!\n')
        except Exception as ex:
            print('\n\tPOST Multi-Client-Test - 04 Fail..!!!!\n', ex)
        self.total_recv=0
    def test_put_01(self):
        print("\nMaking a PUT Request (201 : Created) \n")
        try:
            custom_header={}
            data='Test Data Created'
            custom_header['Content-Type']='text/plain'
            #custom_header['If-Match']='b1a158edc0298f17b70d230e3163f03b'
            response = requests.put(my_server_url + "/Test_PUT/Test_PUT1/test_file.txt",data=data,headers=custom_header)
            self.assertEqual(response.status_code,201)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tPUT Test - 01 Pass..!!!\n")
        except Exception as ex:
            print('\n\tPUT Test - 01 Fail..!!!!\n', ex)
    def test_put_02(self):
        print("\nMaking a PUT Request (200:Ok) \n")
        try:
            custom_header={}
            data='Test Data 2 Created'
            custom_header['Content-Type']='text/plain'
            #custom_header['If-Match']='b1a158edc0298f17b70d230e3163f03b'
            response = requests.put(my_server_url + "/Put/test2.txt",data=data,headers=custom_header)
            self.assertEqual(response.status_code,200)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tPUT Test - 02 Pass..!!!\n")
        except Exception as ex:
            print('\n\tPUT Test - 02 Fail..!!!!\n', ex)
    def test_put_03(self):
        print("\nMaking a PUT Request (415:Unsupported Media Type) \n")
        try:
            custom_header={}
            data_dict=json.dumps({"key":"value"})
            custom_header['Content-Type']='application/json'
            #custom_header['If-Match']='b1a158edc0298f17b70d230e3163f03b'
            response = requests.put(my_server_url + "/Put/test2.txt",data=data_dict,headers=custom_header)
            self.assertEqual(response.status_code,415)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tPUT Test - 03 Pass..!!!\n")
        except Exception as ex:
            print('\n\tPUT Test - 03 Fail..!!!!\n', ex)
    def test_put_04(self):
        print("\nMaking a PUT Request (204:No Content) \n")
        try:
            custom_header={}
            data_dict=''
            custom_header['Content-Type']='application/json'
            #custom_header['If-Match']='b1a158edc0298f17b70d230e3163f03b'
            response = requests.put(my_server_url + "/Put/test_file.txt",data=data_dict,headers=custom_header)
            self.assertEqual(response.status_code,204)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tPUT Test - 04 Pass..!!!\n")
        except Exception as ex:
            print('\n\tPUT Test - 04 Fail..!!!!\n', ex)
    def test_put_05(self):
        print("\nMaking a PUT Request (201:Created) Using Only Directory \n")
        try:
            custom_header={}
            data_dict=json.dumps({'Testing Data':'Data Tested'})
            custom_header['Content-Type']='application/json'
            #custom_header['If-Match']='b1a158edc0298f17b70d230e3163f03b'
            response = requests.put(my_server_url + "/Put",data=data_dict,headers=custom_header)
            self.assertEqual(response.status_code,201)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tPUT Test - 05 Pass..!!!\n")
        except Exception as ex:
            print('\n\tPUT Test - 05 Fail..!!!!\n', ex)
    def test_put_06(self):
        print("\nMaking a PUT Request (412:Pre-Condition Failed) Using  \n")
        try:
            custom_header={}
            data_dict='Testing Data Manually'
            custom_header['Content-Type']='text/plain'
            custom_header['If-Match']='b1a158edc0298f17b70d230e3163f03b'
            response = requests.put(my_server_url + "/Put/test2.txt",data=data_dict,headers=custom_header)
            self.assertEqual(response.status_code,412)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tPUT Test - 06 Pass..!!!\n")
        except Exception as ex:
            print('\n\tPUT Test - 06 Fail..!!!!\n', ex)
    def multiple_put_request(self,num):
        custom_header={}
        data_dict=json.dumps({'MulticlientKey':'MulticlientKey Data'})
        custom_header['Content-Type']='application/json'
        for i in range(num):
            response=requests.put(my_server_url+'/Test_PUT/MultiClient_PUT_Test',data=data_dict,headers=custom_header)
            if response.status_code==201:
                self.total_recv+=1
        return self.total_recv
    def test_put_07(self):
        print("\nMaking a MultiClient PUT Request\n")
        put_thread=[]
        for i in range(4):
            thread=Thread(target=self.multiple_put_request,args=(5,))
            put_thread.append(thread)
            thread.start()
        for thd in put_thread:
            thd.join() 
        try:
            self.assertEqual(self.total_recv,20)
            print('\n\tPUT Multi-Client-Test - 07 Pass..!!!!\n')
        except Exception as ex:
            print('\n\tPUT Multi-Client-Test - 07 Fail..!!!!\n', ex)
        self.total_recv=0
    def test_remove_delete_01(self):
        print("\nMaking a DELETE Request (401:Unauthorized)\n")
        try:
            response = requests.delete(my_server_url + "/hello.html")
            self.assertEqual(response.status_code,401)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tDELETE Test - 01 Pass..!!!\n")
        except Exception as ex:
            print('\n\tDELETE Test - 01 Fail..!!!!\n', ex)
    def test_remove_delete_02(self):
        print("\nMaking a DELETE Request (404:Not Found)\n")
        try:
            response = requests.delete(my_server_url + "/jsdbjhs.html",auth=HTTPBasicAuth('shreeraj','shree@123'))
            self.assertEqual(response.status_code,404)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tDELETE Test - 02 Pass..!!!\n")
        except Exception as ex:
            print('\n\tDELETE Test - 02 Fail..!!!!\n', ex)
    def test_remove_delete_03(self):
        print("\nMaking a Conditional DELETE Request (412 : Pre-Condition Failed) using Etag\n")
        try:
            custom_header={}
            custom_header['If-Match']='b1a158edc0298f17b70d230e3163f03b'
            response = requests.delete(my_server_url + "/file_tobe_delete.html",headers=custom_header,auth=HTTPBasicAuth('shreeraj','shree@123'))
            self.assertEqual(response.status_code,412)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tDELETE Test - 03 Pass..!!!\n")
        except Exception as ex:
            print('\n\tDELETE Test - 03 Fail..!!!!\n', ex)
    def test_remove_delete_04(self):
        print("\nMaking a Valid  DELETE Request\n")
        try:
            response = requests.delete(my_server_url + "/file_tobe_delete.html",auth=HTTPBasicAuth('shreeraj','shree@123'))
            self.assertEqual(response.status_code,200)
            print(f"\tStatus : {response.status_code} {response.reason}")
            #print("\n\tHeaders:", header_dic_formatting(response.headers))
            print("\n\tDELETE Test - 04 Pass..!!!\n")
        except Exception as ex:
            print('\n\tDELETE Test - 04 Fail..!!!!\n', ex)
if __name__=='__main__':
    print("\n\nTesting Started....\n\n")
    my_server_url='http://localhost:1200'
    unittest.main()

