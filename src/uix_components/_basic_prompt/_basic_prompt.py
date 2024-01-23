import os
import json

import uix
from uix.elements import button, border, input, canvas, text, div, row, header, col
from uix_components import basic_imagecard as imagecard
from uix_components import basic_dialog as dialog

uix.html.add_css_file("_basic_prompt.css",__file__)

cur_path = os.path.dirname(os.path.abspath(__file__))

prompt_json = open(f"{cur_path}/prompt.json", "r")
prompt_test = prompt_json.read()
examples = json.loads(prompt_test)

prompt_json.close()
prompt_example = examples["examples"]

uix.html.add_script_source(id="prompt_ui",script="_basic_prompt.js",beforeMain=False,localpath=__file__)

class basic_prompt(uix.Element):
    def __init__(self, value = None, id = None, options = []):
        super().__init__(value, id = id)
        
        self.texts = []
        self.history_texts = [
            "flawors , red background ",
            "flawors , red background ",
            "flawors , red background ",
            "flawors , red background ",
            "flawors , red background ",
            "flawors , red background ",
        ]
        self.examples = [
            "flawors , red background ",
            "flawors , red background ",
            "flawors , red background ",
            "flawors , red background ",
            "flawors , red background ",
        ]
        self.prompt_generator_datas = [
            {
                "title": "Artists",
                "options": [
                    {
                        "name": "Picasso",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Semih",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Umut",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Oğuz",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Bilmem ne",
                        "image": "https://picsum.photos/200/300"
                    },
                ]
            },
            {
                "title": "Art Movements",
                "options": [
                    {
                        "name": "Neon",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Cubism",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Surrealism",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Impressionism",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Picasso",
                        "image": "https://picsum.photos/id/237/200/300"
                    },
                                        {
                        "name": "Neon",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Cubism",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Surrealism",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Impressionism",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Picasso",
                        "image": "https://picsum.photos/id/237/200/300"
                    },
                                        {
                        "name": "Neon",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Cubism",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Surrealism",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Impressionism",
                        "image": "https://picsum.photos/200/300"
                    },
                    {
                        "name": "Picasso",
                        "image": "https://picsum.photos/id/237/200/300"
                    },
                    
                ]
            }
        ]
            
        self.prompt_options = [
            {
                "name": "Examples",
                "id": "examples",
                "active": True
            },
            {
                "name": "History",
                "id": "history",
                "active": False
            },
            {
                "name": "Prompt Generator",
                "id": "prompt-generator",
                "active": False
            }
        ]

        self.filter_text = ""

        self.options = options
        self.bottom_content_type = "Examples"
        self.prompt_generator_type = "Artists"

        self.id = "prompt-wrapper"

        with self.cls("prompt"):
            self.prompt_content()
            self.dialog = dialog("prompt-generator-dialog", close_icon="fa-solid fa-check", elements=[self.dialog_content], close_on_outside=False)
            self.dialog.close_btn.classes = []
            with div(id="bottom").cls("hidden") as self.bottom:
                self.bottom_content_manager()

    def dialog_content(self):
        with col(id="dialog-content").cls("dialog-content") as dialog_content:
            with row("", id="prompt-generator-prompt").cls("prompt-texts prompt prompt-generator-prompt").style("height","15%"):
                self.prompt_generator_prompt_area()
            with row("", id="prompt-generator-content").cls("prompt-generator-content"):
                self.prompt_generator()
        return dialog_content

    def bottom_content_manager(self):
        with row("",id="bottom-content").cls("bottom-content") as bottom_content:
            if self.bottom_content_type == "History":
                self.history()
            elif self.bottom_content_type == "Examples":
                self.example()
            with div(id="prompt-generator-options").cls("prompt-generator-options"):
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
    
    def prompt_generator_prompt_area(self):
        with div().cls("wall prompt-texts") as text_section:
            for text in self.texts:
                self.text_comp(text)
        return text_section         

    def set_bottom_content(self,ctx, id, value):
            print(value, "set_bottom_content")
            self.bottom_content_type = value
            if self.bottom_content_type == "Prompt Generator":
                self.dialog.show()
                self.init()
                self.prompt_input.focus()
                self.bottom.remove_class("hidden")
            else:
                ctx.elements["bottom"].update(self.bottom_content_manager)
                self.init()
                self.prompt_input.focus()
                self.bottom.remove_class("hidden")

    def set_prompt_content(self,ctx, id, value):
        self.prompt_generator_type = value
        ctx.elements["prompt-generator-content"].update(self.prompt_generator)

    def on_filter_change(self,ctx, id, value):
        self.filter_text = value
        self.filter_input.value = value
        self.update_prompt_generator_content(ctx, id, value)

    def prompt_generator(self):
            self.prompt_generator_images_filter()
            with div(id="prompt-generator-options").cls("prompt-generator-options"):
                self.filter_input = input(id="prompt-generator-filter-input", value=self.filter_text, placeholder = "Filter ...").cls("prompt-generator-filter-input").on("change", self.on_filter_change)
                for self.prompt_generator_data in self.prompt_generator_datas:
                    if self.prompt_generator_type == self.prompt_generator_data["title"]:
                        button(self.prompt_generator_data["title"],id=self.prompt_generator_data["title"]).cls("wall").on("click", lambda ctx, id, value: self.set_prompt_content(ctx, id, value))
                    else:
                        button(self.prompt_generator_data["title"],id=self.prompt_generator_data["title"]).cls("wall btn-inactive").on("click", lambda ctx, id, value: self.set_prompt_content(ctx, id, value))

    def prompt_generator_images_filter(self):
        with div(id="prompt-generator-images").cls("prompt-generator-images"):
            for prompt_generator_data in self.prompt_generator_datas:
                if self.prompt_generator_type == prompt_generator_data["title"]:
                    for option in prompt_generator_data["options"]:
                        textstr = option["name"] + " Prompt Generator"
                        if textstr not in self.texts: 
                            if self.filter_text == "" or self.filter_text in option["name"].lower() or self.filter_text in option["name"].upper() or self.filter_text in option["name"]:   
                                imagecard(id=textstr ,imagesrc=option["image"], textstr=textstr).cls("prompt-generator-card to-remove").on("click",lambda ctx, id, value, textstr=textstr: self.on_change(ctx, id, textstr))

    def history(self):
        with col(id="prompt-history").cls("prompt-history") as history:
            text("History").cls("prompt-text")
        return history

    def example(self):
        with col(id="prompt-example").cls("prompt-example") as example:
            for key, value in prompt_example.items():
                text(value,id=key).cls("prompt-text").on("click", lambda ctx, id, value=value: self.on_change(ctx, id, value))
        return example

    def update_texts_content(self,ctx, id, value):
        prompt_content = ctx.elements["prompt-texts"]
        prompt_generator_content = ctx.elements["prompt-generator-prompt"]
        prompt_content.update(self.prompt_content)
        prompt_generator_content.update(self.prompt_generator_prompt_area)
        self.update_prompt_generator_content(ctx, id, value)
        self.prompt_input.focus()


    def update_prompt_generator_content(self,ctx, id, value):
        content = ctx.elements["prompt-generator-content"]
        content.update(self.prompt_generator)
        self.init()
        self.prompt_input.focus()

    def prompt_content(self):
        with div(id="prompt-texts").cls("prompt-texts row").on("click", lambda ctx, id, value: self.prompt_input.focus()) as text_section:
            for text in self.texts:
                self.text_comp(text)
            self.prompt_input = input(id="prompt-input", value="", placeholder = "Write Your Prompt Here ...").cls("prompt-input").on("change", self.on_change)
        return text_section                    

    def text_comp(self, value):
        text(value, id="prompt-text-" + value).cls("border prompt-generator-text").on("click", self.pop)

    def pop(self,ctx, id, value):
        if value in self.texts:
            self.texts.remove(value)
            self.update_texts_content(ctx, id, value)

    def on_change(self,ctx, id, value):
        if value != "" and value not in self.texts:
            split_coma = value.split(",")
            for text in split_coma:
                trimmed_text = text.strip()
                if trimmed_text != "" and trimmed_text not in self.texts:
                    self.texts.append(trimmed_text)
            self.update_texts_content(ctx, id, value)
            self.prompt_input.value = ""


    def get_string(self):
        return ",".join(self.texts)

    def init(self):
        self.session.queue_for_send("init-prompt", {"inputID": "prompt-input", "historyID": "prompt-generator"},"init-prompt")
        self.prompt_input.on("pop", lambda ctx, id, value: self.pop(ctx, id, self.texts[-1]))
