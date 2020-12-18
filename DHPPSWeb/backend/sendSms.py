# !/usr/bin/env python
# coding=utf-8
from random import randint
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
client = AcsClient('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')


def SendSms(iPhonenum):
    ranInt = randint(100000, 999999)
    sendString = '{\"code\":\"'+str(ranInt)+'\"}'
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('TemplateCode', "SMS_204111380")
    request.add_query_param('PhoneNumbers', iPhonenum)
    request.add_query_param('SignName', "请填写")
    request.add_query_param('TemplateParam', sendString)

    response = client.do_action(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))
    return str(ranInt), response["message"], response["Code"]
