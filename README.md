# Client Server Project
This client server project uses Python sockets along with threading in order to function. It can send instant messages as well as send files to the other program running.
## Run the Program
+ Start the server python file ` python Server.py `
+ Start the client python file ` python Client.py `
## How to use
+ Type ` Message ` then the message to send the message to the other python program
+ Type ` File ` then the file in the current directory to send to the other python program
### Notes
+ This is run from the local address of 127.0.0.1 for both the client and the server not over the open internet
+ The file being sent over needs to be in the current directory
+ Threading is used to make the instant messaging happen in real time
