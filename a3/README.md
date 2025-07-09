### How to Run:
To run the program, create the number of config files you want to run  
Run each instance of the "myleprocess.py" script with two command line arguments -  
The full path of the config file and the path and/or name of the log file you want  
the program to create. These two arguments are optional, without providing them,  
the program will default to looking for a "config.txt" file in the working directory  
and creating a generic "log.txt" file in the working directory. 



### Example Run:

#### Node 1:
Sent: 45cda432-6bde-4d67-861a-6adeb2b12afe, flag=0, 0  
Received: uuid=b866adaf-7b10-4f16-8cf1-84e3b916ecde, flag=0, greater, 0  
Sent: uuid=b866adaf-7b10-4f16-8cf1-84e3b916ecde, flag=0, greater, 0  
Received: uuid=b866adaf-7b10-4f16-8cf1-84e3b916ecde, flag=1, 0  
Leader is decided to b866adaf-7b10-4f16-8cf1-84e3b916ecde  
Leader is b866adaf-7b10-4f16-8cf1-84e3b916ecde    

#### Node 2:  
Sent: 8b31d479-685e-4a8f-81f0-cd8ebc3c01ca, flag=0, 0  
Ignored: uuid=45cda432-6bde-4d67-861a-6adeb2b12afe, flag=0 less, 0  
Received: uuid=b866adaf-7b10-4f16-8cf1-84e3b916ecde, flag=0, greater, 0  
Sent: uuid=b866adaf-7b10-4f16-8cf1-84e3b916ecde, flag=0, greater, 0  
Received: uuid=b866adaf-7b10-4f16-8cf1-84e3b916ecde, flag=1, 0  
Leader is decided to b866adaf-7b10-4f16-8cf1-84e3b916ecde  
Leader is b866adaf-7b10-4f16-8cf1-84e3b916ecde    


#### Node 3:
Sent: b866adaf-7b10-4f16-8cf1-84e3b916ecde, flag=0, 0  
Ignored: uuid=8b31d479-685e-4a8f-81f0-cd8ebc3c01ca, flag=0 less, 0  
Leader is decided to b866adaf-7b10-4f16-8cf1-84e3b916ecde  
Sent=b866adaf-7b10-4f16-8cf1-84e3b916ecde, flag=1, equal, 1  
Leader is b866adaf-7b10-4f16-8cf1-84e3b916ecde      
 
