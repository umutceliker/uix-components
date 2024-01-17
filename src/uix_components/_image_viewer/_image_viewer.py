import uix
import os
uix.html.add_script_source('seadragon-js-lib', 'openseadragon.min.js',localpath=__file__,beforeMain=False)
uix.html.add_script_source('seadragon', 'seadragon.js',localpath=__file__, beforeMain=False)
icons_path = os.path.join(os.path.dirname(__file__), "icons")

uix.app.add_static_route("image_viewer",icons_path)
print("image_viewer:",icons_path)
class image_viewer(uix.Element):
    def __init__(self, id = None, value=None, hasButtons=True, zoom=False, size=(500,500)):
        super().__init__(id=id, value=value)
        self.tag = "div"
        self.value_name = None
        self.hasButtons = hasButtons
        self.config = {
            "hasButtons": hasButtons,
            "zoom":  zoom,
            "image": value,
            "prefixUrl":  "image_viewer/"
        }
        if size is not None and len(size) == 2:
            self.size(*size)

    def bind(self,session):
        if self.id is None:
            self.id = "osd_" + str(session.next_id())
        super().bind(session)

    def init(self):
        self.session.queue_for_send(self.id, self.config, "init-seadragon")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        if self._value is not None:
            self.session.send(self.id, self.value_to_command("open",{"type": "image","url": self._value}), "seadragon")

    def value_to_command(self,command,value):
        return { "action": command, "value": value }