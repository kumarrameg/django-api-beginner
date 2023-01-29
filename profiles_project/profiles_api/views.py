from django.shortcuts import render
from rest_framework import status,viewsets,filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from profiles_api import serializers,models,permissions

class HelloApiView(APIView):

  serializer_class=serializers.HelloSerializer

  def get(self,request,format=None):
    # This is fetch list of objects
    an_apiview=[
      'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
      'Lorem Ipsum has been the industrys standard dummy text ever since the 1500s,',
      'when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries.'
    ]
    return Response({'message':'Hello!','an_apiview':an_apiview})

  def post(self,requst):
    serializer=self.serializer_class(data=requst.data)

    if serializer.is_valid() :
      name=serializer.validated_data.get('name')
      message=f'Hello {name}'
      return Response({'message':message})
    else :
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

  def put(self,request,pk=None):
    serializer=self.serializer_class(data=request.data)

    if serializer.is_valid():
      name=serializer.validated_data.get('name')
      message=f'Hello {name} This is put'
      return Response({'method':message})
    else:
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

  def patch(self,request,pk=None):
      return Response({'method':'This is patch'})

  def delete(self,request,pk=None):
      return Response({'method':'This is delete'})
  

class HelloViewSet(viewsets.ViewSet):

  serializer_class=serializers.HelloSerializer
  
  def list(self,request):
    an_apiview=[
      'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
      'Lorem Ipsum has been the industrys standard dummy text ever since the 1500s,',
      'when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries.'
    ]
    return Response({'message':'Hello!','an_apiview':an_apiview})

  def create(self,requst):
    serializer=self.serializer_class(data=requst.data)

    if serializer.is_valid() :
      name=serializer.validated_data.get('name')
      message=f'Hello {name}'
      return Response({'message':message})
    else :
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

  def retrieve(self,request,pk=None):    
      return Response({'method':'this is get'})    

  def update(self,request,pk=None):
      return Response({'method':'This is put'})

  def partial_update(self,request,pk=None):
    return Response({'method':'This is patch'})

  def destroy(self,request,pk=None):
      return Response({'method':'This is delete'})

class UserProfileViewSet(viewsets.ModelViewSet):

  serializer_class=serializers.UserProfileSerializer
  queryset=models.UserProfile.objects.all()
  authentication_classes=(TokenAuthentication,)
  permission_classes=(permissions.UpdateOwnProfile,)

  filter_backends=(filters.SearchFilter,)
  search_fields=('name','email',)

class UserLoginApiView(ObtainAuthToken):
  renderer_classes= api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    permission_classes=(permissions.UpdateOwnStatus,IsAuthenticated)

    queryset = models.ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)