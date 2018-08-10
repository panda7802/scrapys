# coding=utf-8
lxdzx_bili_show_list = [('title', '标题'),
                        ('created', '创建时间'),
                        ('play', '播放量'),
                        ('comment', '评论数'),
                        ('video_review', '弹幕数'),
                        ('favorites', '收藏量'),
                        ('length', '长度'),
                        ('author', '作者'),
                        ('review', '回顾'),
                        ('typeid', '类型'),
                        ('pic', '图片'),
                        ('subtitle', '子标题'),
                        ('description', '描述'),
                        ('aid', '详细信息id'),
                        ('mid', '当前id'),
                        ('copyright', '版权'),
                        ('hide_click', '不可点击')]

BASE_COOKIES = {'a': 'b'}

BASE_HEAD = {
    # 'Host': 'comment.bilibili.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}




# BASE_HEAD = {
#     'Host': 'space.bilibili.com',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
#     'Accept-Encoding': 'gzip, deflate',
#     'Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1',
#     'Cache-Control': 'max-age=0',
# }
