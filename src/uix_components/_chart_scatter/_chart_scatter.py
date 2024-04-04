import uix
from uix.elements import canvas
from uix_components._chart_scatter.chart_scatter_utils import ChartUtils

uix.html.add_script("chart-js","""
    event_handlers["init-chart"] = function (id, value, event_name) {
        let chart = new Chart(id, value);
        elm = document.getElementById(id);
        elm.chart = chart;
    };
""",False)

class chart_scatter(uix.Element):
    def __init__(self, id, value=None, options=None):
        super().__init__(id=id, value=value)
        self._value = value
        self.value_name = None
        self.options = options
        self.canvas_id = id+"_canvas"

        self.chartData ={
            "type": "scatter",
            "data": {
                "datasets": [
                ],
            },
            "options": {
                "scales": {
					"x": {
						"type": "linear",
						"position": "bottom"
					},
				},
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
  
        ChartUtils.dataset_importer(self.chartData, self.value)
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
        ChartUtils.dataset_importer(self.chartData, value)
        ChartUtils.set_options(self.chartData, self.options)
        with self:
            self.canvas = canvas(id=self.canvas_id,value = self.chartData)
        self.update()

title = "Chart Scatter"
description = """
# chart_line(id, value=None, options=None)
1. Chart Line bir chart komponentidir.
    | attr          | desc                                                              |
    | :------------ | :---------------------------------------------------------------  |
    | id            | Komponentin id'si                                                 |
    | value         | Chart verisi                                                      |
    | options       | Chart'ın opsiyonları                                              |
    
```python
    #options kullanım örneği:
    options = {
        "responsive" : True,    #Pencere boyutu değiştiğinde chart'ın yeniden boyutlandırılması
        "legend_pos" : "Top",   #Grafikte görünen veri kümlerinin açıklamalarının konumu(örn: 1.Dataset)
        "title" : "2024"        #Grafik başlığı
        }
```

```python
    #value kullanım örnekleri:
	value = [{'x':-10, 'y':0}, {'x':0, 'y':10}, {'x':10, 'y':5}, {'x':0.5, 'y':5.5}]
	# Scatter Chart'ı kullanmak için verilerin X ve Y özelliklerini içeren nesneler olarak iletilmesi gerekir.
	# Yukarıdaki örnek 4 noktalı bir scatter grafiği oluşturur.
```
"""
sample="""
import uix
import random
from uix.elements import button,row
from uix_components import chart_scatter
from uix_components._chart_scatter._chart_scatter import title, description, sample as code

scatter1= [{
      'x': -10,
      'y': 0
    }, {
      'x': 0,
      'y': 10
    }, {
      'x': 10,
      'y': 5
    }, {
      'x': 0.5,
      'y': 5.5
    }]
scatter2 = [{'x': random.uniform(-20, 20), 'y': random.uniform(-20, 20)} for _ in range(100)]

options = {
    "responsive": True,
    "legend_pos": "top",
    "title": "Burası Başlık",
}

charts = [scatter1,scatter2]
button_value =["Scatter1","Scatter2"]
chart_index = 0 
def update(ctx,id,value):
    global chart_index
    chart_index = int(id[-1:])
    ctx.elements["chart1"].value = charts[chart_index]

def chart_scatter_example():
    with uix.elements.border().size("100%","fit-content").style("overflow-y","auto") as main:
        with row().size("100%","50px").style("gap","10px"):
            for i in range(len(button_value)):
                button(id = f"btn_0{i}", value = button_value[i]).on("click", update)
        chart_scatter(id = "chart1", value=charts[chart_index], options=options).size("90%","90%").cls("border")
"""