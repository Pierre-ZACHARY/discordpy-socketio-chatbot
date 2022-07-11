fork of https://github.com/squid/discord-py-heroku with some websocket implementation

# Hosting your discord.py bot on Heroku
### What are the prerequisites for this guide?
You must have an account for Discord [[Link](https://discordapp.com/developers/applications/)], GitHub [[Link](https://github.com/join)] , and Heroku [[Link](https://signup.heroku.com/)].

### How do I create a bot and get a bot token?
* Create an application in the developer portal by clicking [here](https://discordapp.com/developers/applications/)
* Open up your new application and click 'Add Bot' under the Bot settings to create your bot.
* After creating the bot, click the 'Copy' button under the title Token. Take note of your token as you will need it later.

### How to fork the repository and set it up to work with Heroku?
* Fork a copy of this repository by clicking the 'Fork' on the upper right-hand.
* Create an application for Heroku by clicking [here](https://dashboard.heroku.com/new-app).
* Under 'Deploy', do the following:
  * Deployment Method => Connect your GitHub
  * App connected to GitHub => Search for the forked repository
  * Automatic Deploy => Enable Automatic Deploy (to redeploy after every commit)
* Under 'Settings', click on 'Reveal Config Vars' and enter the following:
  * KEY => DISCORD_TOKEN
  * VALUE => (Enter the bot token that you copied from the developer portal)
  * Click the 'Add' button after entering all of this information.
* Under 'Resources', do the following:
  * Click on the 'Pencil' icon.
  * Switch the worker from off to on.
  * Click 'Confirm' to finalize the decision.
  * NOTE: You are allocated 550 free Dyno hours, which will not last the entire month. However, if you provide a credit card to verify your identity, you are given an additional 450 hours, which will allow your bot to run indefinitely.

### Pierre ZACHARY websocket chatbot
* first, create a new Category on a discord server where your bot is ( give the bot admin right if you don't want any problem )
* Get this new Category id ( see how to enable Discord developer mode ), and set it inside a "CHANNEL_ID" env variable
* this app will open a websocket, listen for messages and type them in the channel
* there is a file called client.py to test the communication with the server
* You may want to add multiple websites, in this case you can add a new env variable for each, with a dedicated category id as value, and add that category id to the "websites" dict ( see main.py line 15 ). Client side, you will have to select which category by adding the website "key" to your uri path ( see client.py line 8 ). Here my default key is "CHANNEL_ID", so if I want to send on message inside this category, I add "/CHANNEL_ID" after my uri


# TO-DO LIST
* Revise the tutorial to be easier to understand for any user.
* Add some images for following along with the process.
* 