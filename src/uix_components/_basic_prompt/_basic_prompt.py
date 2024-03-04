import os
import json
from PIL import Image
import uix
from uix.elements import button, border, input, canvas, text, div, row, header, col, label
from uix_components import basic_imagecard as imagecard
from uix_components import basic_dialog as dialog

from uix import T

uix.html.add_css_file("_basic_prompt.css",__file__)

cur_path = os.path.dirname(os.path.abspath(__file__))

def get_image_data(folder_path):
    data = []

    for root, dirs, files in os.walk(folder_path):
        if os.path.basename(root) == "images":
            continue
        folder_item = {
            "title": os.path.basename(root).replace("_", " ").title(),
            "options": [],
        }
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                original_image_url = f"/prompt_image/{os.path.basename(root)}/{file}"
                output_path = os.path.join(os.path.dirname(__file__), "resized_images", os.path.basename(root), file)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Create directories if not exists
                downsized_image_url = f"/prompt_image/{os.path.basename(root)}/{file}?is-atr=m"
                folder_item["options"].append({
                    "name": file.split(".")[0].replace("_", " ").title(),
                    "image": downsized_image_url,
                    "originalImage": original_image_url
                })
        data.append(folder_item)
    return data

image_data = get_image_data(f"{cur_path}/images")

prompt_json = open(f"{cur_path}/prompt.json", "r")
prompt_test = prompt_json.read()
examples = json.loads(prompt_test)

prompt_json.close()
prompt_example = examples["examples"]

uix.html.add_script_source(id="prompt_ui",script="_basic_prompt.js",beforeMain=False,localpath=__file__)

class basic_prompt(uix.Element):
    def __init__(self, value = None, id = None, options = [], is_prompt_generator_open = True):
        super().__init__(value, id = id)
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

        self.is_prompt_generator_open = True if len(self.prompt_generator_datas) > 0 else False

        if self.is_prompt_generator_open:
            self.prompt_options.append({
                "name": "Prompt Generator",
                "id": "prompt-generator",
                "active": False
            })

        self.filter_text = ""

        self.options = options
        self.bottom_content_type = "Examples"
        self.prompt_generator_type = self.prompt_generator_datas[0]["title"]if len(self.prompt_generator_datas) > 0 else ""
        

        with self.cls("prompt"):
            with div(id="prompt-content").cls("prompt-content"):
                self.prompt_content()
            if self.is_prompt_generator_open:
                self.dialog = dialog("prompt-generator-dialog", close_icon="fa-solid fa-check", elements=[self.dialog_content], close_on_outside=False, close_callback=self.on_dialog_close)
                self.dialog.close_btn.classes = []
            with div(id="bottom").cls("hidden") as self.bottom:
                self.bottom_content_manager()

    def bottom_content_manager(self):
        with row("",id="bottom-content").cls("bottom-content") as bottom_content:
            if self.bottom_content_type == "Examples":
                self.example()
            else:
                self.example()
            with div(id="prompt-generator-options").cls("prompt-generator-options"):
                print(self.bottom_content_type)
                for option in self.prompt_options:
                    if option["name"] is not "Prompt Generator":
                        if self.bottom_content_type == option["name"]:
                            button(option["name"],id=option["id"]).cls("wall").on("click", self.set_bottom_content)
                        else:
                            button(option["name"],id=option["id"]).cls("wall prompt-btn-toggle").on("click", self.set_bottom_content)
                    else:
                            if self.bottom_content_type == option["name"]:
                                button(option["name"],id=option["id"]).cls("wall").on("click", self.set_bottom_content)
                            else:
                                button(option["name"],id=option["id"]).cls("wall prompt-btn-toggle").on("click", self.set_bottom_content)
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
        self.init()        
        prompt_content.update(self.prompt_content)
        self.prompt_input.focus() 


    def add_prompt_from_images(self, ctx, id, value):
        self.on_change(ctx, id, value["value"], True)

    def dialog_content(self):
        with col(id="dialog-content").cls("dialog-content") as dialog_content:
            with row("", id="prompt-generator-prompt").cls("prompt-texts prompt prompt-generator-prompt").style("height","15%").on("add-prompt", self.add_prompt_from_images):
                self.prompt_generator_prompt_area()
            with row("", id="prompt-generator-content").cls("prompt-generator-content"):
                self.prompt_generator()
        return dialog_content

    def prompt_generator_prompt_area(self):
        with div(id="prompt-generator-prompt-area").cls("wall prompt-texts") as text_section:
            for text in self.texts:
                self.text_comp(text)
        return text_section         

    def set_bottom_content(self,ctx, id, value):
        self.bottom_content_type = value
        if self.bottom_content_type == "Prompt Generator":
            ctx.elements["bottom"].update(self.bottom_content_manager)
            self.dialog.show()
            self.init()
            self.prompt_input.focus()
            self.bottom.remove_class("hidden")
        else:
            ctx.elements["bottom"].update(self.bottom_content_manager)
            self.init()
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
            self.filter_input = input(id="prompt-generator-filter-input", value=self.filter_text, placeholder = "Filter ...").cls("prompt-generator-filter-input").on("input", self.on_filter_change)
            with col(id="prompt-generator-types").cls("prompt-generator-types"):
                self.prompt_generator_types()
            with col().cls("hall").style("justify-content","flex-end"):
                imagecard(id="ref-image", imagesrc="/prompt_image/ref-image.png", textstr="Reference Image").style("pointer-events","none")

    def on_dialog_close(self,ctx, id, value):
        self.set_bottom_content(ctx, id, "Examples")

    def prompt_generator_types(self):
        with div() as types:
            print(self.prompt_generator_type)
            for prompt_generator_data in self.prompt_generator_datas:
                filtered_options = []
                for option in prompt_generator_data["options"]:
                    if option["name"] not in self.texts:
                        filtered_options.append(option)

                filtered_options = [option for option in filtered_options if self.filter_text == "" or self.filter_text in option["name"].lower() or self.filter_text in option["name"].upper() or self.filter_text in option["name"] and option["name"] not in self.texts]

                if filtered_options:
                    button_label = prompt_generator_data["title"]
                    len_filtered_options = " - ["+str(len(filtered_options))+"]"

                    if self.prompt_generator_type == prompt_generator_data["title"]:
                        with button(button_label, id=prompt_generator_data["title"]).cls("wall"):
                            text(len_filtered_options).style("color","gray")
                    else:
                        with button(button_label, id=prompt_generator_data["title"]).cls("wall btn-inactive").on("click", lambda ctx, id, value, prompt_title=prompt_generator_data["title"]: self.set_prompt_content(ctx, id, prompt_title)):
                            text(len_filtered_options).style("color","gray")
        return types

    def prompt_generator_images_filter(self):
        for prompt_generator_data in self.prompt_generator_datas:
            if self.prompt_generator_type == prompt_generator_data["title"]:
                # Sort the options alphabetically by name
                sorted_options = sorted(prompt_generator_data["options"], key=lambda x: x["name"])
                for option in sorted_options:
                    textstr = option["name"]
                    if textstr not in self.texts: 
                        if self.filter_text == "" or self.filter_text in textstr.lower() or self.filter_text in textstr.upper() or self.filter_text in textstr:   
                            imagecard(id=textstr, imagesrc=option["image"], textstr=textstr).cls("prompt-generator-card to-remove").on("click", lambda ctx, id, value, textstr=textstr: self.pop_image(ctx, id, textstr))
    
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
        if not without_filter:
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

    def init(self):
        if self.session is not None:  # Check if self.session is set before using it
            print("self.session is set")
            # Assuming you're calling the init-prompt event handler here
            self.session.queue_for_send("init-prompt", {"promptID":self.id,"inputID": "prompt-input", "historyID": "prompt-generator"}, "init-prompt")
        else:
            print("Warning: self.session is not set. Ensure it is set before calling init.")
