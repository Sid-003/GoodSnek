from io import BytesIO
import PIL
import cv2
import numpy as np
import requests
import math
import wand
from PIL import Image, ImageDraw, ImageColor
from darkflow.net.build import TFNet
from discord import File, Member
from discord.ext import commands
import  random
from wand.image import Image


class Image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.tfnet = self.bot.tfnet

    # Implementation from: https://stackoverflow.com/a/7274986
    @classmethod
    def rgb_to_hsv(cls, rgb):
        rgb = rgb.astype('float')
        hsv = np.zeros_like(rgb)
        hsv[..., 3:] = rgb[..., 3:]
        r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
        maxc = np.max(rgb[..., :3], axis=-1)
        minc = np.min(rgb[..., :3], axis=-1)
        hsv[..., 2] = maxc
        mask = maxc != minc
        hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
        rc = np.zeros_like(r)
        gc = np.zeros_like(g)
        bc = np.zeros_like(b)
        rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
        gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
        bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
        hsv[..., 0] = np.select(
            [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
        hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
        return hsv

    @classmethod
    def hsv_to_rgb(cls, hsv):
        rgb = np.empty_like(hsv)
        rgb[..., 3:] = hsv[..., 3:]
        h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
        i = (h * 6.0).astype('uint8')
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
        rgb[..., 0] = np.select(conditions, [v, q, p, p, t, v], default=v)
        rgb[..., 1] = np.select(conditions, [v, v, v, q, p, p], default=t)
        rgb[..., 2] = np.select(conditions, [v, p, t, v, v, q], default=p)
        return rgb.astype('uint8')

    @classmethod
    def shift_hue(cls, arr, hout):
        hsv = cls.rgb_to_hsv(arr)
        hsv[..., 0] = hout
        rgb = cls.hsv_to_rgb(hsv)
        return rgb

    @commands.command(name='animewoke')
    async def eyes(self, ctx, url: str, hue: float = 1.0, rectangle: bool = False):
        response = await self.bot.session.get(url)
        imgarr = np.asarray(bytearray(await response.read()))
        img = cv2.imdecode(imgarr, 1)
        result = await self.bot.loop.run_in_executor(None, self.tfnet.return_predict, img)
        faces = [x for x in result if x['label'] == 'face' and x['confidence'] >= 0.40]
        right_eyes = [x for x in result if x['label'] == 're' and x['confidence'] >= 0.40]
        left_eyes = [x for x in result if x['label'] == 'le' and x['confidence'] >= 0.40]
        img = PIL.Image.open(BytesIO(await response.read())).convert("RGBA")
        red_eyes = PIL.Image.open('eyes/redflare.png').convert("RGBA")
        arr = np.array(red_eyes)
        red_eyes = PIL.Image.fromarray(self.shift_hue(arr, hue / 360.).astype('uint8'), 'RGBA')
        draw = ImageDraw.Draw(img)
        if not faces and not right_eyes and not left_eyes:
            await ctx.send('no definite features detected with strong confidence.')
            return
        for face in faces:
            face_top_left = (face['topleft']['x'], face['topleft']['y'])
            face_bottom_right = (face['bottomright']['x'], face['bottomright']['y'])
            if rectangle:
                draw.rectangle([face_top_left, face_bottom_right], width=2, outline=ImageColor.getrgb('red'))
        for right_eye in right_eyes:
            right_eye_bottom_right = (right_eye['bottomright']['x'], right_eye['bottomright']['y'])
            right_eye_top_left = (right_eye['topleft']['x'], right_eye['topleft']['y'])
            right_eye_width = right_eye_bottom_right[0] - right_eye_top_left[0]
            right_eye_height = right_eye_bottom_right[1] - right_eye_top_left[1]
            right_eye_x = right_eye_top_left[0] + (right_eye_width / 2)
            right_eye_y = right_eye_top_left[1] + (right_eye_height / 2)
            red_eyes = red_eyes.resize(((right_eye_width + 10) * 5, right_eye_height * 5))
            width, height = red_eyes.size
            img.paste(red_eyes, (int(right_eye_x) - int(width / 2), int(right_eye_y) - int(height / 2)), mask=red_eyes)
            if rectangle:
                draw.rectangle([right_eye_top_left, right_eye_bottom_right], width=2, outline=ImageColor.getrgb('blue'))
        for left_eye in left_eyes:
            left_eye_top_left = (left_eye['topleft']['x'], left_eye['topleft']['y'])
            left_eye_bottom_right = (left_eye['bottomright']['x'], left_eye['bottomright']['y'])
            left_eye_width = left_eye_bottom_right[0] - left_eye_top_left[0]
            left_eye_height = left_eye_bottom_right[1] - left_eye_top_left[1]
            left_eye_x = left_eye_top_left[0] + (left_eye_width / 2)
            left_eye_y = left_eye_top_left[1] + (left_eye_height / 2)
            red_eyes = red_eyes.resize(((left_eye_width + 10) * 5, left_eye_height * 5))
            width, height = red_eyes.size
            img.paste(red_eyes, (int(left_eye_x) - int(width / 2), int(left_eye_y) - int(height / 2)), mask=red_eyes)
            if rectangle:
                draw.rectangle([left_eye_top_left, left_eye_bottom_right], width=2, outline=ImageColor.getrgb('green'))
        del draw
        to_send = BytesIO()
        img.save(to_send, 'png')
        to_send.seek(0)
        await ctx.send(file=File(to_send, filename='animeyes.png'))


    @commands.command('warp')
    async def warp(self, ctx, *, url:str):
        response = await self.bot.session.get(url)
        bytes = BytesIO(await response.read())
        img = PIL.Image.open(bytes)
        btarr = img.load()
        img_output = img.copy()
        img_output_acc = img_output.load()
        width, height = img.size
        sclx = 1.0
        scly = 1.0
        cx = width / 2.0
        cy = height / 2.0
        r = cx
        if width > height:
            sclx =  width / height
        else:
            scly = height / width
            r = cy
        for i in range(width):
            for j in range(height):
                offset_x = int(25.0 * 1)
                offset_y = 0
                if j + offset_x < width:
                    img_output_acc[i, j] = btarr[i, (j + offset_x) % height]
                else:
                    img_output_acc[i, j] = 0

        file = BytesIO()
        img_output.save(file, 'png')
        file.seek(0)
        await ctx.send(file=File(file, filename='cool.png'))





    @commands.command(name='avatar')
    async def get_avatar(self, ctx, *, user: Member):
        url = str(user.avatar_url)
        response = await self.bot.session.get(url)
        ext = 'png'
        if user.is_avatar_animated():
            ext = 'gif'
        img_stream = BytesIO(await response.read())
        await ctx.send(file=File(fp=img_stream, filename=f'avatar.{ext}'))

def setup(bot):
    bot.add_cog(Image(bot))