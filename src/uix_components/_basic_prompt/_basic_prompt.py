import os
import json
from PIL import Image
import uix
from uix.elements import button, border, input, canvas, text, div, row, header, col, label, icon, image
from uix_components import basic_imagecard as imagecard
from uix_components import basic_dialog as dialog
from dotenv import load_dotenv
from uix import T

load_dotenv()
cur_path = os.getenv("PROMPT_BUILDER_IMAGES_PARENT_PATH")

uix.html.add_css_file("_basic_prompt.css",__file__)

json_path = os.path.dirname(os.path.abspath(__file__))

def get_image_data(folder_path):
    data = []

    for root, dirs, files in os.walk(folder_path):
        if os.path.basename(root) == "images":
            continue
        
        parent_folder_name = os.path.basename(os.path.dirname(root))
        
        if parent_folder_name == "images":
            parent_folder_name = os.path.basename(root)
            super_folder_item = {
                "super_folder_name": parent_folder_name,
                "ref_image": os.path.basename(root),
                "ref_image_url": f"/manual_api/prompt_image/"+os.path.basename(root)+"/ref-image.png",
                "datas": []
            }
            for sub_dir in dirs:
                sub_dir_path = os.path.join(root, sub_dir)
                folder_item = {
                    "title": sub_dir.replace("_", " ").title(),
                    "options": [],
                }
                for file in os.listdir(sub_dir_path):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        original_image_url = f"/manual_api/prompt_image/{os.path.relpath(sub_dir_path, folder_path)}/{file}"
                        downsized_image_url = f"/manual_api/prompt_image/{os.path.relpath(sub_dir_path, folder_path)}/{file}?is-atr=m"
                        folder_item["options"].append({
                            "name": file.split(".")[0].replace("_", " ").title(),
                            "image": downsized_image_url,
                            "originalImage": original_image_url
                        })
                super_folder_item["datas"].append(folder_item)
            
            data.append(super_folder_item)        
    return data

try:
    image_data = get_image_data(f"{cur_path}/images")

    with open(f"{json_path}/prompt.json", "r", encoding="utf-8") as prompt_json:
        examples = json.load(prompt_json)
    prompt_example = examples["examples"]
except Exception as e:
    image_data = []
    prompt_example = {}

images_path = f"{cur_path}/images"

uix.html.add_script_source(id="prompt_ui",script="_basic_prompt.js",beforeMain=False,localpath=__file__)

class basic_prompt(uix.Element):
    def __init__(self, value = None, id = None, options = [], is_prompt_generator_open = True):
        super().__init__(value, id = id)
        print("Prompt Generator Open: ", is_prompt_generator_open)
        self.is_prompt_generator_open = is_prompt_generator_open
        self.texts = []
        
        self.prompt_generator_datas = image_data
            
        self.prompt_options = [
            {
                "name": "Examples",
                "id": "examples",
                "active": True
            }
        ]

        if self.is_prompt_generator_open:
            self.is_prompt_generator_open = True if len(self.prompt_generator_datas) > 0 else False

        if self.is_prompt_generator_open:
            self.prompt_options.append({
                "name": "Prompt Builder",
                "id": "prompt-generator",
                "active": False
            })

        self.filter_text = ""
        self.selected_ref_image_data = self.prompt_generator_datas[0] if len(self.prompt_generator_datas) > 0 else {}
        self.is_dialog_open = False
        self.options = options
        self.bottom_content_type = "Examples"
        self.prompt_generator_type = self.selected_ref_image_data["datas"][0]["title"] if len(self.selected_ref_image_data) > 0 else ""
        self.ref_images = []
        for data in self.prompt_generator_datas:
            self.ref_images.append(data["ref_image_url"])        

        with self.cls("prompt"):
            with div(id="prompt-content").cls("prompt-content"):
                self.prompt_content()
            if self.is_prompt_generator_open:
                self.dialog = dialog("prompt-generator-dialog", title="Prompt Builder", close_icon="fa-solid fa-check", elements=[self.dialog_content], close_on_outside=False, close_callback=self.on_dialog_close)
                self.dialog.close_btn.classes = []
            with div(id="bottom").cls("hidden") as self.bottom:
                self.bottom_content_manager()

    def bottom_content_manager(self):   
        with row("",id="bottom-content").cls("bottom-content") as bottom_content:
            if self.bottom_content_type == "Examples":
                self.example()
            else:
                self.example()
            with div(id="prompt-generator-options").cls("prompt-generator-options").style("height","fit-content"):
                for option in self.prompt_options:
                    if self.bottom_content_type == option["name"]:
                        button(option["name"],id=option["id"]).cls("wall").on("click", self.set_bottom_content)
                    else:
                        if option["name"] == "Prompt Builder":
                            button(option["name"],id=option["id"]).cls("wall prompt-btn-toggle fa-fade").on("click", self.set_bottom_content)
                        else:
                            button(option["name"],id=option["id"]).cls("wall prompt-btn-toggle").on("click", self.set_bottom_content)
                if self.is_prompt_generator_open == False:
                    with button("Prompt Builder", disabled=True).cls("prompt-btn-toggle").style("font-size:12px; text-wrap: nowrap;"):
                        text("Business").cls("business-only")

        return bottom_content

    def prompt_content(self):
        with label(id="prompt-texts", usefor="prompt-input").cls("prompt-texts row") as text_section:
            for text in self.texts:
                self.text_comp(text)
            self.prompt_input = input(id="prompt-input", value="", placeholder = T("Write Your Prompt Here")).cls("prompt-input").on("change", self.on_change).on("pop", lambda ctx, id, value: self.pop(ctx, id, self.texts[-1]))
        return text_section     

    def update_texts_content(self,ctx, id, value, without_filter=False):
        prompt_content = ctx.elements["prompt-content"]
        if self.is_prompt_generator_open:
            self.update_prompt_generator_content(ctx, id, value, without_filter)
        self.call_js()        
        prompt_content.update(self.prompt_content)
        self.prompt_input.focus() 

    def dialog_content(self):
        with col(id="dialog-content").cls("dialog-content") as dialog_content:
                with row("", id="prompt-generator-prompt").cls("prompt-texts prompt prompt-generator-prompt").style("height","15%").on("add-prompt", lambda ctx, id, value: self.on_change(ctx, id, value["value"], True)):
                    self.prompt_generator_prompt_area()
                with row("", id="prompt-generator-content").cls("prompt-generator-content"):
                    if self.is_dialog_open:
                        self.prompt_generator()
        return dialog_content

    def prompt_generator_prompt_area(self):
        with div(id="prompt-generator-prompt-area").cls("wall prompt-texts") as text_section:
            for text in self.texts:
                self.text_comp(text)
        return text_section         

    def set_bottom_content(self,ctx, id, value):
        self.bottom_content_type = value
        if self.bottom_content_type == "Prompt Builder":
            self.is_dialog_open = True
            ctx.elements["prompt-generator-prompt"].update(self.prompt_generator_prompt_area)
            ctx.elements["prompt-generator-content"].update(self.prompt_generator)
            ctx.elements["bottom"].update(self.bottom_content_manager)
            self.dialog.show()
            self.call_js()
            self.prompt_input.focus()
            self.bottom.remove_class("hidden")
        else:
            ctx.elements["bottom"].update(self.bottom_content_manager)
            self.call_js()
            self.prompt_input.focus()
            self.bottom.remove_class("hidden")

    def set_prompt_content(self, ctx, id, value):
        value_parts = value.split('-', 1)
        print(value_parts)
        self.prompt_generator_type = value_parts[0].strip()
        ctx.elements["prompt-generator-content"].update(self.prompt_generator)

    def on_filter_change(self,ctx, id, value):
        self.filter_text = value
        self.filter_input.value = value
        self.update_prompt_generator_content(ctx, id, value)

    def prompt_generator(self):
        with div(id="prompt-generator-images").cls("prompt-generator-images"):
            self.prompt_generator_images_filter()
        with div(id="prompt-generator-options").cls("prompt-generator-options"):
            with col().style("height","fit-content"):
                self.filter_input = input(id="prompt-generator-filter-input", value=self.filter_text, placeholder = "Filter ...").cls("prompt-generator-filter-input").on("input", self.on_filter_change)
                with col(id="prompt-generator-types").cls("prompt-generator-types"):
                    self.prompt_generator_types()
            with col().cls("ref-container"):
                with row().style("height","fit-content").style("gap","10px"):                        
                    for ref_image in self.ref_images:
                        if ref_image == self.selected_ref_image_data["ref_image_url"]:
                            image(value=ref_image+"?is-atr=m").style("border:1px solid black;outline: 2px solid white;").cls("ref-image")
                        else:
                            image(value=ref_image+"?is-atr=m").cls("ref-image").on("click", lambda ctx, id, value, ref_image=ref_image: self.on_ref_image_click(ctx, id, ref_image))
                self.ref_image = imagecard(id="ref-image", imagesrc=self.selected_ref_image_data["ref_image_url"], textstr="Reference Image").style("pointer-events","none").cls("hall").style("display","flex")

    def on_dialog_close(self,ctx, id, value):
        self.is_dialog_open = False
        self.call_js()
        self.set_bottom_content(ctx, id, "Examples")

    def prompt_generator_types(self):
        with div() as types:
            print(self.prompt_generator_type)
            for prompt_generator_data in self.selected_ref_image_data["datas"]:
                filtered_options = []
                for option in prompt_generator_data["options"]:
                    if option["name"] not in self.texts:
                        filtered_options.append(option)

                filtered_options = [option for option in filtered_options if self.filter_text == "" or self.filter_text in option["name"].lower() or self.filter_text in option["name"].upper() or self.filter_text in option["name"] and option["name"] not in self.texts]

                if filtered_options:
                    button_label = prompt_generator_data["title"]
                    print(button_label)
                    len_filtered_options = " - ["+str(len(filtered_options))+"]"

                    if self.prompt_generator_type == prompt_generator_data["title"]:
                        with button(button_label, id=prompt_generator_data["title"]).cls("wall"):
                            text(len_filtered_options).style("color","gray")
                    else:
                        with button(button_label, id=prompt_generator_data["title"]).cls("wall btn-inactive").on("click", lambda ctx, id, value, prompt_title=prompt_generator_data["title"]: self.set_prompt_content(ctx, id, prompt_title)):
                            text(len_filtered_options).style("color","gray")
        return types

    def prompt_generator_images_filter(self):
        for prompt_generator_data in self.selected_ref_image_data["datas"]:
            if self.prompt_generator_type == prompt_generator_data["title"]:
                # Sort the options alphabetically by name
                sorted_options = sorted(prompt_generator_data["options"], key=lambda x: x["name"])
                for option in sorted_options:
                    textstr = option["name"]
                    if textstr not in self.texts: 
                        if self.filter_text == "" or self.filter_text in textstr.lower() or self.filter_text in textstr.upper() or self.filter_text in textstr:   
                            imagecard(id=textstr, imagesrc=option["image"], textstr=textstr).cls("prompt-generator-card").on("click", lambda ctx, id, value, textstr=textstr: self.pop_image(ctx, id, textstr))
    
    def history(self):
        with col(id="prompt-history").cls("prompt-history") as history:
            text("History").cls("prompt-text")
        return history

    def example(self):
        with col(id="prompt-example").cls("prompt-example") as example:
            for key, value in prompt_example.items():
                text(value,id=key).cls("prompt-text").on("click", self.on_change)
        return example

    def update_prompt_generator_content(self,ctx, id, value, without_filter=False):
        if self.is_dialog_open:
            if not without_filter:
                if ctx.elements["prompt-generator-images"]:
                    content = ctx.elements["prompt-generator-images"]
                    content.update(self.prompt_generator_images_filter)
            prompt_types = ctx.elements["prompt-generator-types"]
            prompt_types.update(self.prompt_generator_types)
            prompt_generator_content = ctx.elements["prompt-generator-prompt"]
            prompt_generator_content.update(self.prompt_generator_prompt_area) 

    def text_comp(self, value):
        text(value, id="prompt-text-" + value).cls("prompt-generator-text").on("click", self.pop)

    def pop(self,ctx, id, value):
        if value in self.texts and len(self.texts) > 0:
            self.texts.remove(value)
            self.update_texts_content(ctx, id, value)

    def on_change(self,ctx, id, value, without_filter=False):
        if value != "" and value not in self.texts:
            split_coma = value.split(",")
            for text in split_coma:
                trimmed_text = text.strip()
                if trimmed_text != "" and trimmed_text not in self.texts:
                    self.texts.append(trimmed_text)
            self.update_texts_content(ctx, id, value, without_filter)
            self.prompt_input.value = ""

    def get_string(self):
        return ",".join(self.texts)
    
    def clear(self, ctx, id, value):
        self.texts = []
        self.update_texts_content(ctx, id, value)

    def __str__(self):
        if len(self.texts) > 0:
            return ", ".join(self.texts)
        else:
            return ""
        
    def pop_image(self, ctx, id, value):
        self.session.send(id, {"id": id, "value": value}, "delete-prompt-image")


    def on_ref_image_click(self, ctx, id, value):
        for ref_image in self.ref_images:
            if ref_image == value:
                self.selected_ref_image_data = self.prompt_generator_datas[self.ref_images.index(ref_image)]
                self.prompt_generator_type = self.selected_ref_image_data["datas"][0]["title"]
                ctx.elements["prompt-generator-content"].update(self.prompt_generator)

    def init(self):
        self.create_resize_api()
        self.call_js()

    def call_js(self):
        self.session.queue_for_send("init-prompt", {"promptID":self.id,"inputID": "prompt-input", "historyID": "prompt-generator"}, "init-prompt")

    ###### Resize API for prompt generator ######
    def create_resize_api(self):
        if self.is_prompt_generator_open:
            uix.app.register_api_handler("prompt_image", self.serve_prompt_image)

    def serve_prompt_image(self, paths, args):
        is_atr = args.get("is-atr", False)

        if paths[-1] == 'ref-image.png':
            if is_atr:
                downsized_image_path = f"{cur_path}/resized_images/{paths[1]}/ref-image.png"
                os.makedirs(os.path.dirname(downsized_image_path), exist_ok=True)
                if not os.path.exists(downsized_image_path):
                    self.resize_image(f"{images_path}/{paths[1]}/ref-image.png", downsized_image_path)
                return uix.send_file(downsized_image_path)
            else:
                return uix.send_file(f"{images_path}/{paths[1]}/ref-image.png")

        image_path = paths[1] + "/" + paths[2] + "/" + paths[3]
        full_path = os.path.join(images_path, image_path)

        if not os.path.exists(full_path):
            return "Image not found" + full_path, 404
        
        if is_atr:
            downsized_image_path = f"{cur_path}/resized_images/{image_path}"
            os.makedirs(os.path.dirname(downsized_image_path), exist_ok=True)
            if not os.path.exists(downsized_image_path):
                self.resize_image(full_path, downsized_image_path)
            # Serve the downsized image
            return uix.send_file(downsized_image_path)
        else:
            return uix.send_file(full_path)

    def resize_image(self, input_path, output_path, size=(300, 300)):
        if self.is_prompt_generator_open:
            try:
                img = Image.open(input_path)
                img.thumbnail(size)
                img.save(output_path)
            except Exception as e:
                print(e)
        else:
            return "Prompt Generator is not open", 400