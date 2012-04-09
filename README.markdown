# Web application to support easy text message voting for favorite Hackathon project

This is a really simple app, it doesn't even have a database (it stores all the information in memory). Regardless, it updates in real time, can support an unlimited amount of teams, doesn't let any single vote twice, and rejects invalid votes (with a nice text message).

If you are looking for an example of what it looks like, check out http://hackvote.herokuapp.com.

## Setup

To configure, fork and clone the repository.

Next, open up the `server.py` file and add any projects you'd like into the `projects` array.

    projects = [{"name": "Jesse, Mark and Brennen's Project", "descr":"An awesome project!", "votes":3}]
  
Then, create a new Heroku application:

    heroku create --stack cedar 
    git push heroku master
  
Now, create a Twilio account if you don't already have one and go to the Apps section of the settings. Create a new TwiML app and set your "request URL" to:

    http://your-heroku-app.herokuapp.com/vote
  
With this set up, you should be able to vote by texting to the number on your Twilio account!

Hope this can help someone do easy crowd sourced voting for their Hackathon!

