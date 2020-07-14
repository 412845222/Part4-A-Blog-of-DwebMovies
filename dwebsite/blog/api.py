from rest_framework.response import Response
from rest_framework.decorators import api_view



@api_view(['POST'])
def add_article(request):
  return Response('ok')