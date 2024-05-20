import uix
from uix.elements import file,col,text,label, row
from uix import T
from uix_components import image_viewer, fabric, button_group
uix.html.add_css_file("_input_image.css",__file__)

buttonGroupConfig = {
            "seadragon": {
                "Delete": {
                    "icon": "fa-solid fa-trash-can",
                    "icon_styles": {"font-size": "20px", "color": "var(--danger-color)"},
                },
            },
            "fabric": {
                "Delete": {
                    "icon": "fa-solid fa-trash-can",
                    "icon_styles": {"font-size": "20px", "color": "var(--danger-color)"},
                    "onClick": "",
                },
            }
        }
class input_image(uix.Element):
    def __init__(
            self,
            value=None,
            id=None,
            viewer="seadragon",
            callback=None
            ):
        super().__init__(value=value,id=id)
        self.imageID = None
        self.viewer_id = id + "-viewer"
        self.file_id = id + "-file"
        self.dropzone_id= id + "-dropzone"
        self.label_id = id + "-label"
        self.loading_file_id = id + "-loading-file"
        self.filename=""
        self.file_url=""
        self.on_upload_done = callback
        self.cls("wall hall input")
        self.style("position","relative")
        self.image_size_warning = None

        with self:
            self.file=file(id=self.file_id,accept="image/png, image/jpeg",multiple=False,callback=self.file_callback).cls("file-input")
            self.loading_file = col(id=self.loading_file_id).cls("loading-file hidden")

            with self.loading_file:
                col().cls("spinner")
                text(T("Uploading")+"...")

            with label(id=self.label_id,usefor=self.file_id).cls("dropzone-label") as dropzone_parent :
                self.dropzone_parent = dropzone_parent
                with col(id=self.dropzone_id).cls("dropzone") as dropzone_inside:
                    self.dropzone_inside = dropzone_inside
                    text(T("Click to upload")).style("font-size","1.5rem")
                    text(T("It supports only png , jpeg files . Upload size is limited to 10MB")).style("font-size","1rem")
                    
            if viewer == "seadragon":   
                self.create_image_viewer("my_images/AIT_AI_LOGO.png")
            else:
                self.create_fabric_viewer()

    def file_callback(self,ctx, id, event, data, status):
        if event == "select":
            self.upload_file(ctx, data, status)    
        elif event == "upload":
            self.upload_callback(ctx, id, data, status)
       
    def upload_file(self,ctx, data, value):
        self.dropzone_parent.set_style("display", "none")
        self.canvas_container.set_style("display", "none")
        if data[0].size < 10000000 and (data[0].type == "image/png" or data[0].type == "image/jpeg"):
            self.file.upload(data[0].url)
            self.dropzone_image.value =data[0].url
            self.file_url = data[0].url
            self.filename = data[0].name
        else:
            ctx.elements["comp_alert"].open("alert-danger", T("File size should be less than 10MB and file type should be png or jpeg."))
            self.dropzone_parent.set_style("display", "flex")
            self.loading_file.set_style("display", "none")

    def upload_callback(self,ctx, id, data, status):
        if status == "done":
            if self.on_upload_done:
                self.image_size_warning= self.on_upload_done(ctx, data, self.filename)
                if self.image_size_warning:
                    self.hide_image()
                else:
                    self.show_image()
            else:
                self.show_image()

        elif status == "progress":
            self.loading_file.set_style("display", "flex")
            self.dropzone_image.set_style("display", "none")
        else:
            ctx.elements["comp_alert"].open("alert-danger", T("File upload failed."))
            
    def create_image_viewer(self, image_url):
        with row(id=self.id + "canvas-container") as canvas_container:
            self.canvas_container = canvas_container 
            self.dropzone_image = image_viewer(id=self.viewer_id, value=image_url, buttonGroup=buttonGroupConfig["seadragon"]).size("100%", "100%")
        self.canvas_container.style("visibility", "hidden") 
        self.dropzone_image.on("button_click", self.resetImage)
        self.dropzone_image.style("display: none ; z-index: 3")

    def create_fabric_viewer(self):
        with row(id=self.id + "canvas-container") as canvas_container:
            self.canvas_container = canvas_container
            self.dropzone_image = fabric(id=self.viewer_id)
        self.canvas_container.style("visibility", "hidden") 
        self.dropzone_image.style("display: none ; z-index: 8")
        buttonGroupConfig["fabric"]["Delete"]["onClick"] = self.resetImage
        button_group(items=buttonGroupConfig["fabric"], id=self.viewer_id + "-button-group").cls("button-group")

    def resetImage(self,ctx, id, value):
            if self.dropzone_image.value:
                self.hide_image()
            else:
                print("No image to reset")

    def setImage(self, options):
        url = options.get("url", None)
        imageID = options.get("_id", None) or options.get("id", None)
        if url or imageID is not None:
            self.show_image()
            self.dropzone_image.value = url
            self.imageID = imageID
          
        else:
            self.hide_image()
    
    
        
    def show_image(self):
        self.dropzone_parent.set_style("display", "none")
        self.dropzone_inside.set_style("display", "none")
        self.dropzone_image.set_style("display", "flex")
        self.loading_file.set_style("display", "none")
        self.canvas_container.set_style("display", "flex")
        self.canvas_container.set_style("visibility", "visible")

    def hide_image(self):
        self.canvas_container.set_style("visibility", "hidden")       
        self.dropzone_parent.set_style("display", "flex")         
        self.dropzone_inside.set_style("display", "flex")
        self.dropzone_image.set_style("display", "none")
        self.dropzone_image.value = None
        self.file.set_style("display", "flex !important")   
        self.file.value = None
        self.loading_file.set_style("display", "none")


        
