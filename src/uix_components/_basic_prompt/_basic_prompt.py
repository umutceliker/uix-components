import uix
from uix.elements import button, border, input, canvas, text, div, row

uix.html.add_script("prompt-js","""
    event_handlers["init-prompt"] = function(id, value, event_name) {
        const input = document.getElementById(value.inputID);
        const history = document.getElementById(value.historyID);
                    
        input.addEventListener("focus", function(e) {
            history.style.display = "block";
            console.log("focus");
        });
                    
        input.addEventListener("blur", function(e) {
            history.style.display = "none";
        });
                    
        input.addEventListener("keydown", function(e) {
                    if (e.key === "Backspace" && (e.target.value === "" || input.selectionStart === 0)) {
                        e.preventDefault();
                        clientEmit(value.inputID, "pop", "pop")
                    }
            });
    };
    

""",beforeMain=False)

uix.html.add_css("prompt-css","""
.prompt {
font-family: var(--ait-text-font);
padding: 5px;
display: flex;
align-items: center;
background-color: var(--background-secondary);
border: 1px solid gray;
border-radius: 6px;
box-sizing: border-box;
color: white;
outline: none;
resize: none;   
flex-direction: row;
flex-wrap: wrap;
max-width: 100%;
position: relative;
gap: 10px;
transition: all 0.5s ease-in-out;

}

.prompt-texts {
    width: fit-content;
    height: fit-content;
    flex-wrap: wrap;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    gap: 10px;
    transition: all 0.5s ease-in-out;
                }

.prompt-texts p:hover {
    background-color: var(--background-secondary);
    color: var(--text-primary);
    cursor: pointer;
    transition: all 0.5s ease-in-out;
                 }
                 
.history-list {
width: 100%;
background-color: var(--background-secondary);
left: 0;
z-index: 1;
position: absolute;
height: 200px;
border: 1px solid gray;
border-radius: 0px 0px 6px 6px;
resize: vertical;
overflow: auto;
top: 95%;
box-sizing: border-box;
}         
""")

class basic_prompt(uix.Element):
    def __init__(self, value = None, id = None):
        super().__init__(value, id = id)
        
        self.texts = []

        with self.cls("prompt"):
            self.texts_func()
            self.prompt_generator()

    def prompt_generator(self):
        div("",id="history-list").cls("history-list")
    
    def update_content(self,ctx, id, value):
        content = ctx.elements["prompt-texts"]
        content.update(self.texts_func)
        ctx.elements["prompt-input"].focus()

    def texts_func(self):
        with div(id="prompt-texts").cls("prompt-texts row") as text_section:
            for text in self.texts:
                self.text_comp(text)
            self.prompt_input = input(id="prompt-input", placeholder = "Write Your Prompt Here ...").on("change", self.on_change)
        return text_section                    

    def text_comp(self, value):
        text(value, id="prompt-text-" + value).cls("border").on("click", self.pop)

    def pop(self,ctx, id, value):
        self.texts.remove(value)
        self.update_content(ctx, id, value)

    def on_change(self,ctx, id, value):
        if value != "" and value not in self.texts:
            split_coma = value.split(",")
            for text in split_coma:
                trimmed_text = text.strip()
                if trimmed_text != "" and trimmed_text not in self.texts:
                    self.texts.append(trimmed_text)
            self.update_content(ctx, id, value)
            self.prompt_input.value = ""

    def get_string(self):
        return ",".join(self.texts)

    def init(self):
        self.session.queue_for_send("init-prompt", {"inputID": "prompt-input", "historyID": "history-list"},"init-prompt")
        self.prompt_input.on("pop", lambda ctx, id, value: self.pop(ctx, id, self.texts[-1]))