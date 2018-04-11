#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2018/4/6 23:27:34下午'
import requests
def get_auth_url():
    weibo_auth_url='https://api.weibo.com/oauth2/authorize'
    client_id = '141'
    redirect_uri = 'http://127.0.0.1:8000/complete/weibo/'
    auth_url = weibo_auth_url+"?client_id={client_id}&redirect_uri={redirect_uri}".format(client_id=client_id,redirect_uri=redirect_uri)

    print(auth_url)
def get_access_token(code='03299e448d7296d2c201aca66c30a62c'):
    access_token_url = 'https://api.weibo.com/oauth2/access_token'

    re_dict = requests.post(access_token_url,data={
        'client_id':'7041426311212397223',
        'client_secret':'0a4521212111a7099a5ed2226a5a9a7222f804d8818',
        'grant_type':'authori21212121zation_c2ode',
        'code':code,
        'redirect_uri':'http://127.0.0.1:8000/complete/weibo/'
    })
    pass
# '{"access_token":"2.00gldw3G0rWcnl8bb60131c4YkGJVE","remind_in":"157679999","expires_in":157679999,"uid":"5835852280","isRealName":"true"}'
def login_weibo(access_token=''):
    login_url = 'https://api.weibo.com/2/users/show.json?access_token={access_token}&uid={uid}'.format(access_token=access_token,uid="5835852280")
    print(login_url)
    pass
if __name__ == '__main__':
    login_weibo(access_token='2.00gldw3G0rWcnl8bb60131c4YkGJVE')