from uix.elements import table, tr, th, td, div, button, input, span,thead, tbody,icon
from uix.core.session import context
import types
import uix
import json
import html


uix.html.add_css_file('datatables.css', __file__)
uix.html.add_script_source('data-table-js', 'datatables.min.js', localpath=__file__)
uix.html.add_script_source('data-table-init-js', 'datatable_comp.js', localpath=__file__, beforeMain=False)


class data_table(uix.Element):
    def __init__(self, id=None, data=[],cols=None,dialog_id=None,callback=None,config=None):
        super().__init__(id=id)
        columns = []
        self.id = id
        self.config = {
            "data":  data,
            "columns": columns,
            "dataTable_config": config,
            "dialog_id": dialog_id,
            "isEditable": False
        }
        
        if callback and dialog_id:
            self.config["isEditable"] = True
            context.session.context.elements[dialog_id].on("info_dialog_open", callback)
        
        with self:
            with table(id=self.id + "-table",value="").cls("stripe hover"):
                with thead():
                    with tr():
                        if cols:
                            for key, value in cols.items():
                                columns.append({"data": key})
                                th(value)
                        else:
                            for key in data[0].keys():
                                columns.append({"data": key})
                                th(key)

                        
                    
    def init(self):
        self.session.send(self.id+"-table", self.config ,"init-data-table")

    def update_table(self,value):
         self.config["data"] = value
         self.session.send(self.id+"-table", self.config,"reload")
