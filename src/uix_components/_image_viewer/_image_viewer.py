import io
from uuid import uuid4
import uix
import os
from PIL import Image
uix.app.add_static_route("seadragon", os.path.dirname(__file__))
uix.html.add_header_item("seadragon", '<script src="/seadragon/openseadragon.min.js"></script>')
#uix.html.add_script_source('seadragon-js-lib', 'openseadragon.min.js',localpath=__file__,beforeMain=False)
uix.html.add_script_source('seadragon', 'seadragon.js',localpath=__file__, beforeMain=False)
icons_path = os.path.join(os.path.dirname(__file__), "icons")


class image_viewer(uix.Element):
    def __init__(self, id = None, value=None, buttonGroup={}, zoom=False, size=(500,500)):
        super().__init__(id=id, value=value)
        self.tag = "div"
        self.value_name = None
        self.buttonGroup = buttonGroup
     
        self.config = {
            "buttonGroup": buttonGroup,
            "zoom":  zoom,
            "image": value,
        }
        if size is not None and len(size) == 2:
            self.size(*size)

        self.has_PIL_image = False
        self.set_later = True
    def init(self):
        self.session.queue_for_send(self.id, self.config, "init-seadragon")
        self.value = self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, Image.Image):
            self.has_PIL_image = True
            self._value = self._create_image_url(value)
        else:
            self.has_PIL_image = False
            self._value = value
            
        if self._value is not None:
            if self.set_later:
                self.session.queue_for_send(self.id, self.value_to_command("open",{"type": "image","url": self._value}), "seadragon")
            else:
                self.session.send(self.id, self.value_to_command("open",{"type": "image","url": self._value}), "seadragon")
        self.set_later = False

    def __del__(self):
        if self.has_PIL_image:
            uix.app.files[self.id] = None

    def _create_image_url(self,img):
        if self.id is None:
            self.id = str(uuid4())
        temp_data = io.BytesIO()
        img.save(temp_data, format="png")
        temp_data.seek(0)
        uix.app.files[self.id] = {"data":temp_data.read(),"type":"image/png"}
        return "/download/"+self.id + "?" + str(uuid4())
    
    def value_to_command(self,command,value):
        return { "action": command, "value": value }


    def zoom_in(self):
        self.session.send(self.id, self.value_to_command("zoomIn", None), "seadragon")

    def zoom_out(self):
        self.session.send(self.id, self.value_to_command("zoomOut", None), "seadragon")

    def home(self):
        self.session.send(self.id, self.value_to_command("home", None), "seadragon")
    
    def fullscreen(self):
        self.session.send(self.id, self.value_to_command("fullscreen", None), "seadragon")
    
    def download(self):
        self.session.send(self.id, self.value_to_command("download", None), "seadragon")

    def save(self):
        #save fonksiyonu yazılacak
        pass


title = "Image Viewer"
description = """
## image_viewer(id, value, buttonGroup, zoom, size)
1. Verilen resmi gösteren bir image viewer oluşturur.

| attr                  | desc                                                                |
| :-------------------- | :------------------------------------------------                   |
| id                    | image_viewer elementinin id'si                                      |
| value                 | image_viewer elementinin göstereceği image url'si veya Image objesi |
| buttonGroup           | image_viewer elementinin sağ üst köşesindeki buton grubu.           |
| zoom                  | image_viewer elementinin zoom yapılmasını sağlar.                   |
| size                  | image_viewer elementinin boyutu. (width, height)                    |
"""
sample = """
import random
from uix.elements import file, row, button,div
from uix_components import image_viewer, basic_alert
from uix.elements._image import title, description, sample as code

buttonGroup= {
    "Zoom in": {
        "icon": "fa-search-plus",
        "icon_styles": {"font-size": "20px", "color": "var(--ait)"},
    },
    "Zoom out": {
        "icon": "fa-search-minus",
        "icon_styles": {"font-size": "20px", "color": "var(--ait)"},
    },
    "Home": {
        "icon": "fa-home",
        "icon_styles": {"font-size": "20px", "color": "var(--ait)"},
    },
    "Full screen": {
        "icon": "fa-expand",
        "icon_styles": {"font-size": "20px", "color": "var(--ait)"},
    },
    "Download": {
        "icon": "fa-download",
        "icon_styles": {"font-size": "20px", "color": "var(--ait)"},
    }
}

def on_button_pil_image_click(ctx, id, value):
    pil_image = create_image()
    iw = ctx.session.elements["iw1"]
    iw.value = pil_image

def on_button_click(ctx, id, value):    
    ctx.elements["alert1"].open("alert-success",value)    

def on_upload(ctx, id, event, data, status):
    print("on_upload", id, event, data, status)
    if status == "done":
        iw = ctx.session.elements["iw1"]
        if event == "select":
            iw.value = data[0].url
        
def image_viewer_example():      
    basic_alert("Image Viewer",id="alert1",type="success")
    with div() as main:
            with row():
                file(id="file1",accept="image/*",multiple=False,callback=on_upload).cls("center")
                button("Show PIL Image",id="show_pil_image").on("click",on_button_pil_image_click)
            iw1 = image_viewer(id = "iw1", value="https://ai.ait.com.tr/wp-content/uploads/AIT_AI_LOGO.png",buttonGroup=buttonGroup).size(400,400)
            iw1.on("button_click",on_button_click).cls("border")
    return main

from PIL import Image, ImageDraw, ImageFilter
def create_image():
    def random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def gradient_circle(draw, center, radius, color1, color2):
        for i in range(radius, 0, -1):
            color = (
                int(color1[0] + (color2[0] - color1[0]) * i / radius),
                int(color1[1] + (color2[1] - color1[1]) * i / radius),
                int(color1[2] + (color2[2] - color1[2]) * i / radius)
            )
            draw.ellipse((center[0] - i, center[1] - i, center[0] + i, center[1] + i), fill=color)

    img_size = 400
    image = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(image)

    # Draw a grid of gradient circles
    spacing = 80  # Space between centers of circles
    radius = 40
    for x in range(spacing, img_size, spacing):
        for y in range(spacing, img_size, spacing):
            gradient_circle(draw, (x, y), radius, random_color(), random_color())

    # Apply a slight blur to smooth out the gradients
    image = image.filter(ImageFilter.GaussianBlur(2))
    return image
"""
