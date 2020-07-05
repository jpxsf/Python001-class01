'''
作业二：

使用 requests 或 Selenium 模拟登录石墨文档 https://shimo.im
'''

'''
石墨文档登录时会请求https://shimo.im/lizard-api/auth/password/login，如果是204则表示登录成功
'''

import requests
from fake_useragent import UserAgent


ua = UserAgent(verify_ssl=False)

# headers里面除了ua和referer还要添加如下所示的其他信息，否则会403
headers = {
    'user-agent' : ua.random,
    'referer' : 'https://shimo.im/login?from=home',
    'origin' : 'https://shimo.im',
    'x-requested-with' : 'XmlHttpRequest',
    'x-source' : 'lizard-desktop'
}

# 使用session来保证多次请求是在同一个会话中的
s = requests.Session()

login_url = 'https://shimo.im/lizard-api/auth/password/login'

# 此处填写手机号和密码
# 注意如果是国内手机号，前面要加+86，否则会返回{'errorcode':3, 'error':'找不到该用户'}
form_data = {
    'mobile' : '',
    'password' : ''
}

# 进行登录
login_response = s.post(login_url, data=form_data, headers=headers)

# 如果登录成功，就去获取个人信息
if 204 == login_response.status_code : 

    me_url = 'https://shimo.im/lizard-api/users/me'
    me_response = s.get(me_url, headers = headers, cookies=s.cookies)

    print('login success!')
    print('me info is :')
    print(me_response.text)
    
else :

    print('login failed!')
