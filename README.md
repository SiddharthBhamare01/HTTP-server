# Http-server


<h3 align="right">HTTP Server</h3>

<div align="center">

</div>

---

<p align="center"> HTTP Server is an HTTP/1.1 compliant web server and is aimed at implementing some common methods for exchanging information.
    <br> 
</p>

## 📝 Table of Contents

- [Features](#features)
- [About](#about)
- [Usage](#usage)
- [Running Tests](#tests)
- [Logging](#log)
- [Environment](#built_using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🎯 Features <a name="features"></a>
:heavy_check_mark: __Supports 5 common HTTP methods__ - GET, POST, PUT, DELETE and HEAD <br>
:heavy_check_mark: __Multithreaded__ <br>
:heavy_check_mark: __Configuration options__ <br>
:heavy_check_mark: __Level based logging support__ <br>
:heavy_check_mark: __Support for cookies__ <br>
:heavy_check_mark: __Automated basic testing__ <br>

## 🧐 About <a name = "about"></a>

This project is aimed at the implementation of the HTTP/1.1 Protocol based on RFC 2616 and incorporates the basic `HTTP` methods of `GET`, `POST`, `PUT`, `DELETE` and `HEAD`.

### Prerequisites

1. Python 3.x

Clone this repository, extract it if you downloaded a .zip or .tar file and cd into the cloned repository.:

For Example :
```sh
$ cd A:\http-server
```

### 🏁 Usage <a name = "usage"></a>

Follow the below steps to start the server

```sh
$ python3 server.py [Port]
```
_**Note : Port = Port number where we want to start the server**_

This will start the server on a default port of as mentioned in the configuration file. To specify custom configuration edit the config file in the config/ directory. The following options are available in the config file

```
1. Autherization = Added Autherization purpose to serve Delete Method with autherized User 
2. DocumentRoot = Specify the document root directory that will serve the requests (DEFAULT : Root_Src)
3. max_connection= Specify the maximum number of simultaneous connections that the server will accept (DEFAULT : 100)
4. time_out = Specify the Timeout value for the response (DEFAULT : 20.0 seconds)
5. Delete_Root = Specify the repository used to store Files/ directories deleted [Recovery Purpose] (DEFAULT : Delete_Src)
6. ACCESS_LOG = Specify the file to save access logs (DEFAULT : Logs/Activity.log )
7. POST_LOG = Specify the file to save post logs (DEFAULT : Post/post_data.txt)
8. Cookies = Implemented 16 digit random number based on creation timestamp to simulate Cookies behaviour
9. LOG_FORMAT = Specify the format to write access logs from the server
10. Allow = Methods Supported by Custom HTTP-Server.

```

Once the server starts, it will start a background process that serves connections from clients.
To stop the server do the following:

```sh
$ stop
```

To restart the server do the following:

```sh
$ restart
```

## 🔧 Running the tests <a name = "tests"></a>

Automated test scripts to test the specified functionalities can be found in the `tester.py` file

### Automated Unit Tests

These tests ensure the conformance of the basic functionalities and the correctness of the responses. All the supported methods are tested and variable paramters can be tuned to test specific scenarios.

#### To run unit test module do the following:

```sh
$ python3 tester.py PORT_NO (DEFAULT : 1200)
```

```
The tester.py combilned of possible Tests as following :

i] GET Request :
    1) Normal GET Request(200 : Ok)
    2) 404 : Not Found
    3) Coditional GET Request (304 : Not Modified)
    4) 412 : Precondition Failed
    5) 406 : Not Acceptable
    6) Content-Negotiated GET Request (200 : Ok)
    7) MultiClient GET Request (STRESS GET Requests)

ii] HEAD Request :
    1) Normal HEAD Request(200 : Ok)
    2) 404 : Not Found
    3) Coditional HEAD Request (304 : Not Modified)
    4) 412 : Precondition Failed
    5) 406 : Not Acceptable
    6) Content-Negotiated HEAD Request (200 : Ok)
    7) MultiClient HEAD Request (STRESS HEAD Requests)

iii] POST Request :
    1) Normal Post Request(200 : Ok)
    2) Conditional POST Request (412: Forbidden) 
    3) 204 : No Content
    4) MultiClient POST Request (STRESS POST Requests)

iv] PUT Request :
    1) Normal Put Request(200 : Ok)
    2) 201 : Created
    3) 415:Unsupported Media Type
    4) 204 : No Content
    5) PUT Request (201:Created) Using Only Directory
    6) 412:Pre-Condition Failed
    7) MultiClient PUT Request (STRESS PUT Requests)

v] DELETE Request :
    1) Valid Delete Request (200 : OK)
    2) 401 : Unauthorized
    3) 404 : Not Found
    4) Conditional DELETE Request (412 : Pre-Condition Failed)
    5) MultiClient DELETE Request (STRESS DELETE Requests)
```

#### To run tests for cookies:

1. Run an instance of the server
2. Go to a browser and type the url `http://localhost:[PORT]/index.html`
3. Corresponding **Cookie** Stored in cookies.txt, just copy ip_address and port_number of client paste at line no. 105 of server.py as a tuple.
4. Again Refresh same page,[ make GET Request for same page ], it will simulate the behaviour of Cookies Service.



## ✍️ Logs <a name="log"></a>

The logs to the server requests as well as internal server state can be viewed in the `Logs` directory. There are two types of logs maintained by the server:

1. Access Logs ( DEFAULT : Logs/Activity.log )
2. POST Request Logs ( DEFAULT : Post/post_data.txt )

<b>Access Logs</b>
Keeps track of all the requests served successfully by the server alongwith the response code. The default format of the access logs:

```
[DATETIME] Filename-accessed (CLIENT_IP, CLIENT_PORT_NO) REQUEST RESPONSE 
```

The log format can be changed from the config file to match a desired format.


<b>POST Logs</b>

Keeps track of all the POST requests served successfully by the server alongwith the response code. The default format of the access logs:

```
[HTTP DATETIME-timestamp] (CLIENT_IP, CLIENT_PORT_NO) {FORM_DATA in json format}
```

The log format can be changed from the config file to match a desired format.


## ⛏️ Environment <a name = "built_using"></a>

- **Python - Server Environment**

## ✍️ Authors <a name = "authors"></a>

- [**Siddharth Bhamare**](https://github.com/SiddharthBhamare01)<br />
_**Subject - Computer Networks**_<br />
_**Division - 01 , TY Computer**_<br />
_**Watumull Institute of Electronics Engineering and Computer Technology, Mumbai**_<br />


## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- [RFC 2616](https://tools.ietf.org/html/rfc2616)
- [RFC 6265](https://tools.ietf.org/html/rfc6265)
- [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP)
