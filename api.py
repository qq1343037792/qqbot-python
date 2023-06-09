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
  if message[0:3] == '300': # 300查团分, 格式为300+游戏名称，如 “300yaq”
    return zhanji(uid, gid, message[3:len(message)])
  if '提神' in message: # 你们懂的
    setu(gid)
  if '哈拉搜' in message:
    halasuo(uid, gid, msgId)
  if '咕咕咕' in message:
  # if message[0:3] == '咕咕咕':
    gugugu(uid, gid, msgId)
  if '合并' in message:
    hebingmsg(uid, gid)

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
  
@Debounce(5)
# 合并转发消息
def hebingmsg(uid, gid):
  print('执行合并')
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
