import random
import uix
from uix.elements import canvas, row, button, div

uix.html.add_script_source('chart.umd.js', 'chart.umd.js',localpath=__file__, beforeMain=False)
uix.html.add_script_source('chart-js', 'chart.js',localpath=__file__, beforeMain=False)

class chart(uix.Element):
    def __init__(self, id, type = "line", value=None):
        super().__init__(id=id, value=None)
        self.type = type
        self.canvas_id = id+"_canvas"
        with self:
            self.canvas = canvas(id=self.canvas_id,value = value)

    def init(self):
        self.session.queue_for_send(self.canvas_id, self.canvas.value, "init-chart")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        with self:
            self.canvas = canvas(id=self.canvas_id,value = value)
        self.update()




if __name__ == "__main__":
    chart_index = 0
    data1 = [65, 59, 80, 81, 56, 55]
    data2 = [15, 59, 20, 81, 26, 55]

    # Create 100 points of random data
    scatter_data1 = []
    scatter_data2 = []

    for i in range(100):
        scatter_data1.append({"x": random.randint(0, 100),"y": random.randint(0, 100)})
        scatter_data2.append({"x": random.randint(0, 100),"y": random.randint(0, 100)})

    charts = [
        {
            "type": "bar",
            "data": {
                "labels": ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
                "datasets": [{
                    "label": "# of Votes",
                    "data": data1,
                }]
            }
        },
        {
            "type": "line",
            "data": {
                "labels": ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
                "datasets": [{
                    "label": "Lines",
                    "data": data2,
                }]
            }
        },
        {
            "type": "bubble",
            "data": {
                "datasets": [{
                    "label": "Bubble Dataset",
                    "data": [{"x":12,"y":34,"r":10},
                             {"x":22,"y":13,"r":15},
                             {"x":32,"y":12,"r":5}],
                }]
            }
        },
        {
            "type": "scatter",
            "data": {
                "datasets": [{
                    "label": "Scatter Dataset 1",
                    "data": scatter_data1,
                    "backgroundColor": 'rgb(255, 99, 232)'
                },
                {
                    "label": "Scatter Dataset 2",
                    "data": scatter_data2,
                    "backgroundColor": 'rgb(255, 199, 132)'
                }],
                
            }
        }]
    

    def update(ctx,id,value):
        global chart_index
        chart_index = int(id[-2:])
        print("update",chart_index)
        
        ctx.elements["chart1"].value = charts[chart_index]


    with div("") as main:
        with row():
            button(id = "btn_00", value = "Bar").on("click", update)
            button(id = "btn_01", value = "Line").on("click", update)
            button(id = "btn_02", value = "Bubble").on("click", update)
            button(id = "btn_03", value = "Scatter").on("click", update)

        chart(id = "chart1", value=charts[chart_index])
    uix.start(ui=main, config={"debug": True})