# coding=utf-8

# -*- coding: utf-8 -*-
from lib.commonlib.base_lib.network import http_request

"""
企业微信添加机器人方法：
1、已经存在讨论组或群
2、讨论组或群标签右键->添加群机器人->添加群机器人
3、点击新创建机器人->输入机器人名称（如：robot-test）->添加机器人

robot-testBOT
Webhook地址： https://qyapi.weixin.qq.com/cg...c6-8e29-1c7c781ff89f复制重置
推送消息示例机器人配置说明 推送消息配置
如何使用群机器人

在终端某个群组添加机器人之后，可以获取到webhook地址，然后开发者用户按以下说明构造post data向这个地址发起HTTP POST 请求，即可实现给该群组发送消息。下面举个简单的例子.
假设webhook是：https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=633a31f6-7f9c-4bc4-97a0-0ec1eefa589
特别特别要注意：一定要保护好机器人的webhook地址，避免泄漏！不要分享到github、博客等可被公开查阅的地方，否则坏人就可以用你的机器人来发垃圾消息了。
以下是用curl工具往群组推送文本消息的示例（注意要将url替换成你的机器人webhook地址，content必须是utf8编码）：

curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=633a31f6-7f9c-4bc4-97a0-0ec1eefa5898' \
   -H 'Content-Type: application/json' \
   -d '
   {
        "msgtype": "text",
        "text": {
            "content": "hello world"
        }
   }'
当前自定义机器人支持文本（text）、markdown（markdown）两种消息类型。
消息类型及数据格式

文本类型

{
    "msgtype": "text",
    "text": {
        "content": "广州今日天气：29度，大部分多云，降雨概率：60%",
        "mentioned_list":["wangqing","@all"],
        "mentioned_mobile_list":["13800001111","@all"]
    }
}
参数	是否必填	说明
msgtype	是	消息类型，此时固定为text
content	是	文本内容，最长不超过2048个字节，必须是utf8编码
mentioned_list	否	userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list
mentioned_mobile_list	否	手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人


markdown类型

{
    "msgtype": "markdown",
    "markdown": {
        "content": "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。\n
         >类型:<font color=\"comment\">用户反馈</font> \n
         >普通用户反馈:<font color=\"comment\">117例</font> \n
         >VIP用户反馈:<font color=\"comment\">15例</font>"
    }
}
参数	是否必填	说明
msgtype	是	消息类型，此时固定为markdown
content	是	markdown内容，最长不超过4096个字节，必须是utf8编码


目前支持的markdown语法是如下的子集：

标题 （支持1至6级标题，注意#与文字中间要有空格）
# 标题一
## 标题二
### 标题三
#### 标题四
##### 标题五
###### 标题六
加粗
**bold**
链接
[这是一个链接](http://work.weixin.qq.com/api/doc)
行内代码段（暂不支持跨行）
`code`
引用
> 引用文字
字体颜色(只支持3种内置颜色)
<font color="info">绿色</font>
<font color="comment">灰色</font>
<font color="warning">橙红色</font>
图片类型

{
    "msgtype": "image",
    "image": {
        "base64": "DATA",
        "md5": "MD5"
    }
}
参数	是否必填	说明
msgtype	是	消息类型，此时固定为image
base64	是	图片内容的base64编码
md5	是	图片内容（base64编码前）的md5值
注：图片（base64编码前）最大不能超过2M，支持JPG,PNG格式


图文类型

{
    "msgtype": "news",
    "news": {
       "articles" : [
           {
               "title" : "中秋节礼品领取",
               "description" : "今年中秋节公司有豪礼相送",
               "url" : "URL",
               "picurl" : "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
           }
        ]
    }
}
参数	是否必填	说明
msgtype	是	消息类型，此时固定为news
articles	是	图文消息，一个图文消息支持1到8条图文
title	是	标题，不超过128个字节，超过会自动截断
description	否	描述，不超过512个字节，超过会自动截断
url	是	点击后跳转的链接。
picurl	否	图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。


消息发送频率限制

每个机器人发送的消息不能超过20条/分钟。
重置Webhook地址后，当前所有根据该地址进行的消息推送都将失效，请根据新的地址重新配置
确定取消

"""


class WeChatNotify(object):
    """
    代码示例::

        we_chat = WeChatNotify()
        we_chat.text_notify_by_markdown(
        "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=1011cde2-1ca4-40c6-8e29-1c7c781ff89f",
        "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。>类型:<font color=\"comment\">用户反馈</font> >普通用户反馈:<font color=\"comment\">117例</font> >VIP用户反馈:<font color=\"comment\">15例</font>")

    """

    def text_notify_simple(self, url, content, notify_user_list=None, notify_mobile_list=None):
        """
        发送文字信息到企业微信机器人。

        :param url: 添加企业微信机器人返回的url地址
        :param content: 要发送的文字信息
        :param notify_user_list: 要@的人，如["zhangsan",@all],@all表示@所有人
        :param notify_mobile_list:  要电话通知的人如["10086",@all],@all表示@所有人
        """
        if notify_mobile_list is None:
            notify_mobile_list = []
        if notify_user_list is None:
            notify_user_list = []
        msg = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": notify_user_list,
                "mentioned_mobile_list": notify_mobile_list
            }
        }
        self._we_chat_notify_do(url=url, msg=msg)

    def text_notify_by_markdown(self, url, content):
        """
        发送文字信息到企业微信机器人,文件信息以markdown格式优化显示。

        :param url: 添加企业微信机器人返回的url地址
        :param content: 要发送的文字信息  如：
                "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。\n
                 >类型:<font color=\"comment\">用户反馈</font> \n
                 >普通用户反馈:<font color=\"comment\">117例</font> \n
                 >VIP用户反馈:<font color=\"comment\">15例</font>"
        """

        msg = {
            "msgtype": "markdown",
            "markdown": {
                "content": content,
            }
        }
        self._we_chat_notify_do(url=url, msg=msg)

    @staticmethod
    def _we_chat_notify_do(url, msg):
        header = {'Content-Type': 'text/html'}
        result = http_request.post(url, data=msg, headers=header)
        result.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常


if __name__ == '__main__':
    aa = WeChatNotify()
    aa.text_notify_by_markdown(
        "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=1011cde2-1ca4-40c6-8e29-1c7c781ff89f",
        "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。\n>类型:<font color=\"comment\">用户反馈</font> \n>普通用户反馈:<font color=\"comment\">117例</font> \n>VIP用户反馈:<font color=\"comment\">15例</font>")
