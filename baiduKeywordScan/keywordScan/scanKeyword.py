#-*- coding:utf-8 –*-
import requests,re,threading,socket;


def scan(url):
    str = "正在处理URL："+url+"\n";
    try:
        content =  requests.get(url,timeout=4,headers={
                                             'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)'
                                         }).content;
    except:
        pass;
    #print content;
    # 匹配手机号码
    matchs = re.finditer(r'1\d{10}', content, re.M | re.I);
    if matchs:
        str += "匹配到手机号码为：";
        for it in matchs:
            str+= it.group()+"||";
        str+="\n";

    #匹配身份证号码
    matchs = re.finditer(r'\d{17}\w', content, re.M | re.I);  # 匹配手机号码
    if matchs:
        str += "匹配到身份证号码为：";
        for it in matchs:
            str += it.group() + "||";
        str += "\n";

    #匹配邮箱地址
    matchs = re.finditer(r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)', content, re.M | re.I);  # 匹配手机号码
    if matchs:
        str += "匹配到邮箱地址为：";
        for it in matchs:
            str += it.group() + "||";
        str += "\n";

    # 匹配IP地址
    matchs = re.finditer(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', content, re.M | re.I);  # 匹配手机号码
    if matchs:
        str += "匹配到IP地址为：";
        for it in matchs:
            str += it.group() + "||";
        str += "\n";

    # 匹配报错信息--bug
    matchs = re.finditer(r'mysql|oracle|sql\sserver|error|jdbc|Exception|Stacktrace|Stack\strace', content, re.M | re.I);  # 匹配报错信息
    if matchs:
        str += "匹配到报错信息为：";
        for it in matchs:
            str += it.group() + "||";
        str += "\n";
    print str+"\n";

def scan2(url):
    print url;
#scan("http://blog.csdn.net/huangwenjun1988/article/details/8152058");exit();

site = open("./urls.txt", "r");
sites = site.readlines();
site.close();


def process():
    while True:
        try:
            ss = sites.pop().replace("\r\n","").replace("\n","");
        except:
            break;
        try:
            scan(ss);
        except:
            pass;

socket.setdefaulttimeout(5);
#多线程
threads =[];
for trd in range(1,20):
	threads.append(threading.Thread(target=process));

# 启动所有线程
for t in threads:
	t.start();
#主线程中等待所有子线程退出
for t in threads:
	t.join();

print "main end\n";