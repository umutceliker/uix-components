import uix 
from uix.elements import table, th, tr, td, thead, tbody

class basic_table(uix.Element):
    def __init__(self, id=None, headers=[], data=[]):
        super().__init__(id=id)
        self.style("overflow: auto;")
        with self:
            with table(""):
                with thead():
                    with tr():
                        for header in headers:
                            th(value=header)
                with tbody():
                    for row in data:
                        with tr():
                            for cell in row:
                                td(value=cell)
