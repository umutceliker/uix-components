import uix
from uix.elements import canvas
uix.html.add_header_item("fabric-cdn",'<script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"></script>')
uix.html.add_script_source('fabric-js', 'fabric.js',localpath=__file__, beforeMain=False)

class fabric(canvas):
    def __init__(self, id, value=None, width= 300, height= 150):
        super().__init__(id=id, value=value, width=width, height=height)
        self.tag = "canvas"

    def init(self):
        self.session.queue_for_send(self.id, self.value, "init-fabric")

