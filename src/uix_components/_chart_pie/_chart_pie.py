import uix
from uix.elements import canvas
from uix_components._chart_pie.chart_pie_utils import ChartUtils

uix.html.add_script("chart-js","""
    event_handlers["init-chart"] = function (id, value, event_name) {
        let chart = new Chart(id, value);
        elm = document.getElementById(id);
        elm.chart = chart;
    };
""",False)

class chart_pie(uix.Element):
    def __init__(self, id, value=None, labels=None, options=None):
        super().__init__(id=id, value=value)
        self._value = value
        self.value_name = None
        self.labels = labels
        self.options = options
        self.canvas_id = id+"_canvas"

        self.chartData ={
            "type": "pie",
            "data": {
                "labels": [],
                
                "datasets": [
                ],
            },
            "options": {
                "responsive": None,
                "plugins": {
                    "legend": {
                    "position": None,
                    },
                "title": {
                "display": None,
                "text": None
                    }
                }
            }
        }
  
        ChartUtils.dataset_importer(self.chartData, self.value, self.labels)
        ChartUtils.set_options(self.chartData, self.options)
               
        with self:
            self.canvas = canvas(id=self.canvas_id, value=self.chartData)

    def init(self):
        self.session.queue_for_send(self.canvas_id, self.canvas.value, "init-chart")
        
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        ChartUtils.dataset_importer(self.chartData, value, self.labels)
        ChartUtils.set_options(self.chartData, self.options)
        with self:
            self.canvas = canvas(id=self.canvas_id,value = self.chartData)
        self.update()

title = "Chart Pie"
description = """
# chart_bar(id, value=None, labels=None, options=None)

1. Chart Bar bir chart komponentidir.
    | attr          | desc                                                              |
    | :------------ | :---------------------------------------------------------------  |
    | id            | Komponentin id'si                                                 |
    | value         | Chart verisi                                                      |
    | labels        | Chart verilerinin label'ları (x ekseninde altta yazacaklar)       |
    | options       | Chart'ın opsiyonları                                              |
    
```python
    #options kullanım örneği:
    options = {
        "responsive" : True,    #Pencere boyutu değiştiğinde chart'ın yeniden boyutlandırılması
        "legend_pos" : "Top",   #Grafikte görünen veri kümlerinin açıklamalarının konumu(örn: 1.Dataset)
        "title" : "2024"        #Grafik başlığı
        "backgroundColor": [	#Grafikteki veri kümlerinin arkaplan rengi
        	"rgb(255, 99, 132)",
        	"rgb(54, 162, 235)",
        	"rgb(255, 205, 86)",
        	"rgb(75, 192, 192)",
        	"rgb(153, 102, 255)"
    	]
        
        }
```
```python
    #labels kullanım örneği:
    labels = ["ocak","şubat","mart","nisan","mayıs"]
    #Eğer labels parametresi verilmezse chart'ın x ekseninde 1'den başlayarak veri sayısı kadar sayılar otomatik yazılır.
```
```python
    #value kullanım örnekleri:
    #value tuple olabilir, list olabilir.
    #value = [1, 2, 3, 4, 5]
```
"""
sample="""
import uix
import numpy as np
from uix.elements import button,row
from uix_components import chart_pie
from uix_components._chart_pie._chart_pie import title, description, sample as code

tupple1 = (1, 2, 3, 4, 5)
tupple2 = ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10],[3,6,3,7,3])
tupple3 = ((1, 2, 3, 4, 5), (6, 7, 8, 9, 10),(3,6,3,7,3))

list1 = [1, 2, 3, 4, 5]
list2 = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10],[3,6,3,7,3]]
list3 = [(1, 2, 3, 4, 5), (6, 7, 8, 9, 10),(3,6,3,7,3)]

label1 = ["ocak","şubat","mart","nisan","mayıs"]

options = {
    "responsive": True,
    "legend_pos": "top",
    "title": "Burası Başlık",
    "backgroundColor": [
        "rgb(255, 99, 132)",
        "rgb(54, 162, 235)",
        "rgb(255, 205, 86)",
        "rgb(75, 192, 192)",
        "rgb(153, 102, 255)"
    ]
}

charts = [tupple1,tupple2,tupple3,list1,list2,list3]
button_value =["Tuple1","Tuple2","Tuple3","List1","List2","List3"]
chart_index = 0
def update(ctx,id,value):
    global chart_index
    chart_index = int(id[-1:])
    ctx.elements["chart1"].value = charts[chart_index]

def chart_pie_example():
    with uix.elements.border().size("100%","fit-content").style("overflow-y","auto") as main:
        with row().size("100%","50px").style("gap","10px"):
            for i in range(len(button_value)):
                button(id = f"btn_0{i}", value = button_value[i]).on("click", update)
        chart_pie(id = "chart1", value=charts[chart_index], options=options, labels=label1).size("50%","50%").cls("border")
"""