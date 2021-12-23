# IHT-chatbot

The Interplay of Humanity and Technology-New Trends and New Competencies (I) (人文科技的交響：新趨勢與新素養（一）) 2021 - Final presentation chatbot

## QRcode

* Notice 
  * It is recommended to use mobile phone to interact with this chatbot
  * The first response may take longer time because the app on Heroku would turn off if no one interacts with it for a period of time

![qrcode](./qrcode.png)

## How to start

### Environment property

Fill in the following environment variables:

```
channel_access_token=
channel_secret=
```

### Test in local

1. Run `python3 app.py`
2. Open another terminal, run `ngrok http 5000`
3. Copy the ngrok url to LINE Developer Console and add `/callback` behind the url
4. Have fun!

### Deploy on Heroku

1. Run `heroku login -i`  to login heroku
2. Run `heroku git:remote -a <your_heroku_app_name> ` in the local directory with this repo
3. Set the environment variables list above on Heroku

```
heroku config:set channel_access_token=
heroku config:set channel_secret=
```

5. Run `git push heroku` , and the chatbot server will start
6. Copy the Heroku url to LINE Developer Console and add `/callback` behind the url
7. Have fun!

## Staff

* Script: 
  * 吳宣瑜, 楊銘祥, 陳虹瑄, 蕭楚真

* Information collection: 
  * 方姸晴, 李研, 李宥頡, 柳硯, 崔皓翔, 張晉維, 陳禹廷, 曾繁宸, 黃威綸, 塗捷安, 劉湛湛, 鄭品妘 

* Coding:
  * 陳柏衡

* Teaching assistant
  * 文心