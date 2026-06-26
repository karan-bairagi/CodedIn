from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from chat.models import Message,ChatRoom
from rest_framework.authentication import BaseAuthentication
from chat.serializers import SerachSerilizer,InboxSerializer,MessageSerilizer
from django.db.models import Q
from app.views import login_required
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
@login_required
def index_view(request):
    return render(request,'index.html')
class CsrfExemptSessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = getattr(request._request, 'user', None)
        if not user or not user.is_authenticated:
            return None
        return (user, None)
class ChatSearch(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            search_input = request.query_params.get('q','')
            check=User.objects.filter(username__icontains=search_input)
            if check.exists():
                all_search_users=SerachSerilizer(check,many=True)
                return Response({
                    'detail':all_search_users.data,
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'detail':'not query found'
                },status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'detail':'Internal Server error'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class Inbox(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            user=request.user
            print(user)
            find=ChatRoom.objects.filter(Q(user1=user)|Q(user2=user)).filter(message__isnull=False).distinct()
            serilizer=InboxSerializer(find,many=True,context={'request':request})
            return Response({
                'detail':serilizer.data,
                'login_username':user.username,
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'detail':'Internal Server error'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class RoomGeneration(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            active_room=None
            user=request.user
            print(user)
            print(user.id)
            room_id=request.data.get('room_id')
            target_user_id=request.data.get('target_user_id')
            if(room_id):
                active_room=room_id
            elif target_user_id:
                target_user_id=int(target_user_id)
                ids=sorted([user.id,target_user_id])
                generate_room_id=f"Chat_with_{ids[0]}_to_{ids[1]}"
                try:
                    find=ChatRoom.objects.get(room_id=generate_room_id)
                    active_room=find.room_id
                except ChatRoom.DoesNotExist:
                    user2=User.objects.get(id=target_user_id)
                    add=ChatRoom.objects.create(room_id=generate_room_id,user1=user,user2=user2)
                    active_room=add.room_id
            all_chat_msg=Message.objects.filter(room=active_room).order_by('timestamp')
            serilizer=MessageSerilizer(all_chat_msg,many=True)
            return Response({
                'detail':serilizer.data,
                'room':active_room,
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'detail':'Internal Server error'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class Message_Read(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request,room_id):
        try:
            user=request.user
            check=Message.objects.filter(room_id=room_id,is_read=False).exclude(sender=user).update(is_read=True)
            return Response({
                'detail':'Successfully',
                'read':check
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'detail':'Internal Server error'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)