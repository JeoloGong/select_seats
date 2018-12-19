# Select_Seats
As we know, reservation can be made in advance and new seats will be opened at 22:00 every night. But when the time is coming, we can be really hard to sign in the reservation system because all people wanna get into it and select a more comfortable seat. Unfortunately, the system does not getting enough optimization so that their carrying capacity does not allow so many students to use the system at the same time. That is the main reason why I write the automated script. 
One the one hand, using the script can reduce personal unnecessary	operations to lower the pressures on the server. On the other hand, we can liberate our time to do more stuff like studying. The script can help us choose the seat we want accurately and efficiently with greater possibilities(nearly 100% unless other student use the script and pick the same seat).
## Environment 
Python
requests
logging
(All in the last version can run)

## Usage
After you built your environment and fill your information into setting.json with the same format, cd to the folder you store the files, and input the command in terminal

`python select_seats.py`
You can build a task schedule to run it before 22:00 everyday.
