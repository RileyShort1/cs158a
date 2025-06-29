### How to Run:
Run the program by first running the “mychatserver.py” with python mychatserver.py  
Then run “mychatclient.py” with python mychatclient.py.  

The ip address default values should work assuming both programs  
are running on the same machine. Otherwise, they should be changed  
accordingly. 

Once the server is running, it will display new connection messages as clients  
join the chat. The server will relay all client messages to each active client  
in the chat, except the sender of the message. To leave the chat, clients  
can type 'exit' and will be disconnected. 



### Example Run:

#### Server Side:
New connection from ('10.0.0.37', 62726)  
New connection from ('10.0.0.37', 62727)  
New connection from ('10.0.0.37', 62730)  
62730: Hello Guys  
62727: Hey, whats up  
62726: Just hanging out  
62730: sounds good!  

#### Client 1:  

Connected to chat server. Type 'exit' to leave.  
62730: Hello Guys  
Hey, whats up  
62726: Just hanging out  
62730: sounds good!  


#### Client 2:

Connected to chat server. Type 'exit' to leave.  
Hello Guys  
62727: Hey, whats up  
62726: Just hanging out  
sounds good!  
exit  

Disconnected from server    


#### Client 3:  

Connected to chat server. Type 'exit' to leave.  
62730: Hello Guys  
62727: Hey, whats up  
Just hanging out  
62730: sounds good!  
  
