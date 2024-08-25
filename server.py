import os
import sys
import threading
import logging
import config as cfg
from helper import request_with_error,gen_cookie, store_cookie
import responseBuilder
import requestParser

sys.path.append(os.path.abspath(os.path.join('Methods')))

from Methods.get import do_get
from Methods.head import do_head
from Methods.delete import do_delete
from Methods.post import do_post
from Methods.put import do_put
from socket_std import serverSocket

		
class HTTPServer:
	def __init__(self, host, port):
		self.serverSocket = serverSocket(host, port)
		self.serverstatus=True
		self.users=[]
		self.req_timeout=cfg.time_out
		self.max_user=cfg.max_connection
		self.cur_user_count=0
		self.port_no=port

	def helper(self,clientSocket,clientaddress):
		try:
			while self.serverstatus:
				request = self.full_req_serve(clientSocket,clientaddress)
				#print(request)
				parsedRequest=requestParser.request_parser(request)
				#print(parsedRequest)
				if parsedRequest["req_info"]["method"]=="GET":
					response_dict=do_get(parsedRequest)
					logging.info('  {}  :  {}  :  {}  :  {}  :  {}\n\n'.format(clientaddress,parsedRequest["req_info"]['method'],parsedRequest["req_info"]['uri'],response_dict['response-line']['statuscode'],response_dict['response-line']['status_code_msg']))
				elif parsedRequest["req_info"]["method"]=="HEAD":
					response_dict=do_head(parsedRequest)
					logging.info('  {}  :  {}  :  {}  :  {}  :  {}\n\n'.format(clientaddress,parsedRequest["req_info"]['method'],parsedRequest["req_info"]['uri'],response_dict['response-line']['statuscode'],response_dict['response-line']['status_code_msg']))
				elif parsedRequest["req_info"]["method"]=="DELETE":
					response_dict=do_delete(parsedRequest)
					logging.info('  {}  :  {}  :  {}  :  {}  :  {}\n\n'.format(clientaddress,parsedRequest["req_info"]['method'],parsedRequest["req_info"]['uri'],response_dict['response-line']['statuscode'],response_dict['response-line']['status_code_msg']))
				elif parsedRequest["req_info"]["method"]=="POST":
					response_dict=do_post(parsedRequest)
					logging.info('  {}  :  {}  :  {}  :  {}  :  {}\n\n'.format(clientaddress,parsedRequest["req_info"]['method'],parsedRequest["req_info"]['uri'],response_dict['response-line']['statuscode'],response_dict['response-line']['status_code_msg']))
				elif parsedRequest["req_info"]["method"]=="PUT":
					response_dict=do_put(parsedRequest)
					logging.info('  {}  :  {}  :  {}  :  {}  :  {}\n\n'.format(clientaddress,parsedRequest["req_info"]['method'],parsedRequest["req_info"]['uri'],response_dict['response-line']['statuscode'],response_dict['response-line']['status_code_msg']))
				else:
					response_dict=request_with_error('','405')
				#print("\n\n",response_dict,"\n\n")
				#self.serverSocket.send(response, 'utf-8')
				#print("\nThread-count:",threading.active_count())
				response = responseBuilder.responseBuilder(response_dict)
				#print("Response_str",response.decode())
				self.serverSocket.send(clientSocket,response)
				if(('Connection' in response_dict['responseHeaders']) and response_dict['responseHeaders']['Connection'].lower() == 'close'):
							#print("Thread stopped:",threading.active_count())
							self.serverSocket.close(clientSocket)
							self.cur_user_count-=1
							#print(len(self.users))
							return
		except:
			response_dict=request_with_error('','500')
			response=responseBuilder.responseBuilder(response_dict)
			self.serverSocket.send(clientSocket,response)
    	

	def full_req_serve(self,clientSocket,clientaddress):
		full_req = ''
		content_length = -1
		chunk = self.serverSocket.receive(clientSocket,cfg.max_bytes).decode('iso-8859-15')
		if chunk:
			full_req += chunk
			header, data  = chunk.split('\r\n\r\n', 1)
			for head in header.split('\n'):
				if "Content-Length" in head:
					content_length = int(head.split(":")[1].strip())

			#if it is either put or post request
			if content_length != -1:
				remaining_data = content_length - int(len(data))
				while(remaining_data > 0):
					next_chunk = self.serverSocket.receive(clientSocket,cfg.max_bytes).decode('iso-8859-15')
					remaining_data -= len(next_chunk)
					full_req += next_chunk
		return full_req.encode('iso-8859-15')
	def start_thread(self):
		print("Server Started Serving on : {}".format(self.port_no))
		logging.basicConfig(filename = cfg.Root+'/Logs/Activity.log', level=logging.INFO, format='%(asctime)s  :  %(filename)s  :%(message)s')
		while self.serverstatus:
			if self.cur_user_count<=self.max_user:
				try:
					clientSocket,clientaddress=self.serverSocket.accept()
				except BlockingIOError:
					#print("Blocking error happens")
					continue
				handlerThread = threading.Thread(target=self.helper,args=(clientSocket,clientaddress),daemon=True)
				self.users.append(handlerThread)
				self.cur_user_count+=1
				cookie_value=gen_cookie()
				#clientaddress=('127.0.0.1', 50578)
				store_cookie(clientaddress,cookie_value)
				handlerThread.start()
	def server_stop(self):
		waiting_period=self.req_timeout
		self.serverstatus=False
		for user in self.users:
			try:
				user.join(waiting_period)
				waiting_period=0
			except:
				print("Exception occurs in joining threads")
		#print("Stopped Server Successfully")
		return

		
if __name__ == "__main__":
	port_no=0
	if len(sys.argv)>1:
		port_no=int(sys.argv[1])
	
	server = HTTPServer('', port_no)
	StartingThread=threading.Thread(target=server.start_thread)
	StartingThread.start()
	while True:
		input_btn=input().upper()
		if input_btn=="STOP":
			print("Stopping Server Manually !!!")
			server.server_stop()
			break
		elif input_btn=="RESTART":
			server.server_stop()
			StartingThread.join()
			#print("Restarting Server Manually !!!")
			StartingNewThread=threading.Thread(target=server.start)
			StartingNewThread.start()
		else:
			print("Invalid Input !!!")
	StartingThread.join()
			
		
		

