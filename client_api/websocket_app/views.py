import os
from urllib.parse import parse_qs

import socketio
import jwt
from asgiref.sync import sync_to_async
from django.conf import settings

basedir = os.path.dirname(os.path.realpath(__file__))
manager = socketio.AsyncRedisManager(settings.SOCKET_IO_MANAGER)
sio = socketio.AsyncServer(
    client_manager=manager,
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=False,
    engineio_logger=False
)


class TransformImageNamespace(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        try:
            token = parse_qs(environ['QUERY_STRING'])['token'][0]
            user_id = jwt.decode(token, settings.SECRET_KEY)['user_id']
            await self.save_session(sid, {'user_id': user_id})
        except (KeyError, jwt.PyJWTError):
            return

    async def on_get_image(self, sid, data):
        session = await self.get_session(sid)
        user_id = session.get('user_id')
        if user_id is None:
            await self.emit('error', {'info': 'token is missing or expired'}, sid)
            return

        image_id = data.get('image_id')
        if image_id is None:
            await self.emit('error', {'info': 'image_id is missing'}, sid)
            return

        has_permission = await self._user_has_permission(user_id, image_id)
        if has_permission is False:
            await self.emit('error', {'info': 'You don\'t have permissions to retrieve this image'}, sid)
            return

        self.enter_room(sid, room=image_id)

    async def _user_has_permission(self, user_id, image_id):
        from image.models import TransformedImage

        try:
            get_transformed_image = sync_to_async(TransformedImage.objects.get)
            await get_transformed_image(id=image_id, user_id=user_id)
            return True
        except TransformedImage.DoesNotExist:
            return False


sio.register_namespace(TransformImageNamespace('/'))
