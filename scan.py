#-*- coding:utf-8 –*-
import requests,re,threading;

#从百度获取搜索后的加密链接
def getBaiduURL(keyword):
    print "getBaiduURL\n";
    urls=set();
    first = 1;
    for i in range(1, 10):
        baiduURL="https://www.baidu.com/s?wd=site:"+keyword+"&pn="+str(first)+"&rn=50";
        #print baiduURL;
        try:
            baiduBody = requests.get(baiduURL,
                                     headers={
                                         'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)',
                                        "Cookie":"sug=3; sugstore=0; ORIGIN=0; bdime=0; BAIDUID=3AB18E233C1C3A551CAA22006503B9D9:FG=1; PSTM=1489974930; BIDUPSID=FDD497C29FC1BFE6909A41A5D9D649F0; H_WISE_SIDS=114456_102065_100185_114823_114652_114743_100100_114669_107918_112107_107319_114132_114843_115055_115054_115044_114797_114741_114513_115021_114998_114330_114535_115032_114922_114276_114718_114946_114078_110085; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_645EC=d08eTpmujjGV4zzpcJ3ctzZpQ1FvcL83KrmCIjEfm6nMFteG%2BUG8eDiDGpi%2Fy1XcFiTp; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_CK_SAM=1; PSINO=1; BD_HOME=1; H_PS_PSSID=1451_21108_17001_22159; BD_UPN=123253"
                                     },
                                     timeout=3).content;
            matchs = re.finditer(r'(http:|https:)\/\/www.baidu.com\/link\?url\=\S+\"', baiduBody, re.M | re.I);
            for it in matchs:
                site = it.group().replace("\"", "");
                urls.add(site)

            first += 50;
        except:
            pass;

    return urls;

#从百度加密链接中提取真实链接v1
def getTrueURL(trueURL,keyword):
    print "getTrueURL --  keyword 为："+keyword;
    trueURL_t = set();
         # 获取真实链接 
    while True:
        try:
            url = trueURL.pop();
            if url:
                site2 = requests.get(url, timeout=3,verify=False)
                site2_str = str(site2.url)
                # print site2_str 
                if site2_str.find(keyword) > -1:
                    trueURL_t.add(site2_str)
            else:
                break;
        except:
            break;
    return trueURL_t;

#从百度加密链接中提取真实链接v2
def getTrueURL_2(trueURL,keyword):
    if keyword.count('.') > 1:
        keyword = keyword[keyword.find('.')+1:]
    print "getTrueURL --  keyword 为："+keyword;
    # 获取真实链接 
    for url in trueURL:
        try:
            site2 = requests.get(url, timeout=3)
            site2_str = str(site2.url)
            # print site2_str 
            if site2_str.find(keyword) > -1:
                g_TrueURL.add(site2_str)
                print site2_str;#有问题，改为全局变量
        except:
            pass;

#初始化本地文件
def initialize():
    # 读取查询URL与关键词
    try:
        site = open("./sites.txt", "r");
        sites = site.readlines();
        keyword = open("./keyword.txt", "r");
        keywords = keyword.readlines();
        site.close();
        keyword.close();
    except:
        print "initialize error\n";
        exit(0);
    return sites,keywords;

#生成搜索关键词
def processKeyword():
    result=set();
    i=0;
    while True:
        try:
            kw = keywords.pop().replace("\r\n","").replace("\n","");
        except:
            break;
        for site in sites:
            try:
                p =  site.replace("\r\n", "").replace("\n", "") + " " +kw;
                result.add(p);
                i=i+1;
            except:
                pass;
    print "一共生成："+str(i)+"条搜索词";
    return result;

#线程处理函数
def printBaidu():
    while True:
        try:
            tKeyword = searchKw.pop();
        except:
            break;
        try:
            #print "正在处理第" + str(num) + "条搜索词";
            t_burls = getBaiduURL(tKeyword);
            print t_burls;
            getTrueURL_2(t_burls,tKeyword[0:tKeyword.find(" ")]);
        except:
            pass
            #if len(t_burls2)>0:
            #    for i in t_burls2:
            #        print i;



#全局真实链接变量
g_TrueURL = set();

#初始化本地文件
sites,keywords=initialize();

#生成搜索词
searchKw=set();
searchKw = processKeyword();

#多线程
threads =[];
for trd in range(1,10):
	threads.append(threading.Thread(target=printBaidu));

# 启动所有线程
for t in threads:
	t.start()
#主线程中等待所有子线程退出
for t in threads:
	t.join()

print "main end\n";

#写入结果
fo = open("./spiderSite.txt","a+");

for jj in g_TrueURL:
	fo.write(jj+"\n");
fo.flush();
fo.close();
print g_TrueURL;

