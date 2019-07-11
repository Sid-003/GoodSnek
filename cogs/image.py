from io import BytesIO

import PIL
import cv2
import numpy as np
import requests

from PIL import Image, ImageDraw, ImageColor
from discord import File, Member
from discord.ext import commands
from darkflow.net.build import TFNet


class Image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        options = {"pbLoad": "modeldata/model.pb", "metaLoad": "modeldata/config.meta", "threshold": 0.1}
        self.tfnet = TFNet(options)

    @commands.command(name='animeeyes')
    async def detect_eyes(self, ctx, url: str):
        response = requests.get(url)
        imgarr = np.asarray(bytearray(response.content))
        img = cv2.imdecode(imgarr, 1)
        result = self.tfnet.return_predict(img)
        faces = [x for x in result if x['label'] == 'face' and x['confidence'] >= 0.40]
        right_eyes = [x for x in result if x['label'] == 're' and x['confidence'] >= 0.40]
        left_eyes = [x for x in result if x['label'] == 'le' and x['confidence'] >= 0.40]
        img = PIL.Image.open(BytesIO(response.content))
        draw = ImageDraw.Draw(img)
        for face in faces:
            face_top_left = (face['topleft']['x'], face['topleft']['y'])
            face_bottom_right = (face['bottomright']['x'], face['bottomright']['y'])
            draw.rectangle([face_top_left, face_bottom_right], width=2, outline=ImageColor.getrgb('red'))
        for right_eye in right_eyes:
            right_eye_bottom_right = (right_eye['bottomright']['x'], right_eye['bottomright']['y'])
            right_eye_top_left = (right_eye['topleft']['x'], right_eye['topleft']['y'])
            draw.rectangle([right_eye_top_left, right_eye_bottom_right], width=2, outline=ImageColor.getrgb('blue'))
        for left_eye in left_eyes:
            left_eyes_top_left = (left_eye['topleft']['x'], left_eye['topleft']['y'])
            left_eyes_bottom_right = (left_eye['bottomright']['x'], left_eye['bottomright']['y'])
            draw.rectangle([left_eyes_top_left, left_eyes_bottom_right], width=2, outline=ImageColor.getrgb('green'))
        del draw
        to_send = BytesIO()
        img.save(to_send, 'png')
        to_send.seek(0)
        await ctx.send(file=File(to_send, filename='animeyes.png'))


    @commands.command(name='avatar')
    async def get_avatar(self, ctx, *, user: Member):
        response = requests.get(user.avatar_url)
        ext = 'png'
        if user.is_avatar_animated():
            ext = 'gif'
        img_stream = BytesIO(response.content)
        await ctx.send(file=File(fp=img_stream, filename=f'avatar.{ext}'))

def setup(bot):
    bot.add_cog(Image(bot))