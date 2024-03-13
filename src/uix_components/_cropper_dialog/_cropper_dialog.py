
import uix
from uix.elements import button, canvas, text
from uix_components._basic_dialog._basic_dialog import basic_dialog
uix.html.add_script_source('crop-js', '_cropper_dialog.js',localpath=__file__, beforeMain=False)
          
class cropper_dialog(uix.Element):
    def __init__(self, id=None, image_url=None, callback=None):
        super().__init__(id=id)
        self.callback = callback
        self.image_url = image_url
        self.dialog = basic_dialog(id=self.id + "-dialog", elements=[self.crop_dialog]).size("42vw","70vh")

    def show(self):
        self.dialog.show()
        self.session.send(self.id, {"imageUrl": self.image_url, "cropCanvas" : self.canvas.id}, "init-cropper")

    def hide(self):
        self.dialog.hide()

    def crop_dialog(self):
        self.canvas = canvas(id=self.id+"-cropper").style("border","2px solid black")
        self.canvas.attrs["width"] = 800
        self.canvas.attrs["height"] = 450
        text("* Crop işlemi yapmak için resme çift tıklayın.")
        text("* İşleminiz bittiğinde imaj dışarısındaki bir alana tıklayarak işlemi gerçekleştirmiş olursunuz.")
        text("* Done butonuna basarak işlemi tamamlayabilirsiniz.")
        button("Done", id="doneButton").on("cropper-done", self.callback)


title = "Cropper Dialog"


description = """
# cropper_dialog(id, image_url, callback)
1. Cropper dialog bir image'ı crop etmek için kullanılır. Dialog içerisinde image'ı crop edebilir ve sonucu alabilirsiniz.
    | attr          | desc                                                                                                 |
    | :------------ | :-----------------------------------------------------------------------------------------------     |
    | id           | Element id.                                                                                           |
    | callback     | Crop işlemi bittiğinde çağrılacak fonksiyon, bu fonksiyonun value değeri croplanmış image url içerir. |
    | image_url    | Cropper'ın başlangıçta göstereceği image url.                                                         |
"""

sample = """
from uix_components._cropper_dialog._cropper_dialog import cropper_dialog
from uix_components._input_image._input_image import input_image
from uix.elements import button, col
import uix_components
import uix

file_url = ""

def crop_done(ctx, id, value):
    options = {"url" : value, "id" : None}
    ctx.elements["input-image-crop"].setImage(options)
    ctx.elements["cropper_dialog"].image_url = value
    ctx.elements["cropper_dialog"].hide()

def upload_done(ctx, id, value):
    global file_url
    file_url = ctx.elements["input-image-crop"].file_url
    ctx.elements["cropper_dialog"].image_url = file_url

def cropper_dialog_example():
    global file_url
    cropper_dialog(id="cropper_dialog", callback = crop_done, image_url = file_url)
    with col(id="cropper-col").cls("border").style("width","40%").style( "height","30%"):
        input_image(id="input-image-crop", callback=upload_done).style("height","500px")
        button("Crop", id="crop-button").on("click", lambda ctx, id, value: ctx.elements["cropper_dialog"].show())
"""
        
        