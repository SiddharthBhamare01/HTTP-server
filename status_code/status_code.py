import json
a="""{ 
	"200": 
		{
			"message": "OK",
			"explaination": "none"
		},
	"404":
		{
			"message": "Not Found",
			"explaination": "The requested URI doesnot exists in the server."
		},
	"400":
		{
			"message": "Bad Request",
			"explaination": "Your browser sent a request that this server could not understand."
		},
	"201":
		{
			"message": "Created",
			"explaination": "none"
		},
	"415":	{
			"message": "Unsupported Media Type",
			"explaination": "The requested URI doesnot match the media type."
		},
	"405":	{
			"message": "Method Not Allowed",
			"explaination": "Requested method is not implemented on the specified resources."
		},
	"204":	{
			"message": "No Content",
			"explaination": "No Content Provided to Server"
		},
	"505":	{
			"message": "Http Version Not Supported",
			"explaination": "Requested version is not supported by the browser."
		},
	"501":  {
			"message": "Not Implemented",
			"explaination": "The server doesnot support the functionality to fulfill the request."	
		},
	"413": {
			"message": "Payload Too Large",
			"explaination": "Requested resource payload exceeds the server limit."
		},
	"304": {
			"message": "Not modified",
			"explaination": "The requested resource has not been modified."
		},
	"412": {
			"message": "Pre-condition Failed",
			"explaination": "The requested resource has been modified."
		},
	"500": {
			"message": "Internal Server Error",
			"explaination": "server encountered an unexpected condition that prevented it from fulfilling the request. "
		},
	"403": {
			"message" : "Access to Resource is Forbidden",
			"explaination" : "Requested Resource doesnot have required file permissions."
	       },
	"401": {
			"message" : "Unauthorized",
			"explaination" : "operation requires the authorisation."	
		},
	"503": {
			"message" : "Service unavailable",
			"explaination": "Server is not ready to handle the request."
	       },
	"406": {
			"message" : "Not Acceptable",
			"explaination": "Server cannot produce a response matching the list of acceptable values"
		   }
}"""

def error_code_dict():
    b=json.loads(a)
    return b