import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from app.models import BoardingKelas

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.roomGroupName = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        id_user = text_data_json["id_user"]
        id_kelas = text_data_json["id_kelas"]
        nama = text_data_json["nama"]
        image = text_data_json["image"]
        
        await self.save_message(message, id_user, id_kelas)     

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "id_user": id_user,
                "id_kelas": id_kelas,
                "nama":nama,
                "image": image
            }
        )
        
    async def sendMessage(self, event):
        message = event["message"]
        id_user = event["id_user"]
        nama = event["nama"]
        image=event["image"]
        await self.send(text_data=json.dumps({"message": message,
                                               "id_user": id_user,
                                               "nama":nama,
                                               "image": image}))
    
    @sync_to_async
    def save_message(self, message, id_user, id_kelas):
        print(id_user,id_kelas,"----------------------")

        BoardingKelas.create_boarding(pesan=message,pengirim_id=id_user,id_kelas_id=id_kelas)
