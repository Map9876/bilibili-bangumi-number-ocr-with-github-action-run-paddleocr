# bilibili-bangumi-number-ocr-with-github-action-run-paddleocr
paddleocr 运行在github action上，自动每天识别bilibili号，通过识别ogv视频的前十秒的右下角小矩形框内的数字，来记录。

https://github.com/SocialSisterYi/bilibili-API-collect/issues/1136
中国手机版指定用户投稿视频列表获取API（无需鉴权） #1136

https://app.bilibili.com/x/v2/space/archive/cursor?vmid=928123

https://app.bilibili.com/x/v2/space/archive/cursor?vmid=928123
输入用户uid，获取视频列表如下


```json
{"code":0,"message":"0","ttl":1,"data":{"episodic_button":{"text":"播放全部","uri":"bilibili://music/playlist/spacepage/928123?desc=1\u0026offset=0\u0026oid=0\u0026order=time\u0026page_type=1\u0026playlist_intro=UP%E4%B8%BB%E7%9A%84%E5%85%A8%E9%83%A8%E8%A7%86%E9%A2%91\u0026ps=20\u0026sort_field=1\u0026total_count=24438\u0026user_name=%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%E7%95%AA%E5%89%A7"},"order":[{"title":"最新发布","value":"pubdate"},{"title":"最多播放","value":"click"}],"count":24438,"item":[{"title":"虫王战队超王者（中配）49","subtitle":"","tname":"连载动画","cover":"http://i2.hdslb.com/bfs/archive/625f310abfa1729140e7af3f948e0d06cd284a27.png","cover_icon":"","uri":"https://www.bilibili.com/bangumi/play/ep1191813","param":"113718000092993","goto":"av","length":"","duration":1360,"is_popular":false,"is_steins":false,"is_ugcpay":false,"is_cooperation":false,"is_pgc":true,"is_live_playback":false,"is_pugv":false,"is_fold":false,"is_oneself":false,"play":6527,"danmaku":22,"ctime":1735439401,"ugc_pay":0,"author":"哔哩哔哩番剧","state":false,"bvid":"BV1JxC6Y8EP5","videos":1,"three_point":[{"type":"addtoview","icon":"https://i0.hdslb.com/bfs/app/25cc01346574a601dafd45c94226d92a67eed79a.png","text":"添加至稍后再看"},{"type":"share","icon":"https://i0.hdslb.com/bfs/app/a5787f586c72f2d6f6ade4b33c64908938c4a01f.png","text":"分享","share_succ_toast":"分享成功","share_fail_toast":"分享失败","share_path":"pages/video/video?avid=113718000092993","short_link":"https://b23.tv/BV1JxC6Y8EP5"}],"first_cid":27540588592,"cursor_attr":{"is_last_watched_arc":false,"rank":0},"view_content":"6527","icon_type":0,"publish_time_text":"22小时前"},{"title":"虫王战队超王者 49","subtitle":"","tname":"连载动画","cover":"http://i0.hdslb.com/bfs/archive/1cc80c7adc8bfb1e72fcd2a71724f2ee54c1291b.png","cover_icon":"","uri":"https://www.bilibili.com/bangumi/play/ep1191808","param":"113718000093502","goto":"av","length":"","duration":1351,"is_popular":false,"is_steins":false,"is_ugcpay":false,"is_cooperation":false,"is_pgc":true,"is_live_playback":false,"is_pugv":false,"is_fold":false,"is_oneself":false,"play":45124,"danmaku":994,"ctime":1735439400,"ugc_pay":0,"author":"哔哩哔哩番剧","state":false,"bvid":"BV1ExC6Y8EBA
.......省略
```

获取所有的bvid值，以及每个对应的title值，

获取每个bvid值比如BV1JxC6Y8EP5 之后，去访问他，并且跟随重定向，最终跳转到 
类似于 curl -Ls -w %{url_effective} https://b23.tv/BV1JxC6Y8EP5
https://www.bilibili.com/video/BV1JxC6Y8EP5
这个还不是浏览器显示的epid那种链接
搜索 获取应用最终跳转
https://www.youdiandongxi.com/article/smzdm-php-catch.html获取 什么值得买 跳转链接的方法
里说，这个就只是header里面location的链接

```
.../emulated/0 $ curl -L  https://b23.tv/BV1JxC6Y8EP5 -I
HTTP/2 302
date: Mon, 30 Dec 2024 01:07:41 GMT
content-type: text/html; charset=utf-8
bili-trace-id: 53c08c16806771f2
location: https://www.bilibili.com/video/BV1JxC6Y8EP5
x-bili-trace-id: 545cbdfbd8c1980653c08c16806771f2
expires: Mon, 30 Dec 2024 01:07:40 GMT
cache-control: no-cache
x-cache-webcdn: BYPASS from blzone02

HTTP/2 200
date: Mon, 30 Dec 2024 01:07:41 GMT
content-type: text/html; charset=utf-8
set-cookie: buvid3=93484282-E46B-480A-D267-24324523247661391infoc; path=/; expires=Sun, 26 Sep 2027 01:07:41 GMT; domain=.bilibili.com
set-cookie: b_nut=1735520861; path=/; expires=Tue, 30 Dec 2025 01:07:41 GMT; domain=.bilibili.com
vary: Origin,Accept-Encoding
content-encoding: gzip
x-cache-webcdn: BYPASS from blzone02

.../emulated/0 $
```



```python
import requests

def request_jd():
    url = 'https://www.bilibili.com/video/BV1JxC6Y8EP5/'
    #allow_redirects= False 这里设置不允许跳转
    response = requests.get(url=url, allow_redirects=False)
    print(response.headers)
    print(response.status_code)
request_jd()    
```


——————————————————————————————————————————

```python
import requests
def get_permanent_link(url):
    # 使用requests库发送head请求（也可以选择GET，但HEAD更快且消耗资源更少）
    response = requests.head(url, allow_redirects=True)
    # print(response.headers)
    # 检查是否有重定向发生
    if 'location' in response.headers:
        # 如果响应头中包含'location'，则表示发生了重定向
        # 递归调用自身以处理连续重定向的情况
        return get_permanent_link(response.headers['location'])
    else:
        # 如果没有重定向，则返回当前请求的URL作为永久链接
        return response.url
# 测试函数
temporary_link = "https://b23.tv/BV1JxC6Y8EP5"
permanent_link = get_permanent_link(temporary_link)
print("永久链接是:", permanent_link)
#搜 。b23.tv重定向  https://blog.csdn.net/knighthood2001/article/details/139382420```
浏览器看f12，html加载了下面几个:

https://b23.tv/BV1JxC6Y8EP5到 https://bilibili.com/video/BV1JxC6Y8EP5
到 https://m.bilibili.com/video/BV1JxC6Y8EP5到https://www.bilibili.com/bangumi/play/ep1191813到https://m.bilibili.com/bangumi/play/ep1191813

```
直接用curl -L https://m.bilibili.com/video/BV1JxC6Y8EP5  -I不行，手机浏览器f12复制出来以curl复制

```
curl 'https://m.bilibili.com/video/BV1JxC6Y8EP5' \
  -H 'authority: m.bilibili.com' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'cookie: buvid3=5564B54E-5813-A348-4AC8-45AC50AA8D8A61860infoc; b_nut=1735519061; bg_view_47246=1191813; _uuid=2BD89BBB-B9C8-4444-99CB-9DBDB88DE5CF61974infoc; buvid_fp=9cc10382255c6da3ec2b7d607a825b25; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzU3Nzk2OTIsImlhdCI6MTczNTUyMDQzMiwicGx0IjotMX0.0ItunAwLqk1T7KX9kzjZgkkVMBSS1gYjSyy6cwefG3c; bili_ticket_expires=1735779632; rpdid=0zbfAHVMFb|9ZNUpxIj|b4G|3w1Ts4a4; buvid4=C1733CD5-AB98-AC6D-B9DB-E97522A0861263078-124123000-hRvmAMS8bju0xRpPKpAufE1YMNgofzBa4g0hCKaaQvmsprKR8Dm%2B%2BBhH7ZqeQbXO; b_lsid=108399569_194152760EF; sid=ozpa14oh' \
  -H 'sec-ch-ua: "Not-A.Brand";v="99", "Chromium";v="124"' \
  -H 'sec-ch-ua-mobile: ?1' \
  -H 'sec-ch-ua-platform: "Android"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: none' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36' \
  --compressed
  
```
然后把手机user agent加进去，也就是
curl -L https://m.bilibili.com/video/BV1JxC6Y8EP5 -I -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36' \


获取每个bvid值比如BV1JxC6Y8EP5 之后 ，构造链接为
https://m.bilibili.com/video/BV1JxC6Y8EP5  这种格式 然后去使用 -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'  获取最终链接https://m.bilibili.com/bangumi/play/ep1191813 然后获取ep后面的数字id
最后使用api链接 https://api.bilibili.com/pgc/player/web/playurl/html5?ep_id=1191813&bsource=
得到
{"code":0,"message":"success","result":{"accept_format":"mp4,mp4,mp4,mp4,mp4","code":0,"durl":[{"size":6389468,"ahead":"","length":180179,"vhead":"","backup_url":[],"url":"https://cn-gddg-cm-01-05.bilivideo.com/upgcxcode/92/85/27540588592/27540588592-1-400.mp4?e=ig8euxZM2rNcNbRVhwdVhwdlhWdVhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1735526358&gen=playurlv2&os=bcache&oi=0&trid=0000a9cb5831dbfb4621be15baf93b1ae560p&mid=0&platform=html5&og=cos&upsig=f38297dc49d2b5417c32bf50450972f8&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&cdnid=2125&bvc=vod&nettype=0&orderid=0,1&buvid=5564B54E-5813-A348-4AC8-45AC50AA8D8A61860infoc&build=0&f=p_0_0&bw=35497&logo=80000000","order":1,"md5":""}],"seek_param":"start","is_preview":1,"no_rexcode":

获取其中的url进行下载

https://curlconverter.com/
转
curl -L https://m.bilibili.com/video/BV1JxC6Y8EP5  -I -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36' \格式为

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

#然后填进去headers=headers,

```
import requests
def get_permanent_link(url):
    # 使用requests库发送head请求（也可以选择GET，但HEAD更快且消耗资源更少）
    response = requests.head(url, headers=headers, allow_redirects=True)
    # print(response.headers)
    # 检查是否有重定向发生
    if 'location' in response.headers:
        # 如果响应头中包含'location'，则表示发生了重定向
        # 递归调用自身以处理连续重定向的情况
        return get_permanent_link(response.headers['location'])
    else:
        # 如果没有重定向，则返回当前请求的URL作为永久链接
        return response.url
# 测试函数
temporary_link = "https://b23.tv/BV1JxC6Y8EP5"
permanent_link = get_permanent_link(temporary_link)
print("永久链接是:", permanent_link)
```

——————————————————————
https://app.bilibili.com/x/v2/space/archive/cursor?vmid=928123
定时每天使用这个api链接，获取视频列表如下

{"code":0,"message":"0","ttl":1,"data":{"episodic_button":{"text":"播放全部","uri":"bilibili://music/playlist/spacepage/928123?desc=1\u0026offset=0\u0026oid=0\u0026order=time\u0026page_type=1\u0026playlist_intro=UP%E4%B8%BB%E7%9A%84%E5%85%A8%E9%83%A8%E8%A7%86%E9%A2%91\u0026ps=20\u0026sort_field=1\u0026total_count=24438\u0026user_name=%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%E7%95%AA%E5%89%A7"},"order":[{"title":"最新发布","value":"pubdate"},{"title":"最多播放","value":"click"}],"count":24438,"item":[{"title":"虫王战队超王者（中配）49","subtitle":"","tname":"连载动画","cover":"http://i2.hdslb.com/bfs/archive/625f310abfa1729140e7af3f948e0d06cd284a27.png","cover_icon":"","uri":"https://www.bilibili.com/bangumi/play/ep1191813","param":"113718000092993","goto":"av","length":"","duration":1360,"is_popular":false,"is_steins":false,"is_ugcpay":false,"is_cooperation":false,"is_pgc":true,"is_live_playback":false,"is_pugv":false,"is_fold":false,"is_oneself":false,"play":6527,"danmaku":22,"ctime":1735439401,"ugc_pay":0,"author":"哔哩哔哩番剧","state":false,"bvid":"BV1JxC6Y8EP5","videos":1,"three_point":[{"type":"addtoview","icon":"https://i0.hdslb.com/bfs/app/25cc01346574a601dafd45c94226d92a67eed79a.png","text":"添加至稍后再看"},{"type":"share","icon":"https://i0.hdslb.com/bfs/app/a5787f586c72f2d6f6ade4b33c64908938c4a01f.png","text":"分享","share_succ_toast":"分享成功","share_fail_toast":"分享失败","share_path":"pages/video/video?avid=113718000092993","short_link":"https://b23.tv/BV1JxC6Y8EP5"}],"first_cid":27540588592,"cursor_attr":{"is_last_watched_arc":false,"rank":0},"view_content":"6527","icon_type":0,"publish_time_text":"22小时前"},{"title":"虫王战队超王者 49","subtitle":"","tname":"连载动画","cover":"http://i0.hdslb.com/bfs/archive/1cc80c7adc8bfb1e72fcd2a71724f2ee54c1291b.png","cover_icon":"","uri":"https://www.bilibili.com/bangumi/play/ep1191808","param":"113718000093502","goto":"av","length":"","duration":1351,"is_popular":false,"is_steins":false,"is_ugcpay":false,"is_cooperation":false,"is_pgc":true,"is_live_playback":false,"is_pugv":false,"is_fold":false,"is_oneself":false,"play":45124,"danmaku":994,"ctime":1735439400,"ugc_pay":0,"author":"哔哩哔哩番剧","state":false,"bvid":"BV1ExC6Y8EBA
.......省略


获取所有的bvid值，以及每个对应的title值，构造链接为
https://m.bilibili.com/video/BV1JxC6Y8EP5然后使用

```

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

#然后填进去headers=headers,
import requests
def get_permanent_link(url):
    # 使用requests库发送head请求（也可以选择GET，但HEAD更快且消耗资源更少）
    response = requests.head(url, headers=headers, allow_redirects=True)
    # print(response.headers)
    # 检查是否有重定向发生
    if 'location' in response.headers:
        # 如果响应头中包含'location'，则表示发生了重定向
        # 递归调用自身以处理连续重定向的情况
        return get_permanent_link(response.headers['location'])
    else:
        # 如果没有重定向，则返回当前请求的URL作为永久链接
        return response.url
# 测试函数
temporary_link = "https://m.bilibili.com/video/BV1JxC6Y8EP5"
permanent_link = get_permanent_link(temporary_link)
print("永久链接是:", permanent_link)

```

获取到跳转链接permanent_link为https://m.bilibili.com/bangumi/play/ep1191813 之后
然后获取ep后面的数字id
最后使用api链接 https://api.bilibili.com/pgc/player/web/playurl/html5?ep_id=1191813&bsource=
得到
{"code":0,"message":"success","result":{"accept_format":"mp4,mp4,mp4,mp4,mp4","code":0,"durl":[{"size":6389468,"ahead":"","length":180179,"vhead":"","backup_url":[],"url":"https://cn-gddg-cm-01-05.bilivideo.com/upgcxcode/92/85/27540588592/27540588592-1-400.mp4?e=ig8euxZM2rNcNbRVhwdVhwdlhWdVhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1735526358&gen=playurlv2&os=bcache&oi=0&trid=0000a9cb5831dbfb4621be15baf93b1ae560p&mid=0&platform=html5&og=cos&upsig=f38297dc49d2b5417c32bf50450972f8&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&cdnid=2125&bvc=vod&nettype=0&orderid=0,1&buvid=5564B54E-5813-A348-4AC8-45AC50AA8D8A61860infoc&build=0&f=p_0_0&bw=35497&logo=80000000","order":1,"md5":""}],"seek_param":"start","is_preview":1,"no_rexcode":

获取其中的视频url进行下载
https://github.com/copilot/c/9499a8c7-711a-4943-8528-741d265ae034


# 完整流程:

获取视频列表并下载视频的Python脚本
https://app.bilibili.com/x/v2/space/archive/cursor?vmid=928123
定时每天使用这个api链接，获取视频列表如下

```
{"code":0,"message":"0","ttl":1,"data":{"episodic_button":{"text":"播放全部","uri":"bilibili://music/playlist/spacepage/928123?desc=1\u0026offset=0\u0026oid=0\u0026order=time\u0026page_type=1\u0026playlist_intro=UP%E4%B8%BB%E7%9A%84%E5%85%A8%E9%83%A8%E8%A7%86%E9%A2%91\u0026ps=20\u0026sort_field=1\u0026total_count=24438\u0026user_name=%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%E7%95%AA%E5%89%A7"},"order":[{"title":"最新发布","value":"pubdate"},{"title":"最多播放","value":"click"}],"count":24438,"item":[{"title":"虫王战队超王者（中配）49","subtitle":"","tname":"连载动画","cover":"http://i2.hdslb.com/bfs/archive/625f310abfa1729140e7af3f948e0d06cd284a27.png","cover_icon":"","uri":"https://www.bilibili.com/bangumi/play/ep1191813","param":"113718000092993","goto":"av","length":"","duration":1360,"is_popular":false,"is_steins":false,"is_ugcpay":false,"is_cooperation":false,"is_pgc":true,"is_live_playback":false,"is_pugv":false,"is_fold":false,"is_oneself":false,"play":6527,"danmaku":22,"ctime":1735439401,"ugc_pay":0,"author":"哔哩哔哩番剧","state":false,"bvid":"BV1JxC6Y8EP5","videos":1,"three_point":[{"type":"addtoview","icon":"https://i0.hdslb.com/bfs/app/25cc01346574a601dafd45c94226d92a67eed79a.png","text":"添加至稍后再看"},{"type":"share","icon":"https://i0.hdslb.com/bfs/app/a5787f586c72f2d6f6ade4b33c64908938c4a01f.png","text":"分享","share_succ_toast":"分享成功","share_fail_toast":"分享失败","share_path":"pages/video/video?avid=113718000092993","short_link":"https://b23.tv/BV1JxC6Y8EP5"}],"first_cid":27540588592,"cursor_attr":{"is_last_watched_arc":false,"rank":0},"view_content":"6527","icon_type":0,"publish_time_text":"22小时前"},{"title":"虫王战队超王者 49","subtitle":"","tname":"连载动画","cover":"http://i0.hdslb.com/bfs/archive/1cc80c7adc8bfb1e72fcd2a71724f2ee54c1291b.png","cover_icon":"","uri":"https://www.bilibili.com/bangumi/play/ep1191808","param":"113718000093502","goto":"av","length":"","duration":1351,"is_popular":false,"is_steins":false,"is_ugcpay":false,"is_cooperation":false,"is_pgc":true,"is_live_playback":false,"is_pugv":false,"is_fold":false,"is_oneself":false,"play":45124,"danmaku":994,"ctime":1735439400,"ugc_pay":0,"author":"哔哩哔哩番剧","state":false,"bvid":"BV1ExC6Y8EBA
.......省略
```

获取所有的bvid值，以及每个对应的title值，构造链接为
https://m.bilibili.com/video/BV1JxC6Y8EP5然后使用

```

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

#然后填进去headers=headers,
import requests
def get_permanent_link(url):
    # 使用requests库发送head请求（也可以选择GET，但HEAD更快且消耗资源更少）
    response = requests.head(url, headers=headers, allow_redirects=True)
    # print(response.headers)
    # 检查是否有重定向发生
    if 'location' in response.headers:
        # 如果响应头中包含'location'，则表示发生了重定向
        # 递归调用自身以处理连续重定向的情况
        return get_permanent_link(response.headers['location'])
    else:
        # 如果没有重定向，则返回当前请求的URL作为永久链接
        return response.url
# 测试函数
temporary_link = "https://m.bilibili.com/video/BV1JxC6Y8EP5"
permanent_link = get_permanent_link(temporary_link)
print("永久链接是:", permanent_link)

```

获取到跳转链接permanent_link为https://m.bilibili.com/bangumi/play/ep1191813 之后
然后获取ep后面的数字id
最后使用api链接 https://api.bilibili.com/pgc/player/web/playurl/html5?ep_id=1191813&bsource=
得到

```
{"code":0,"message":"success","result":{"accept_format":"mp4,mp4,mp4,mp4,mp4","code":0,"durl":[{"size":6389468,"ahead":"","length":180179,"vhead":"","backup_url":[],"url":"https://cn-gddg-cm-01-05.bilivideo.com/upgcxcode/92/85/27540588592/27540588592-1-400.mp4?e=ig8euxZM2rNcNbRVhwdVhwdlhWdVhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1735526358&gen=playurlv2&os=bcache&oi=0&trid=0000a9cb5831dbfb4621be15baf93b1ae560p&mid=0&platform=html5&og=cos&upsig=f38297dc49d2b5417c32bf50450972f8&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&cdnid=2125&bvc=vod&nettype=0&orderid=0,1&buvid=5564B54E-5813-A348-4AC8-45AC50AA8D8A61860infoc&build=0&f=p_0_0&bw=35497&logo=80000000","order":1,"md5":""}],"seek_param":"start","is_preview":1,"no_rexcode":
```

获取其中的视频url进行下载

# 完整代码: 
```
import requests
import time
import json
from datetime import datetime

# Headers for requests
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

# Function to get video list
def get_video_list(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch video list: {response.status_code}")

# Function to get permanent link
def get_permanent_link(url):
    response = requests.head(url, headers=headers, allow_redirects=True)
    if 'location' in response.headers:
        return get_permanent_link(response.headers['location'])
    else:
        return response.url

# Function to get video download url using ep_id
def get_video_download_link(ep_id):
    api_url = f"https://api.bilibili.com/pgc/player/web/playurl/html5?ep_id={ep_id}&bsource="
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0 and 'result' in data:
            return data['result']['durl'][0]['url']
        else:
            raise Exception(f"Failed to fetch video download link: {data['message']}")
    else:
        raise Exception(f"Failed to fetch video download link: {response.status_code}")

# Function to download video
def download_video(url, filename):
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded {filename}")
    else:
        raise Exception(f"Failed to download video: {response.status_code}")

def main():
    video_list_url = "https://app.bilibili.com/x/v2/space/archive/cursor?vmid=928123"
    video_data = get_video_list(video_list_url)
    items = video_data['data']['item']

    for item in items:
        bvid = item['bvid']
        title = item['title']
        temporary_link = f"https://m.bilibili.com/video/{bvid}"
        
        # Get permanent link
        permanent_link = get_permanent_link(temporary_link)
        
        # Extract ep_id from permanent link
        ep_id = permanent_link.split('ep')[-1]
        
        # Get video download link
        video_download_url = get_video_download_link(ep_id)
        
        # Download video
        filename = f"{title}.mp4"
        download_video(video_download_url, filename)

# Set the time to run the script every day (e.g., at midnight)
main()
"""
while True:
    current_time = datetime.now().strftime("%H:%M:%S")
    if current_time == "00:00:00":
        main()
        time.sleep(86400)  # Sleep for one day
    time.sleep(1)
"""
    
```
