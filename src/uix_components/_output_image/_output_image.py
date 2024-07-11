import uix
from uix.elements import div
from uix import T
from uix_components import image_viewer, fabric, button_group
from ._output_loading import output_loading


buttonGroupConfig = {
            "seadragon": {
                "Zoom in": {"icon": "fa-search-plus", "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
                "Zoom out": {"icon": "fa-search-minus", "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
                "Home": {"icon": "fa-home", "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
                "Full screen": {"icon": "fa-expand", "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
                "Download": {"icon": "fa-download", "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
                "Save": {"icon": "fa-solid fa-floppy-disk", "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
                "Send to input": {"icon": "fa-arrow-left", "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
            },
            "fabric": {
                "Download": {"icon": "fa-solid fa-download", "icon_styles": {"font-size": "20px", "color": "var(--ait)"},"link":"my_images/AIT_AI_LOGO.png", "download":True},
                "Save": {"icon": "fa-solid fa-floppy-disk", "icon_styles": {"font-size": "20px", "color": "var(--ait)"}, "onClick": ""},
            }
        }
class output_image(uix.Element):
    def __init__(
            self,
            value=None,
            id=None,
            viewer="seadragon",
            setinputImage=None,
            add_to_favorite=None
    ):
        super().__init__(value=value, id=id)
        self.id = id
        self.viewer_id = id + "-viewer"
        self.file_id = id + "-file"
        self.label_id = id + "-label"
        self.loading_file_id = id + "-loading-file"
        self.loading_id = id + "-loading"
        self.setinputImage= setinputImage
        self.add_to_favorite = add_to_favorite
        self.viewer=viewer
        self.cls("wall hall")
        self.style("position", "relative")
       

        with self:
            if self.viewer == "seadragon":
                self.create_image_viewer("my_images/AIT_AI_LOGO.png")
            else:
                with div().cls("wall hall").style("position", "absolute").style("top", "0").style("left", "0"):
                    self.create_fabric_viewer("my_images/AIT_AI_LOGO.png")
            self.output_loading = output_loading(id=self.loading_id).cls("wall hall hidden")

    def create_image_viewer(self, image_url):
        self.image_viewer = image_viewer(id=self.viewer_id, value=image_url, buttonGroup=buttonGroupConfig["seadragon"]).size("100%", "100%").cls("opacity-30")
        self.image_viewer.on("button_click", self.on_click)

    def create_fabric_viewer(self, image_url):
        self.image_viewer = fabric(id=self.viewer_id, value=image_url).size("100%", "100%").cls("opacity-30")
        buttonGroupConfig["fabric"]["Save"]["onClick"] = self.addToFavorite
        self.buttonGroup=button_group(items=buttonGroupConfig["fabric"], id=self.viewer_id + "-button-group").cls("button-group")

    def set_image(self,ctx, id=None, value=None):
        url = value
        if isinstance(value, dict):
            url = value.get("url")

        imageID = id
        if url or imageID is not None:
            self.output_loading.add_class("hidden")
            self.image_viewer.remove_class("hidden")
            self.value = imageID
            self.image_viewer.value = url
            self.image_viewer.remove_class("opacity-30")
            if self.viewer == "fabric":
                self.output_loading.add_class("hidden")
                self.image_viewer.remove_class("hidden")
                self.buttonGroup.link.attrs["href"]=self.image_viewer.value
                name=self.image_viewer.value.split("/")[-1]
                self.buttonGroup.link.attrs["download"]=name
                self.buttonGroup.update()
                
        elif imageID is None:
            self.image_viewer.add_class("opacity-30")
            self.image_viewer.value = "my_images/AIT_AI_LOGO.png"
        
        else:
            self.image_viewer.value = url
        
      
    def loading(self, is_loading=True):
        if is_loading:
            self.image_viewer.add_class("hidden")
            self.output_loading.remove_class("hidden")
        else:
            self.output_loading.add_class("hidden")
            self.image_viewer.remove_class("hidden")
       
    def sendToInput(self,ctx,id,value):
        if value == None and "comp_alert" in ctx.elements:
            ctx.elements["comp_alert"].open("alert-danger",(T("Something went wrong")))
        dataToSend = {
            "id": self.value,
            "url": self.image_viewer.value
        }
        
        if self.setinputImage is not None:
            self.setinputImage(dataToSend)
        else:
            pass
        
    def addToFavorite(self,ctx,id,value):
        if self.add_to_favorite is not None:
            self.add_to_favorite(ctx, id, self.value)

    def on_click(self, ctx, id, value):
        if value == "Zoom in":
            self.image_viewer.zoom_in()
        elif value == "Zoom out":
            self.image_viewer.zoom_out()
        elif value == "Home":
            self.image_viewer.home()
        elif value == "Full screen":
            self.image_viewer.fullscreen()
        elif value == "Download":
            self.addToFavorite(ctx, "download", value)
            self.image_viewer.download()
        elif value == "Send to input":
            self.sendToInput(ctx, id, self.value)
        elif value == "Save":
            self.addToFavorite(ctx, id, value)


    


