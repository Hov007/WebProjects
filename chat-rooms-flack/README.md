# Project 2

Web Programming with Python and JavaScript
Flack web based chat application

# application.py

application.py contains all ruotes and backend code,
• /signin route backend of signin in to web site
• /logout
• /create code of creating a new channel, and /channels/<channel> wich lets you
  to stay on the same page with new channels
• And some socket code, join_room, leave_room and send message wich is connected
  with index.js

# helpers.py

  helpers.py contains some code wich let you to import @login_required
  function

# index.js

index.js contains all javascript and socketio code wich lets you to connect all
files together

# templates

This folder contains all html files
• layout.html contains navbar and buttons wich is the same in other html files
• signin.html signin page
• index.html home page where you can create a new channel or join to existed one
• channel.html this show you in wich channel you are, and chatroom itself
• error.html shows you the individual error you get

# static
contains css files, png file for logo, and index.js
• error.css style for error.html
• style.css all css style for html files
