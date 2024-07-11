import uix
from uix.elements import file,col,text,label, row, input,border
from uix_components import basic_slider, basic_checkbox
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
            },
           "interactive_imageViewer": {
                "Delete": {
                    "icon": "fa-solid fa-trash-can",
                    "icon_styles": {"font-size": "20px", "color": "var(--danger-color)"},
                },
                "Edit": {
                    "icon": "fa-solid fa-pencil",
                    "icon_styles": {"font-size": "20px", "color": "var(--ait)"},
                },
                "Change Canvas": {
                    "icon": "fa-solid fa-refresh",
                    "icon_styles": {"font-size": "20px", "color": "var(--ait)"},
                },
                "Pan Mode": {
                    "icon": "fa-solid fa-hand",
                    "icon_styles": {"font-size": "20px", "color": "var(--ait)"},
                },
       

        }}



class input_image(uix.Element):
    def __init__(
            self,
            value=None,
            id=None,
            viewer="seadragon",
            callback=None,
            ):
        super().__init__(value=value,id=id)
        self.imageID = None
        self.viewer_id = id + "-viewer"
        self.file_id = id + "-file"
        self.dropzone_id= id + "-dropzone"
        self.label_id = id + "-label"
        self.loading_file_id = id + "-loading-file"
        self.filename= "drawable_image.png"
        self.file_url=""
        self.on_upload_done = callback
        self.cls("wall hall input")
        self.style("position","relative")
        self.viewer = viewer
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

            elif viewer == "interactiveSeadragon":
                self.create_drawable_image_viewer("my_images/white_background.jpg")

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
            if self.viewer is not "interactiveSeadragon":
                self.loading_file.set_style("display", "flex")
                self.dropzone_image.set_style("display", "none")
        else:
            ctx.elements["comp_alert"].open("alert-danger", T("File upload failed."))
  
    def create_image_viewer(self, image_url):
        with row(id=self.id + "canvas-container") as canvas_container:
            self.canvas_container = canvas_container 
            self.dropzone_image = image_viewer(id=self.viewer_id, value=image_url, buttonGroup=buttonGroupConfig["seadragon"]).size("100%", "100%")
        self.canvas_container.style("visibility", "hidden") 
        self.dropzone_image.on("button_click", self.on_button_click)
        self.dropzone_image.style("display: none ; z-index: 3")

    def create_drawable_image_viewer(self,image_url):
        with col(id=self.id + "-color-picker-container").cls("color-picker-container"):
            with row().size("100%", "max-content").style("justify-content", "end"):
                self.eraser_tool =basic_checkbox(id=self.id + "-eraser-tool", label_text="<i class='fa-solid fa-eraser fa-2x'></i>", 
                                                 value=False, callback=self.eraser_mode)
            with border().size("100%", "max-content").cls("brush-tool-container"):
                self.brushSize = basic_slider(id=self.id + "-brush-size", name=T("Brush Size") ,min=10, max=100, step=5, value=50, callback=self.on_slider_change)
            with border().size("100%", "max-content").cls("brush-tool-container"):
                text(value=T("Color"))
                self.color_picker = input(id=self.id + "-color-picker", type="color", value="#000000").style("height", "30px").on("input", self.on_color_change)
            with border().size("100%", "max-content").cls("brush-tool-container"):
                self.opacity = basic_slider(id=self.id + "-opacity", name=T("Opacity") ,min=0, max=1, step=0.1, value=1, callback=self.on_slider_change)
            
        with row(id=self.id + "canvas-container") as canvas_container:
            self.canvas_container = canvas_container
            self.dropzone_image = image_viewer(id=self.viewer_id, value=image_url, buttonGroup=buttonGroupConfig["interactive_imageViewer"],isInteractive=True).size("100%", "100%")
        
        self.file.style("display", "none")
        self.dropzone_parent.style("display", "none")
        self.canvas_container.style("visibility", "visible")
        self.dropzone_image.style("display: flex ; z-index: 3")
        self.dropzone_image.on("button_click", self.on_button_click)



    def create_fabric_viewer(self):
        with row(id=self.id + "canvas-container") as canvas_container:
            self.canvas_container = canvas_container
            self.dropzone_image = fabric(id=self.viewer_id)
        self.canvas_container.style("visibility", "hidden") 
        self.dropzone_image.style("display: none ; z-index: 8")
        buttonGroupConfig["fabric"]["Delete"]["onClick"] = self.resetImage
        button_group(items=buttonGroupConfig["fabric"], id=self.viewer_id + "-button-group").cls("button-group")

    def on_button_click(self,ctx, id, value):
        if value == "Delete":
            self.resetImage(ctx, id, value)
        elif value == "Edit":
            self.dropzone_image.open_edit_area(value= self.id + "-color-picker-container")
        elif value == "Change Canvas":
            self.dropzone_image.value = "my_images/white_background.jpg"
        elif value == "Pan Mode":
            self.dropzone_image.set_pan_mode()
      
    def resetImage(self,ctx, id, value):
            if self.dropzone_image.value:
                self.hide_image()
            else:
                self.hide_image()

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

    def on_color_change(self,ctx, id, value):
        ctx.elements[id].value = value     
        self.dropzone_image.edit_brush(color=self.color_picker.value,opacity=self.opacity.slider.value,brushSize=self.brushSize.slider.value)

    def on_slider_change(self,ctx, id, value):
        ctx.elements[id].value = value
        self.dropzone_image.edit_brush(color=self.color_picker.value, opacity=self.opacity.slider.value, brushSize=self.brushSize.slider.value)

    def eraser_mode(self,ctx, id, value):
        if value:
            self.eraser_tool.set_style("color", "var(--primary)")
        else:
            self.eraser_tool.set_style("color", "var(--text-color)")
        self.dropzone_image.eraser_tool(brushSize=self.brushSize.slider.value, value=value)
    