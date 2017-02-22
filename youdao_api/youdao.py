import json
from urllib import parse
from urllib import request
import codecs


def youdao(word):

    if type(word).__name__ == "unicode":
        word = word.encode('UTF-8')

    quote_word = parse.quote(word)
    base_url = r'http://fanyi.youdao.com/openapi.do?keyfrom=aingNZ&key=1417591443&type=data&doctype=json&version=1.1&q='
    url = base_url + quote_word
    response = request.urlopen(url)
    reader = codecs.getreader('utf-8')
    result = json.load(reader(response))
    error_code = result['errorCode']
    if error_code == 0:
        if 'basic' in result.keys():
            trans = u'%s:\n%s\n%s\n网络释义：\n%s' % \
                    (result['query'], ''.join(result['translation']), ' '.join(result['basic']['explains']), ''.join(result['web'][0]['value']))
            return trans
        else:
            trans = u'%s:\n基本翻译:%s\n' % (result['query'], ''.join(result['translation']))
            return trans
    elif error_code == 20:
        return u'对不起，要翻译的文本过长'
    elif error_code == 30:
        return u'对不起，无法进行有效的翻译'
    elif error_code == 40:
        return u'对不起，不支持的语言类型'
    else:
        return u'对不起，您输入的单词"%s"无法翻译,请检查拼写' % word

