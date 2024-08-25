def responseBuilder(response_dict):
    response_line = response_dict['response-line']['http-version'] + " "
    response_line += response_dict['response-line']['statuscode'] + " "
    response_line += response_dict['response-line']['status_code_msg']
    headersDict = response_dict['responseHeaders']
    response_body = response_dict['responseBody']
    response_line = response_line + "\r\n"
    for i in headersDict:
        response_line += i+": "+headersDict[i]+"\r\n"
    response_line+="\r\n"
    response_line = response_line.encode()
    response_line+=response_body
    return response_line

def blank_error_msg():
    error_msg="""<!DOCTYPE">
    <html>
	    <head><meta http-equiv="Content-Type" content="text/html;charset=utf-8">
		    <title>Error response</title>
	    </head>
	    <body>
		    <h1>%(code)s - %(message)s.</h1>
		    <p>%(explain)s</p>
            <br>
		    <hr>
		    <address>Shreeraj's Server (Ubuntu) Server at 127.0.0.1</address>
	    </body>
    </html>"""
    return error_msg
