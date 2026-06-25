from channels.consumer import AsyncConsumer
import json
from app.models import UserProfile
from channels.db import database_sync_to_async
from chat.models import Message,ChatRoom
class MyChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        self.room_id=self.scope['url_route']['kwargs']['room_id']
        self.user=self.scope['user']
        await self.channel_layer.group_add(self.room_id,self.channel_name)
        await self.send({
            'type':'websocket.accept',
        })
    async def websocket_receive(self,event):
        json_data=json.loads(event['text'])
        msg=json_data.get('message')
        action=json_data.get('action')
        if(action=='typing_start'):
            await self.channel_layer.group_send(self.room_id,{
                'type':'type.start',
                'action':'typing_start',
                'type_user':self.user.username,
            })
        elif(action=='typing_stop'):
            await self.channel_layer.group_send(self.room_id,{
                'type':'type.stop',
                'action':'typing_stop',
                'type_user':self.user.username,
            })
        elif(action=='delete_msg'):
            msg_id=json_data.get('msg_id')
            await self.channel_layer.group_send(self.room_id,{
                'type':'delete.msg',
                'action':'delete_success',
                'msg':msg_id,
            })
            await self.delete_msg_to_db(self.room_id,msg_id)
        else:
            sv=await self.save_message_to_db(self.room_id,self.user,msg)
            await self.channel_layer.group_send(self.room_id,{
                'type':'chat.message',
                'username':self.user.username,
                'msg':msg,
                'timestamp':sv.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                'msg_id':sv.id,
            })
    async def chat_message(self,event):
        response={
            'username':event['username'],
            'msg':event['msg'],
            'timestamp':event['timestamp'],
            'msg_id':event['msg_id']
        }
        await self.send({
            'type':'websocket.send',
            'text':json.dumps(response)
        })
    async def type_start(self,event):
        response={
            'type_user':event['type_user'],
            'action':'typing_start',
        }
        await self.send({
            'type':'websocket.send',
            'text':json.dumps(response)
        })
    async def type_stop(self,event):
        response={
            'type_user':event['type_user'],
            'action':'typing_stop',
        }
        await self.send({
            'type':'websocket.send',
            'text':json.dumps(response)
        })
    async def delete_msg(self,event):
        response={
            'action':'delete_success',
            'msg_id':event['msg']
        }
        await self.send({
            'type':'websocket.send',
            'text':json.dumps(response)
        })
    async def websocket_disconnect(self,event):
        await self.channel_layer.group_discard(self.room_id,self.channel_name)
    @database_sync_to_async
    def save_message_to_db(self,room_id,sender,msg):
        room_id=ChatRoom.objects.get(room_id=room_id)
        return Message.objects.create(room=room_id,sender=sender,text=msg)
    @database_sync_to_async
    def delete_msg_to_db(self,room_id,msg_id):
        room_id=ChatRoom.objects.get(room_id=room_id)
        return Message.objects.get(id=msg_id).delete()
    
online_users=set()
class OnlineGlobal(AsyncConsumer):
    async def websocket_connect(self,event):        
        self.user=self.scope['user']
        await self.channel_layer.group_add('global_online_users',self.channel_name)
        online_users.add(self.user.username)
        await self.send({
            'type':'websocket.accept',
        })
        response={
            'already_online_users':list(online_users)
        }
        await self.send({
            'type':'websocket.send',
            'text':json.dumps(response)
        })
        await self.channel_layer.group_send('global_online_users',{
            'type':'online.user',
            'action':'user_online',
            'username':self.user.username,
            })
    async def online_user(self,event):
        response=({
            'username':event['username'],
            'action':'user_online',
        })
        await self.send({
            'type':'websocket.send',
            'text':json.dumps(response)
        })

    async def websocket_disconnect(self,event):
        await self.channel_layer.group_discard('global_online_users',self.channel_name)
        online_users.remove(self.user.username)
        await self.channel_layer.group_send('global_online_users',{
            'type':'offline.user',
            'action':'user_offline',
            'username':self.user.username,
        })
    async def offline_user(self,event):
        response={
            'action':'user_offline',
            'username':event['username'],
        }
        await self.send({
            'type':'websocket.send',
            'text':json.dumps(response)
        })


