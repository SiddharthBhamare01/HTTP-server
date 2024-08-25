def request_parser(request):
    request_dict={};headers_dict={};req_info={}
    count=0
    updated_req=request.strip()
    Bodysplit=updated_req.split("\r\n\r\n".encode(),1)
    Fullrequest=Bodysplit[0]
    Fullrequest=Fullrequest.decode('utf-8')
    request_body=""
    if len(Bodysplit)>1:
        request_body=Bodysplit[1]
    #print("Request_body:",request_body)
    Request_split=Fullrequest.strip().split("\r\n")
    Headers=Request_split[1:]
    FirstLine=Request_split[0].split(" ")
    req_info["method"]=FirstLine[0]
    req_info["uri"]=FirstLine[1]
    req_info["http_version"]=FirstLine[2]
    for header in Headers:
        pair=header.split(":",1)
        headers_dict[pair[0].strip().lower()]=pair[1].strip()
    format={0:"req_info",1:"req_headers",2:"req_body"}
    for ele in [req_info,headers_dict,request_body]:
        request_dict[format.get(count,None)]=ele
        count+=1
    return request_dict
    



    
