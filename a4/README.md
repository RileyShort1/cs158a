### How to Run:
To run the program, create the number of config files you want to run  
each instance of the "myleprocess.py" script with two command line arguments -  
The full path of the config file and the path and/or name of the log file you want  
the program to create. These two arguments are optional, without providing them,  
the program will default to looking for a "config.txt" file in the working directory  
and creating a generic "log.txt" file in the working directory. 



### Example Run:

#### Node 1:
Sent: uuid=94e557a3-35c3-4cc7-8571-02386720812a, flag=0  
Received: uuid=d5758340-6598-4371-8f64-0613fc13fea9, flag=0, greater, 0  
Received: uuid=dc3bb932-0066-498c-93ae-fa857a5e8b65, flag=0, greater, 0  
Sent: uuid=d5758340-6598-4371-8f64-0613fc13fea9, flag=0  
Sent: uuid=dc3bb932-0066-498c-93ae-fa857a5e8b65, flag=0  
Received: uuid=dc3bb932-0066-498c-93ae-fa857a5e8b65, flag=1, greater, 0  
Leader is decided to dc3bb932-0066-498c-93ae-fa857a5e8b65  
Sent: uuid=dc3bb932-0066-498c-93ae-fa857a5e8b65, flag=1  
  
Leader is dc3bb932-0066-498c-93ae-fa857a5e8b65     

#### Node 2:  
Received: uuid=94e557a3-35c3-4cc7-8571-02386720812a, flag=0, less, 0  
Sent: uuid=dc3bb932-0066-498c-93ae-fa857a5e8b65, flag=0    
Ignored: uuid=94e557a3-35c3-4cc7-8571-02386720812a, flag=0  
Received: uuid=d5758340-6598-4371-8f64-0613fc13fea9, flag=0, less, 0  
Ignored: uuid=d5758340-6598-4371-8f64-0613fc13fea9, flag=0  
Received: uuid=dc3bb932-0066-498c-93ae-fa857a5e8b65, flag=0, equal, 0  
Leader is decided to dc3bb932-0066-498c-93ae-fa857a5e8b65  
Sent: uuid=dc3bb932-0066-498c-93ae-fa857a5e8b65, flag=1  
Received: uuid=dc3bb932-0066-498c-93ae-fa857a5e8b65, flag=1, equal, 1  
  
Leader is dc3bb932-0066-498c-93ae-fa857a5e8b65     


#### Node 3:
Received: uuid=dc3bb932-0066-498c-93ae-fa857a5e8b65, flag=0, greater, 0  
Sent: uuid=d5758340-6598-4371-8f64-0613fc13fea9, flag=0  
Sent: uuid=dc3bb932-0066-498c-93ae-fa857a5e8b65, flag=0  
Received: uuid=dc3bb932-0066-498c-93ae-fa857a5e8b65, flag=1, greater, 0  
Leader is decided to dc3bb932-0066-498c-93ae-fa857a5e8b65  
Sent: uuid=dc3bb932-0066-498c-93ae-fa857a5e8b65, flag=1  
  
Leader is dc3bb932-0066-498c-93ae-fa857a5e8b65       
 
