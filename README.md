# Dynalist Chatbot

A chatbot which can push messages from a channel like Telegram to your dynalist inbox working with the [Recast.AI](https://recast.ai) platform.

> **Note:** This project is currently in beta version and can be modified at any time.


## Test the bot
### Add the bot 
#### Via Webchat
**Webchat script**

```javascript
<script src="https://cdn.recast.ai/webchat/webchat.js"
channelId="a4b980bb-7d48-451a-8dff-f1c57849c676"
token="48374a061050040522cfa81d56a0002e"
id="recast-webchat"
></script>
```

**Optional**
```javascript
// Put the meta tag below for mobile responsive
<meta name="viewport" content="width=device-width">
```

#### Via Telegram
You can find it with the UserName [@DynalistInboxBot](t.me/DynalistInboxBot)


## Requirements for forking the bot
### Setup
##### Recast.AI account

Create an account on the [Recast.AI](https://recast.ai) platform.

##### Inspect the bot

You can find the logic of the bot [here](https://recast.ai/pojo93/dynalist-inbox/)


### Installation

#### Local

First clone the project:
```bash
git clone git@github.com:PoJo93/dynalist-chatbot.git my-bot && cd my-bot
```

Then, install the dependencies:

Using pip
```bash
pip install -r requirements.txt
```

Using easy\_install
```bash
easy_install `cat requirements.txt`
```

## Deployment


### Run locally

`REQUEST_TOKEN=xxx LANGUAGE=xxx PORT=xxx python server.py`


- Download [ngrok](https://ngrok.com/)
- Launch: `ngrok http 5000`
- Copy the url ngrok outputs
- Paste it in the [Recast.AI](https://recast.ai) interface: Go to your bot page, click on the **RUN** tab and edit your `current bot webhook`
- Chat with your bot on the channels you've configured ;)

### SAP Clound Foundry
Currently it has all necessary files to be deployed under SAP Cloudfoundry. Follow [this](https://blogs.sap.com/2017/12/04/deploying-flaskbottle-python-app-rest-api-on-sap-cloud-foundry/) tutorial to set up the hosting on SAP Cloudfoundry








## Usage


## More
You can view the whole API reference at [man.recast.ai](https://man.recast.ai).


