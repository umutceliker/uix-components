import uix

class component_list(uix.Element):
    def __init__(self, id,components = []):
        super().__init__(id = id)
        with self:
            for component in components:
                component()

