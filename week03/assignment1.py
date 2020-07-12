# 调用示例：
# 单个主机
# python assignment1.py -n 3 -ip 127.0.0.1 -f tcp
# 多个主机
# python assignment1.py -n 3 -ip 192.168.1.1-192.168.10.10 -f ping

import argparse
import subprocess
from multiprocessing import Manager, Pool
from time import sleep, time
import random
import os

def ip2num(ip):
    ips = [int(x) for x in ip.split('.')]
    return ips[0] << 24 | ips[1] << 16 | ips[2] << 8 | ips[3]

def num2ip(num):
    return '%s.%s.%s.%s' % ((num >> 24) & 0xff, (num >> 16) & 0xff, (num >> 8) & 0xff, num & 0xff)

def gen_ip_list_from_range(begin_ip, end_ip):
    start = ip2num(begin_ip)
    end = ip2num(end_ip)
    ret = []
    for n in range(start, end + 1):
        if n & 0xff:
            ret.append(num2ip(n))
    return ret

def scan(ip, q, f):
    # 如果用户输入的参数是ping,则调用ping函数，否则调用nc函数
    if 'ping' == f:
        ping_ret = ping(ip)
        if '' != ping_ret:
            q.put(ping_ret)
    else:
        nc_ret = nc(ip)
        q.put({ip : nc_ret})

def ping(ip):
    ret = subprocess.call(f'ping {ip} -c 3', shell=True)
    if 0 == ret:
        return ip
    else:
        return ''

def nc(ip):
    results = subprocess.Popen(f'nc -z -v {ip} 1-1024 2>&1 | grep succeeded', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    stdout, stderr = results.communicate() 
    res = stdout.decode('utf-8')
    ret_list = []
    if len(res) > 0:
        tmp_list = res.split('\n')
        for item in tmp_list:
            if len(item) > 0:
                item_str_list = item.split(' ')
                if len(item_str_list) >= 5:  
                    ret_list.append(item_str_list[4])
    return ret_list

if __name__ == "__main__":

    # 解析参数
    parser = argparse.ArgumentParser(prog = 'assignment1', description = 'scan hosts and ports, use -n, -f, -ip, -w')
    parser.add_argument('-n', type=int, default=1)
    parser.add_argument('-f', type=str, default='ping')
    parser.add_argument('-ip', type=str, default='192.168.0.1')
    parser.add_argument('-w', type=str, default='out.json')
    args = parser.parse_args()

    # 对参数做简单校验
    if not('ping' == args.f or 'tcp' == args.f):
        exit('-f must be ping or tcp')

    if args.n < 1:
        exit('-n must >= 1')

    iplist = args.ip.split('-')
    if not(len(iplist) == 1 or len(iplist) == 2):
        exit('-ip must be one ip ,or a range of ip')

    # 如果是ip区间
    if 2 == len(iplist) :
        iplist = gen_ip_list_from_range(iplist[0], iplist[1])

    # 根据用户输入的参数创建进程池
    p = Pool(args.n)

    # 如果要在进程池里面使用queue进行通信的话，要用Manager().Queue()
    q = Manager().Queue()
    print("父进程开始")

    for ip in iplist:
        p.apply_async(scan, args=(ip, q, args.f))

    p.close()
    p.join()
    
    # 打印ping得通的主机ip，并且打印其开启的端口
    for i in range(q.qsize()):
        print(q.get(True))

    print("父进程结束。")
    p.terminate()