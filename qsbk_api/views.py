from rest_framework.views import APIView
from rest_framework.response import Response
import re
import requests
from qsbk_api.models import Joke
from random import choice
from random import randint


class TestView(APIView):

    def get(self, request, format=None):
        return Response(self.get_joke()['content'])

    def get_joke(self):
        all_url = 'http://www.qiushibaike.com/hot/page/' + str(randint(1, 35)) + '/'
        start_html = requests.get(all_url)

        pattern = re.compile(
            '<div.*?author clearfix">.*?<h2>(.*?)</h2>.*?<div.*?content">.*?<span>(.*?)</span>(.*?)<i.*?class="number">(.*?)</i>',
            re.S)

        items = re.findall(pattern, start_html.text)
        response = []
        for item in items:
            contain_image = re.search("thumb", item[2])
            if not contain_image:
                response.append(Joke(
                    author=item[0].strip(' \t\n\r'), content=item[1].strip(' \t\n\r'), like=item[3].strip(' \t\n\r')))

        res_list = [ob.as_json() for ob in response]
        return choice(res_list)
