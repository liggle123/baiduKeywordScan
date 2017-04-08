本程序可以通过百度搜索关键词，批量获取对应链接。

扫描需要同目录下的两个文件，keyword.txt，sites.txt。

keyword.txt里面存放关键词，一行一个，例如”身份证”、”.action”、”admin”等，中英文都可以，但是文件编码最好使用UTF-8。
sites.txt里面存放域名，一行一个，不包含协议头（http,https等，直接放域名，例如www.baidu.com）。

原理：通过百度搜索   “site:www.baidu.com 身份证”   批量抓取搜索到的内容。然后再进行其它处理。

结果输出：扫描结果回保存到程序同目录下的spiderSite.txt。

注意：测试过程发现一个IP多次进行百度搜索时，百度会提示输入验证码，所以做好使用阿里云等VPS进行扫描。