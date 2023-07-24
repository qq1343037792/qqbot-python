import json

import requests
import re
import random
import threading
import config
# import schedule
# import time

class Debounce:
  def __init__(self, interval):
      self.interval = interval
      self.debounced = None

  def __call__(self, func):
      def decorator(*args, **kwargs):
          if self.debounced is not None:
              self.debounced.cancel()
          self.debounced = threading.Timer(self.interval, func, args, kwargs)
          self.debounced.start()
      return decorator

#'下面这个函数用来判断信息开头的几个字是否为关键词'
#'如果是关键词则触发对应功能，群号默认为空'
def keyword(message, uid, gid = None, msgId = None):
  print(message)
  print(gid)

  if '[CQ:at,qq='+ str(config.BOT_QQ) +']' in message and config.ADMIN_QQ != uid:
    return atme(gid, msgId)
  # if message[0:3] == '300': # 300查团分, 格式为300+游戏名称，如 “300yaq”
  #   return zhanji(uid, gid, message[3:len(message)])
  # if '[CQ:at,qq='+ config.BOT_QQ +']' in message and config.ADMIN_QQ == uid and '给我打' in message:
  #   return fight(uid, gid, msgId)
  if message[0:2] == '热搜':
    return baiduresou(gid)
  if '战绩查询' in message:
    return lolzhanji(gid, msgId)
  if message[0:2] == '提神':
    return setu(gid)
  if '哈喇搜' in message:
    return halasuo(uid, gid, msgId)
  if '咕咕咕' in message:
  # if message[0:3] == '咕咕咕':
    return gugugu(uid, gid, msgId)
  if message[0:2] == '天气':
    return weather(uid, gid, msgId)
  if '合并' in message:
    return hebingmsg(uid, gid)
# 300战绩查询
def zhanji(uid, gid, name):
    url = 'https://300report.jumpw.com/api/getrole?name=' + name
    menu = requests.get(url)
    for i in menu.json()['Rank']:
        if i['RankName'] == '团队实力排行':
            tuanfen = i['Value']
    if gid != None:
      # 如果是群聊信息
      requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}团分{2}'.format(gid, name, tuanfen))
    else:
      # 如果是私聊信息
   		requests.get(url='http://127.0.0.1:5700/send_private_msg?user_id={0}&message={1}团分{2}'.format(uid, name, tuanfen))

@Debounce(3)
def atme(gid, msgId):
  # requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, '@我干叼'))
  requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, '[CQ:reply,id=' + str(msgId) + ']' + '@我干叼' + '[CQ:image,file=emoji1.png]'))
  # requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, '[CQ:image,file=emoji1.png]'))

@Debounce(3)
def fight(uid, gid, msgId):
  requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, '[CQ:image,file=emoji2.png]'))
  return 

@Debounce(5)
# lol战绩查询
def lolzhanji(gid, msgId):
  eleId = 'gfKaKVRVrS2QhgcCVb9JFVIQEUpSONic6L86J6ad6G8G4XLtLEoiV5x_Qw'
  nubnaId = 'mX_bUEf0UAGkbRUbtMoqLS5NS3CK0hYZmXhq-THQ4WWeUec_bQ7YWIz5CQ'
  sadId = 'eZCjuSJuFQfwQQpcMnr02Z5vq9rweIYv1u6IgJi0n1K1xX2Pwa0PA8QqbQ'

  my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
  ]
  eleRes = requests.get('https://op.gg/api/v1.0/internal/bypass/games/tw/summoners/'+ eleId +'?&limit=20&hl=zh_CN&game_type=aram', headers={'User-Agent': random.choice(my_headers)})
  eleInfo = winCount(eleRes.json()['data'])

  nbnRes = requests.get('https://op.gg/api/v1.0/internal/bypass/games/tw/summoners/'+ nubnaId +'?&limit=20&hl=zh_CN&game_type=aram', headers={'User-Agent': random.choice(my_headers)})
  nbnInfo = winCount(nbnRes.json()['data'])

  sadRes = requests.get('https://op.gg/api/v1.0/internal/bypass/games/tw/summoners/'+ sadId +'?&limit=20&hl=zh_CN&game_type=aram', headers={'User-Agent': random.choice(my_headers)})
  sadInfo = winCount(sadRes.json()['data'])
  requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, r'近20场胜率 ELEGANTZ：' + str(eleInfo) + r'%, 觉得离谱：' + str(nbnInfo) + r'%, sadlessman：' + str(sadInfo) + '%'))

# 胜率计算
def winCount(rankData):
  wins = 0
  for i in rankData:
    if i['myData']['team_key'] == 'RED':
      if i['teams'][1]['game_stat']['is_win'] == True:
        wins = wins + 1
    elif i['myData']['team_key'] == 'BLUE':
      if i['teams'][0]['game_stat']['is_win'] == True:
        wins = wins + 1
  return (wins * 100) // 20 

# 提神图
@Debounce(5)
def setu(gid): 
  key = ''
  url = 'https://api.lolicon.app/setu?apikey=' + key + r'&size1200=true'
  menu = requests.get(url)
  setu_url = menu.json()['data'][0]['url'] # 对传回来的涩图网址进行数据提取
  requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, r'[CQ:image,' r'file=' + str(setu_url) + r']'))

@Debounce(5)
# 回复特定消息
def halasuo(uid, gid, msgId):
  print('执行halasuo')
  requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, r'[CQ:reply,' r'id=' + str(msgId) + r']' + '哈几把哈'))

@Debounce(5)
def gugugu(uid, gid, msgId):
  requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, r'[CQ:reply,' r'id=' + str(msgId) + r']' + '懂得都懂'))

# 天气查询
@Debounce(3)
def weather(uid, gid, msgId):
  # 上海
  shanghai = requests.get('https://devapi.qweather.com/v7/weather/3d?location=101021500&key=' + config.WEATHER_KEY)
  shanghaiNow = requests.get('https://devapi.qweather.com/v7/weather/now?location=101021500&key=' + config.WEATHER_KEY)
  shanghaires = shanghai.json()['daily'][0]
  shanghaiNowRes = shanghaiNow.json()
  # 埇桥
  yongqiao = requests.get('https://devapi.qweather.com/v7/weather/3d?location=101220706&key=' + config.WEATHER_KEY)
  yongqiaoNow = requests.get('https://devapi.qweather.com/v7/weather/now?location=101220706&key=' + config.WEATHER_KEY)
  yongqiaores = yongqiao.json()['daily'][0]
  yongqiaoNowRes = yongqiaoNow.json()
  # 泗县
  sixian = requests.get('https://devapi.qweather.com/v7/weather/3d?location=101220704&key=' + config.WEATHER_KEY)
  sixianNow = requests.get('https://devapi.qweather.com/v7/weather/now?location=101220704&key=' + config.WEATHER_KEY)
  sixianres = sixian.json()['daily'][0]
  sixianNowRes = sixianNow.json()
  # 苏州
  suzhou = requests.get('https://devapi.qweather.com/v7/weather/3d?location=101190405&key=' + config.WEATHER_KEY)
  suzhouNow = requests.get('https://devapi.qweather.com/v7/weather/now?location=101190405&key=' + config.WEATHER_KEY)
  suzhoures = suzhou.json()['daily'][0]
  suzhouNowRes = suzhouNow.json()
  # 合肥
  hefei = requests.get('https://devapi.qweather.com/v7/weather/3d?location=101220101&key=' + config.WEATHER_KEY)
  hefeiNow = requests.get('https://devapi.qweather.com/v7/weather/now?location=101220101&key=' + config.WEATHER_KEY)
  hefeires = hefei.json()['daily'][0]
  hefeiNowRes = hefeiNow.json()

  tempList = [int(shanghaiNowRes['now']['temp']), int(yongqiaoNowRes['now']['temp']), int(sixianNowRes['now']['temp']), int(suzhouNowRes['now']['temp']), int(hefeiNowRes['now']['temp'])]
  face0 = getFace(0,tempList)
  face1 = getFace(1,tempList)
  face2 = getFace(2,tempList)
  face3 = getFace(3,tempList)
  face4 = getFace(4,tempList)

  # 接口支持 和风天气 https://dev.qweather.com/
  line = '%0a--------------------------'
  requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, ('普陀：' + '当前 ' + shanghaiNowRes['now']['text'] + '   ' + shanghaiNowRes['now']['temp'] + '°C' + face0 + '%0a          今日 ' + shanghaires['tempMin'] + '°C - '+ shanghaires['tempMax'] + '°C' +
                                                                                          line +
                                                                                          '%0a埇桥：' + '当前 ' + yongqiaoNowRes['now']['text'] + '   ' + yongqiaoNowRes['now']['temp'] + '°C' + face1 + '%0a          今日 ' + yongqiaores['tempMin'] + '°C - '+ yongqiaores['tempMax'] + '°C' +
                                                                                          line +
                                                                                          '%0a泗县：' + '当前 ' + sixianNowRes['now']['text'] + '   ' + sixianNowRes['now']['temp'] + '°C' + face2 + '%0a          今日 ' + sixianres['tempMin'] + '°C - '+ sixianres['tempMax'] + '°C' +
                                                                                          line +
                                                                                          '%0a吴中：' + '当前 ' + suzhouNowRes['now']['text']+ '   ' + suzhouNowRes['now']['temp'] + '°C' + face3 + '%0a          今日 ' + suzhoures['tempMin'] + '°C - '+ suzhoures['tempMax'] + '°C' +
                                                                                          line +
                                                                                          '%0a合肥：' + '当前 ' + hefeiNowRes['now']['text']+  '   ' + hefeiNowRes['now']['temp'] + '°C' + face4 + '%0a          今日 ' + hefeires['tempMin'] + '°C - '+ suzhoures['tempMax'] + '°C')))
  
def getFace(i, list):
  if(list[i] == max(list)):
    return '[CQ:face,id=11]'
  if(list[i] < max(list) and list[i] > min(list)):
    return '[CQ:face,id=10]'
  if(list[i] == min(list)):
    return '[CQ:face,id=4]'

#百度热搜
@Debounce(5)
def baiduresou(gid):
  url = 'https://top.baidu.com/board?tab=realtime'
  res = requests.get(url)
  r = res.text
  data = re.search('(<!--s-data:)({.+})(-->)', r)
  # r = json.loads(data.groups()[1])["data"]["cards"][0]["content"][:cnt]
  r = json.loads(data.groups()[1])["data"]["cards"][0]["content"]
  # print(r)
  msg_list = ['百度热搜榜']
  for i,obj in enumerate(r):
    # result = '%d、%2ahot:%2a链接:%s'%(i+1,obj["desc"],obj["hotScore"],'')
    result = '%d、%s\nhot:%s\n链接:%s'%(i+1,obj["desc"],obj["hotScore"],obj["appUrl"])
    msg_list.append(result)

  print(msg_list)
  try:
    requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, msg_list))
  except:
    requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, '寄了啊'))

@Debounce(5)
# 合并转发消息
def hebingmsg(uid, gid):
  print('执行合并')
  # to do
  msg = ['测试消息1', '测试消息2', '测试消息3']
  group_msg = []
  for item in msg:
    each_msg = {
      "type": "node",
      "data": {
          "name": "QQ昵称",
          "uin": 2900824356,
          "content": item
      }
    }
  group_msg.append(each_msg)
  postData = {
    'group_id': gid,
    'messages': group_msg
  }
  res = requests.post('http://127.0.0.1:5700/send_group_forward_msg', data=postData)
  print(res.json())

# 早上报时
# def morning():
#   # requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, '[CQ:image,file=emoji2.png]'))
#   print('报时')
#   return

# schedule.every().monday.at("15:43").do(morning)
# schedule.every().tuesday.at("09:00").do(morning)
# schedule.every().wednesday.at("09:00").do(morning)
# schedule.every().thursday.at("09:00").do(morning)
# schedule.every().friday.at("09:00").do(morning)

# while True:
#   schedule.run_pending() # 运行所有可运行的任务