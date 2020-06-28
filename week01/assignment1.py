'''
作业一：
#安装并使用 requests、bs4 库，爬取猫眼电影（）的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
'''

"""
因网页版访问被禁止，作业中爬取手机版

手机版单个电影元素的html结构如下：

<a href="/movie/1250952">
    <div class="classic-movie">
    <div class="avatar">
        <img src="https://p0.meituan.net/movie/ecca4f0b95340b2c57006a1bace4c3f91386100.jpg@1l_1e_1c_128w_180h" onerror="this.style.visibility='hidden'">		
    </div>
    <div class="movie-info">
        <div class="title line-ellipsis">天气之子</div>
        <div class="english-title line-ellipsis">天気の子</div>
        <div class="actors line-ellipsis">爱情,动画,奇幻</div>
        <div class="show-info line-ellipsis">2019-11-01中国大陆上映</div>
    </div>
    <div class="movie-score">
        <div class="score line-ellipsis">
            <span class="grade">9.0</span>
            <span>分</span>
        </div>
    </div>
    </div>
</a>
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

header = {'user-agent':user_agent}

# 因手机版默认一次加载10个电影，正好符合作业要求。
myurl = 'https://m.maoyan.com/films?showType=3'

response = requests.get(myurl,headers=header)

bs_info = bs(response.text, 'html.parser')

movie_dict = {'title': [], 'type': [], 'time': []}

for tags in bs_info.find_all('div', attrs={'class': 'movie-info'}):
    film_title = tags.find('div', attrs={'class': 'title line-ellipsis'}).text
    film_type = tags.find('div', attrs={'class': 'actors line-ellipsis'}).text
    film_time = tags.find('div', attrs={'class': 'show-info line-ellipsis'}).text
    # 此处进行字符串截断，取出上映日期
    film_time = film_time[0:10]

    movie_dict['title'].append(film_title)
    movie_dict['type'].append(film_type)
    movie_dict['time'].append(film_time)

maoyan_movie = pandas.DataFrame(movie_dict)
# 参数中设置编码为utf8，不需要行号，需要表头
maoyan_movie.to_csv('maoyan_movie.csv', encoding='utf-8', index=False, header=True)