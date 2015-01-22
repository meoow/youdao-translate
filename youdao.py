#!/usr/bin/env python2.7
#coding: utf8

import urllib, urllib2
import json
import copy

class YoudaoError(Exception):

	def __init__(self, error_code, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
		self.error_code = error_code

class Youdao(object):

	__QUERY_URL = 'http://fanyi.youdao.com/openapi.do?'

	__QUERY_PARAM = {
			"keyfrom" :  "",
			"key"     :  "",
			"type"    :  "data",
			"doctype" :  "json",
			"version" :  1.1,
			"only"    :  "", 
			"q"       :  ""
			}

	__ERROR_MSG = {
			20: "要翻译的文本过长", 
			30: "无法进行有效的翻译", 
			40: "不支持的语言类型", 
			50: "无效的key", 
			60: "无词典结果，仅在获取词典结果生效"
			}
	
	def __init__(self, token):

		self.param = copy.copy(self.__QUERY_PARAM)
		self.param['keyfrom'] = token[0]
		self.param['key'] = token[1]

		self.last_result = {}
	
	def translate(self, text, translate=True, dictionary=True):

		if text.strip() == "":
			return ''

		self.param['q'] = text

		_translate = 0
		_dictionary = 0
		
		if translate:
			_translate = 1
		if dictionary:
			_dictionary = 10

		if _translate | _dictionary == 0:
			raise TypeError('At least 1 of translate or dictionary must be set')
		else:
			self.param['only'] = {
					1 : 'translate', 
					10 : 'dict', 
					11 : ''} [ _translate | _dictionary ]

		resp = urllib2.urlopen(self.__QUERY_URL + \
				urllib.urlencode(self.param))
		
		result = json.loads(resp.read())

		if result['errorCode'] != 0:
			raise YoudaoError(
					result['errorCode'], 
					self.__ERROR_MSG.get(result['errorCode'], '未知错误')
					)

		self.last_result = result

		if _translate | _dictionary == 10:
			#return '\n'.join(result.get('basic', []))
			output = []
			if 'basic' in result:
				basic = result['basic']
				#if 'phonetic' in basic:
				#	output.append(u'[{}]'.format(basic['phonetic']))
				if 'us-phonetic' in basic:
					output.append(u'US [{}]'.format(basic['us-phonetic']))
				if 'uk-phonetic' in basic:
					output.append(u'UK [{}]'.format(basic['uk-phonetic']))
				if 'explains' in basic:
					output.extend(basic['explains'])
			return '\n'.join(output).encode('utf8')
		else:
			return '\n'.join(result.get('translation', []))

if __name__ == '__main__':
# Note the following code is for demonstration of usage only, 
# it will not work unless you replace "your_key_name" and "your_key_code"
# with your own ones.
# API key for youdao translate can be applied at 
# http://fanyi.youdao.com/openapi?path=data-mode
	youdao = Youdao(('your_key_name', 'your_key_code'))
	print youdao.translate('I am the god of war.')
	print youdao.translate('water', translate=False)
