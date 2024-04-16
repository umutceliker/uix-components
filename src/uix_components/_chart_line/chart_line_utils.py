import numpy as np

class ChartUtils:
    @staticmethod
    def set_options(chart_data, options):
        for key, value in options.items():
            switcher = {
                "responsive": ChartUtils.set_responsive,
                "legend_pos": ChartUtils.set_legend_pos,
                "title": ChartUtils.set_title,
                "tension": ChartUtils.set_tension,
                "dataset_labels": ChartUtils.set_dataset_labels,
            }
            func = switcher.get(key, lambda: "Invalid option")
            func(chart_data, value)
                
    @staticmethod
    def set_responsive(chart_data, value):
        if isinstance(value, bool):
            chart_data["options"] = {"responsive": value}
        else:
            print("Responsive must be bool")

    @staticmethod
    def set_dataset_labels(chart_data, value):
        dataset_length = len(chart_data["data"]["datasets"])
        for index in range(dataset_length):
            if len(value) > index:
                chart_data["data"]["datasets"][index]["label"] = value[index]
                        
    @staticmethod
    def set_legend_pos(chart_data, value):
        chart_data["options"]["plugins"] = {"legend": {}}
        chart_data["options"]["plugins"]["legend"]["position"] = value.lower()
        
    @staticmethod
    def set_title(chart_data, value):
        chart_data["options"]["plugins"]["title"] = {"display": True, "text": value}

    @staticmethod
    def set_tension(chart_data, value):
        dataset_length = len(chart_data["data"]["datasets"])
        for i in range(dataset_length):
            chart_data["data"]["datasets"][i]["tension"] = value
    
    @staticmethod
    def dataset_importer(chart_data, value, labels=None):
        dimension = 0
        if isinstance(value, dict):
            chart_data["data"]["labels"].clear()
            chart_data["data"]["datasets"].clear()
            for val in value.values():
                if isinstance(val, dict):
                    ChartUtils.add_dataset(chart_data, val, dimension)
                    dimension += 1
                else:
                    ChartUtils.add_dataset(chart_data, value, dimension)
                    break
        else:
            chart_data["data"]["datasets"].clear()
            if isinstance(value[0], (list, tuple)):
                dimension = len(value)
                for i, data in enumerate(value):
                    ChartUtils.add_dataset(chart_data, data, i)
            else:
                ChartUtils.add_dataset(chart_data, value, 0)
            if labels is None:
                label_length = len(value) if dimension == 0 else len(value[0])
                chart_data["data"]["labels"] = [i+1 for i in range(label_length)]
            else:
                chart_data["data"]["labels"] = labels

    @staticmethod
    def add_dataset(chart_data, data, index):
        random_color = np.random.randint(0, 255, 3)
        random_border_color = f"rgba({random_color[0]},{random_color[1]},{random_color[2]},1)"
        chart_data["data"]["datasets"].append({
            "label": f"{index+1}. Dataset",
            "borderColor": random_border_color,
            "borderWidth": 2,
            "data": data,
            "tension": 0.1
        })
