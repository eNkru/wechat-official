from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import re
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def get_post_details(request, pk, format=None):
    logger.debug('Get the trace info for %s' % pk)
    if request.method == 'GET':
        return Response(trace_post(pk))


def trace_post(trace_number):
    trace_number_lower = trace_number.lower()

    # validate the trace number.
    pattern_ftd = re.compile('^nz[0-9]{7}$')
    pattern_ydt = re.compile('^zy[0-9]{9}nz$')
    pattern_cg = re.compile('^[0-9]{12}$')

    if pattern_ftd.match(trace_number_lower):
        return get_ftd(trace_number_lower)
    elif pattern_ydt.match(trace_number_lower):
        return get_ydt(trace_number_lower)
    elif pattern_cg.match(trace_number_lower):
        return get_cg(trace_number_lower)
    else:
        return u'''目前只支持傅腾达|易达通快递。
请输入正确的快递单号。'''


def trace_post_number_only(trace_number):
    return trace_post(trace_number)


def get_ydt(trace_number):
    base_url = r'http://www.qexpress.co.nz/tracking.aspx?orderNumber='
    query_url = base_url + trace_number
    r = requests.get(query_url)
    result_pattern = re.compile('<table width="670" class="list".*?>(.*?)</table>', re.S)
    result = result_pattern.search(r.text)
    details_pattern = re.compile('<td>(.*?)</td>|<td height="25">(.*?)</td>', re.S)
    items = re.findall(details_pattern, result.group())

    items_list = []
    for item in items:
        items_list.extend(item)

    striped_items = map(str.strip, filter(None, items_list))

    final_string = u'易达通单号：%s' % trace_number + '\n\n'
    for item in striped_items:
        final_string += item.replace("&nbsp", "").replace(";", "\n")

    return final_string


def get_ftd(trace_number):
    base_url = r'http://www.ftd.nz'
    query_url = base_url + '/query/'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    headers = {'User-Agent': user_agent}
    payload = {'codes': trace_number}
    r = requests.post(query_url, data=payload, headers=headers)

    pattern = re.compile(
        '的查询结果</p>(.*?)<div id="pRight">',
        re.S)

    match = pattern.search(r.text)

    if match:
        matched_group = match.group()
        result_pattern = re.compile('<p>(.*?)</p>', re.S)
        items = re.findall(result_pattern, matched_group)

        link_pattern = re.compile('<script.*?src="(.*?)"></script>', re.S)
        links = re.findall(link_pattern, matched_group)
        if links:
            # get additional trace info in China.
            additional_query_url = base_url + links[0]
            additional_r = requests.get(additional_query_url, headers=headers, cookies=r.cookies)
            additional_items = re.findall(result_pattern, additional_r.text)
            items.extend(additional_items)

        return u'富腾达单号：%s' % trace_number + '\n\n' + '\n\n'.join(item for item in items)
    else:
        return u'您所提供的傅腾达单号「%s」还未录入系统，请您稍后再查。' % trace_number


def get_cg(trace_number):
    base_url = r'http://www.flywayex.com/cgi-bin/GInfo.dll?EmmisTrack'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    headers = {'User-Agent': user_agent}
    payload = {'cno': trace_number}
    r = requests.post(base_url, data=payload, headers=headers)

    pattern = re.compile(
        '<tr align=.*?<td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td>.*?</tr>',
        re.S
    )
    items = re.findall(pattern, r.text)

    result = u'程光单号：%s\n' % trace_number
    for item in items:
        result += '\n\n%s\n%s' % (item[0], item[2])

    return result
