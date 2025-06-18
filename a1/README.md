### How to Run:
Run the program by first running the “myvlserver.py” with python myvlserver.py  
Then run “myvlclient.py” with python myvlclient.py.  

The ip address default values should work assuming both programs  
are running on the same machine. Otherwise, they should be changed  
accordingly. 

Use the program by inputting the string that contains the length of message  
and then the message itself.  



### Example Run:

**Client Side:**  
PS C:\Users\riley\PycharmProjects\cs158a\a1> python myvlclient.py  
Input lowercase sentence: 05hello  
From Server: HELLO  
PS C:\Users\riley\PycharmProjects\cs158a\a1>  

**Server Side:**  
PS C:\Users\riley\PycharmProjects\cs158a\a1> python myvlserver.py  
Server Starting...  
Connected from: 127.0.0.1  
msg_len: 5  
processed: hello  
msg_len_sent: 5  
Connection closed  
...  

