import requests
import re
import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view


logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def tuling_api(request):
    if request.method == 'POST':
        return Response(tuling_robot(request.data['user_id'], request.data['message']))
    elif request.method == 'GET':
        return Response('GET is not supported.')


def tuling_robot(user_id, message):
    api_url = r'http://www.tuling123.com/openapi/api'
    escaped_user_id = re.sub(r'[^a-zA-Z0-9]', '', user_id)
    payload = r'{"key": "4424be4bf32c45ad805812875dbc3f08", "info": "%s", "userid": "%s"}' % (message, escaped_user_id)
    logger.debug('Calling Tuling API with the payload: %s' % payload)
    r = requests.post(api_url, data=payload.encode('UTF-8'))
    json_r = r.json()

    if json_r['code'] == 100000:
        return json_r['text']

