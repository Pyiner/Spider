# Spider #
编程语言：Python

功能：爬取网站资源

例如：http://www.hao123.com/

网站的资源：a标签，img标签，css文件、js文件，iframe标签

限制：

- 只爬取xxx.hao123.com下的资源，不包括外站的资源
- 可以设置爬取资源的上限，比如，设置1个参数max_size=1000，爬到1000个时候就终止爬虫
- 实现了线程池
- 以log日志记录爬取的资源链接

调用方式：
	
	python spider.py --site http://www.hao123.com/ --max_size 1000
