import uix
from uix.elements import option, datalist, input

class basic_datalist(uix.Element):
    def __init__(self, name, value=None, id=None, options : dict[str, str] = None, callback=None, placeholder=None, required:bool = False , **kwargs):
        super().__init__(name, id=id, **kwargs)
        self.options = options
        self.datalistID = id + "-datalist"
        self.inputID = id + "-input"
        self.callback = callback
        self.placeholder = placeholder
        self.required = required
        
        with self:
            self.input = input(value="", 
                               id=self.inputID, 
                               type="text", 
                               list=self.datalistID, 
                               placeholder=self.placeholder,
                               required=self.required).on("change", self.on_dlist_change)
            
            with datalist(id=self.datalistID) as self.datalist:
                if type(self.options) == list:
                    for _option in self.options:
                        option(id=_option, value=_option)
                else:
                    for key, value in self.options.items():
                        option(value=value, id=key)
            
    def on_dlist_change(self, ctx, id, value):
        if self.callback:
            self.callback(ctx, id, value)