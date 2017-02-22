from rest_framework.decorators import api_view
from we_robot.models import Mode
from rest_framework.response import Response
from we_robot.serializers import ModeSerializer


@api_view(['GET', 'POST'])
def modes(request):
    if request.method == 'GET':
        all_modes = Mode.objects.all()
        serializer = ModeSerializer(all_modes, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print(request.data)
        user_id = request.data['user']
        user, created = Mode.objects.get_or_create(user=user_id)
        if created:
            return Response("New User %s is created." % user.user)
        else:
            return Response("Find the existing user %s" % user.user)
