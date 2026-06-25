from django.db import models
from django.contrib.auth.models import User
class ChatRoom(models.Model):
    room_id=models.CharField(max_length=60,primary_key=True)
    user1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
    user2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
    class Meta:
        db_table='chatroom'

class Message(models.Model):
    room=models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)
    class Meta:
        db_table='message'