#!/usr/bin/env python3
import time

import hackchat
import sys, os, traceback
import json
lockFlag = False

def words(txt):
    wList = []
    word = ''
    for c in txt:
        if (c == ' ') + (c == '@') == 0:
            word += c
        elif word != '':
            wList.append(word)
            word = ''
    if word != '':
        wList.append(word)
    return wList

  
def hc_message_got(chat, message, sender, trip, online):
  global lockFlag
  with open('users.json', 'r') as f:
    data = json.loads(f.read())
  if sender not in data:
    data[sender] = {'trip': trip,
                   'authority':'user',
                   'cookie':0,
                   'money':0,
                   'bullet':0,
                   'gun':False}
    with open('users.json', 'w') as f:
      json.dump(data, f)
  wList = words(message)
  if wList[0] == '=help':
    bot.send_message(f'''Your authority: =={data[sender]["authority"]}==
These commands are available:
|Command|Authority|Args|Effect|
|-------|---------|----|------|
|=help  |User     |None|Get help|
|=info  |User     |None|Get your info|
|=lockflag|User   |None|Check lockflag|
|=listop|Operator |None|Get oplist|
|=kill  |Operator |<nick>|Kill someone|
|=lock  |Operator |None|Lock room|
|=addop |Owner    |<trip>|Add op|
|=print |Owner    |<nick> <num>|Print money for someone|''')
  if wList[0] == '=info':
    bot.send_message(f'''These are your info:
```
{data[sender]}''')
  if wList[0] == '=lockflag':
      bot.send_message(f'Lockflag:=={lockFlag}==')
  if data[sender]["authority"] in ['op', 'owner']:
    if wList[0] == '=listop':
      opList = []
      for i in data.values():
        if i["authority"] == 'op':
          opList.append(i["trip"])
      bot.send_message(f'These trips are ==operatore==: {", ".join(opList)}')
    if wList[0] == '=kill':
      bot.send_to(wList[1], '$\\rule{10000000000000000em}{10000000000000000em}$')
      bot.send_message(f'Successfully killed =={wList[1]}==!')
    if wList[0] == '=lock':
      lockFlag = True
      bot.send_message('Successfully locked the room!')
      
  if data[sender]["authority"] == 'owner':
    if wList[0] == '=addop':
      for i in data.values():
        if i["trip"] == wList[1]:
          i["authority"] = 'op'
      bot.send_message(f'Add =={wList[1]}== as operator successfully!')
    if wList[0] == '=print':
      data[wList[1]]['money'] += eval(wList[2])
      bot.send_message(f'Successfully printed =={wList[2]}== BCoin for =={wList[1]}==!')
  print("{trip}|{user}: {message}".format(trip=trip, user=sender, message=message))
  with open('users.json', 'w') as f:
    json.dump(data, f)


def hc_user_join(chat, nick, trip):
  global lockFlag
  if lockFlag:
    bot.send_to(nick, '$\\rule{10000000000000000em}{10000000000000000em}$')
  bot.send_message("Hello, {user}.".format(user=nick))
  print("{user} joined.".format(user=nick))


def hc_user_leave(chat, nick):
  bot.send_message("Bye, {user}.".format(user=nick))
  print("{user} left.".format(user=nick))


bot = hackchat.HackChat("BBot#awa", "lounge")
bot.on_message += [hc_message_got]
bot.on_join += [hc_user_join]
bot.on_leave += [hc_user_leave]
try:
    bot.run()
except:
    print('机器人运行时异常：\n' + traceback.format_exc() + '\n现在重启！')
    py = sys.executable
    os.execl(py, py, *sys.argv)
    os._exit(0)
