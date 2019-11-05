# Select_Seats
As we know, reservation can be made in advance and new seats will be opened at 22:00 every night. But when the time is coming, we can be really hard to sign in the reservation system because all people wanna get into it and select a more comfortable seat. Unfortunately, the system does not getting enough optimization so that their carrying capacity does not allow so many students to use the system at the same time. That is the main reason why I write the automated script. 
One the one hand, using the script can reduce personal unnecessary	operations to lower the pressures on the server. On the other hand, we can liberate our time to do more stuff like studying. The script can help us choose the seat we want accurately and efficiently with greater possibilities(nearly 100% unless other student use the script and pick the same seat).
## Environment 
Python  
requests  
logging  
(All in the last version can run)  

## Parameter Setting
"number":"************",    //学号  
"password":"******",        //登录密码  
"date":"today",             //选座日期，默认日期为次日，当参数为"today"时，选择当日的座位  
"beginTime":10,             //开始时间  
"duration":12,              //学习时长  
"studyroom":"2n",           //选择自习室（3楼南:"3S"或"3s"，3楼北:"3N"或"3n"，2楼南:"2S"或"2s"，2楼北:"2N"或"2n"）  
"seat":"100",              //选择座位，选择的座位没选上可就近匹配  
"distinct":12               //优先选择座位距离seat的距离  

## Usage
After you built your environment and fill your information into setting.json with the same format, cd to the folder you store the files, and input the command in terminal

`python select_seats.py setting.json `
You can build a task schedule to run it before 22:00 everyday.

