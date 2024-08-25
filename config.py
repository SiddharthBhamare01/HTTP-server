#This is config file for my server should be used for holding various path and necessary info for configuartin of Server.
import pathlib

Allow =["GET","POST","HEAD","DELETE","PUT"]

DocumentRoot={
    'root':str(pathlib.Path().absolute())+'/Root_Src'
}

Root = str(pathlib.Path().absolute())

Autherization={
    'type':'Basic',
    'username':'shreeraj',
    'password':'shree@123'
}

max_bytes = 1048576

max_connection=100

max_listen=25

time_out=20.0

Delete_Root=Root+'/Delete_Src'
