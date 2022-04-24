# CONNECT
#### Description:
This website serves as a platform for people to connect with each other through similar hobbies. Users are able to join events organised by others or even created their own event. In my project, I referenced the videos and links provided by the CS50 team.

**login.html**
log-in page.

**register.html**
For users to create their account. In this page, I included various input boxes for users to submit. After clearing the data validation, the information would be added to a database.

**index.html**
The homepage after logging in. I included a table for users to see their upcoming events. From this table, I considered what information to input as the table would not be able to fit all the information. I also added a function for the user to withdraw from the activitiy. This button linked to a withdraw page taking the input as the information from the table.

**events.html**
This page allowed users to browse through all the activities in the database. If they choose to filter events based on their hobbies, there is a drop-down box function. Just to make the interface better, I made the table header a variable that could change based on the hobby. After viewing the various activities, users could press on join to join the event. Upon joining the event (passing the data validation: such as is the event oversubscribed), users would receive an email to their registered gmail account.

**for_you.html**
This page was something I thought would be interesting to attempt. When the user loads this page, the number of events for each hobby that the user has joined will be counted, and the hobby the user is "most" interested in will be filtered. The user will view other events of the same hobby in this page. If there is a tie in terms of number of events per hobby, the other hobby (decided by alphabatical order) will be suggested via a submit input box, linking the user back to the events page.

**create.html**
This page allowed users to create their own activity. Once it passed the data validation, everyone will be able to view and join their event. User who created the event will automatically be added to the event. An email will also be sent to the registered gmail account to confirm the creation of event.

**change_password.html**
Similar to the registration page, users can change their password here after confirming their account details (by knowing the previous password).

**layout.html**
Building on what the CS50 team has done in one example of a layout function, I read up about the functions and their usage, and editted the layout accordingly to fit this website.

**connect.db**
In this SQL table, I created 4 different tables. The users table stored user account information. Activities stored every information regarding an event. participant stored the detail of every participant who joined any event. I linked these 2 tables together often to obtain who joined which event. The last 2 tables were to help me with data validation. The date_checker table was used to check when the event has expired. Once the event has expired (ie event date is before today), the event will be automatically removed from the system. The fyp table helped me filter the users individual hobies into a seperate table that I could select from. Both these tables were appended and deleted upon every login as a way of updating. I considered combining the tables into the users table but I felt that making an individual table to serve each purpose would be clearer.

**application.py**
Here, I made use of what I have learned over the past few weeks to perform checks on the user input as well as link pages to each other. With the help of the flask documentation, I attempted to send an email with a html.

It was really enjoyable making this website. Looking back, this course has been a fun, albeit tough journey. I learned alot starting from being completely clueless to making a website of my own, due largely in part to the CS50 team and the online community.
