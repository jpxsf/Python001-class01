# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql

class Assignment1Pipeline:
    def __init__(self):
        # 此处提交时隐去用户名密码
        self.db=pymysql.connect(host='localhost',user='xxx',passwd='xxx',
                                db='maoyanmovie',charset='utf8',port=3306)
        self.cur=self.db.cursor()

    def process_item(self, item, spider):
        sql='INSERT INTO maoyan(title,type,time) VALUES(%s,%s,%s,%s) '
        self.cur.execute(sql,(item['title'],item['type'],item['time']))
        self.db.commit()
        return item
      
    def close_spider(self, spider):
        self.cur.close()
        self.db.close()

