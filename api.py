import json

import requests
import re
import random
import threading

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
  if '[CQ:at,qq=2900824356]' in message:
    return atme(gid, msgId)
  # if message[0:3] == '300': # 300查团分, 格式为300+游戏名称，如 “300yaq”
  #   return zhanji(uid, gid, message[3:len(message)])
  if '战绩查询' in message:
    return lolzhanji(gid, msgId)
  if '提神' in message: # 你们懂的
    return setu(gid)
  if '哈喇搜' in message:
    return halasuo(uid, gid, msgId)
  if '咕咕咕' in message:
  # if message[0:3] == '咕咕咕':
    return gugugu(uid, gid, msgId)
  if '天气' in message:
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
  eleRes = requests.get('https://op.gg/api/v1.0/internal/bypass/games/tw/summoners/'+ eleId +'?&limit=20&hl=zh_CN&game_type=total', headers={'User-Agent': random.choice(my_headers)})
  eleInfo = winCount(eleRes.json()['data'])

  nbnRes = requests.get('https://op.gg/api/v1.0/internal/bypass/games/tw/summoners/'+ nubnaId +'?&limit=20&hl=zh_CN&game_type=total', headers={'User-Agent': random.choice(my_headers)})
  nbnInfo = winCount(nbnRes.json()['data'])

  sadRes = requests.get('https://op.gg/api/v1.0/internal/bypass/games/tw/summoners/'+ sadId +'?&limit=20&hl=zh_CN&game_type=total', headers={'User-Agent': random.choice(my_headers)})
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

@Debounce(3)
def weather(uid, gid, msgId):
  shanghai = requests.get('https://devapi.qweather.com/v7/weather/3d?location=101020100&key=eff26461c820481e869c09ec6f894948')
  shanghaires = shanghai.json()['daily'][0]
  szhou = requests.get('https://devapi.qweather.com/v7/weather/3d?location=101220701&key=eff26461c820481e869c09ec6f894948')
  szhoures = szhou.json()['daily'][0]
  print(szhou.json()['daily'][0])
  suzhou = requests.get('https://devapi.qweather.com/v7/weather/3d?location=101190401&key=eff26461c820481e869c09ec6f894948')
  suzhoures = suzhou.json()['daily'][0]
  # 接口支持 和风天气 https://dev.qweather.com/
  requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, '上海：' + shanghaires['textDay'] + '  温度 ' + shanghaires['tempMin'] + '°C - '+ shanghaires['tempMax'] + '°C%0a宿州：' + szhoures['textDay'] + '  温度 ' + szhoures['tempMin'] + '°C - '+ szhoures['tempMax'] + '°C%0a苏州：' + suzhoures['textDay'] + '  温度 ' + suzhoures['tempMin'] + '°C - '+ suzhoures['tempMax'] + '°C'))


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
