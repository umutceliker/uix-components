from uix.elements import select, option

class basic_select(select):
    def __init__(
            self,
            id=None,
            value=None,
            options : dict[str, str] = None,
            callback=None,
            **kwargs
        ):
        super().__init__( id=id, **kwargs)
        self.options = options
        self.callback = callback
        self.value = value

        with self.on("change", self.on_change):    
            if type(self.options) == list:
                for _option in self.options:
                    if _option["isSelect"] == True:
                        option(id=_option['id'], value=_option['id'], text=_option['value']).selected()
                    else:
                        option(id=_option['id'], value=_option['id'], text=_option['value'])
            else:
                for key, value in self.options.items():
                    if value["isSelect"] == True:
                        option(value=key, id=value["id"], text=value["value"]).selected()
                    else:
                        option(value=key, id=value["id"], text=value["value"])

    def on_change(self, ctx, id, value):
        self.value = value
        if self.callback:
            self.callback(ctx, id, value)