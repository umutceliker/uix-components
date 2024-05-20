import uix
from uix.elements import canvas
from uix_components._chart_bar.chart_utils import ChartUtils

uix.html.add_script("chart-js","""
    event_handlers["init-chart"] = function (id, value, event_name) {
        let chart = new Chart(id, value);
        elm = document.getElementById(id);
        elm.chart = chart;
    };
""",False)

class chart_bar(uix.Element):
    def __init__(self, id, value=None, labels=None, options=None):
        super().__init__(id=id, value=value)
        self._value = value
        self.value_name = None
        self.labels = labels
        self.options = options
        self.canvas_id = id+"_canvas"

        self.chartData ={
            "type": "bar",
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
        self.init()    
        self.update()