import numpy as np

class ChartUtils:
    @staticmethod
    def set_options(chart_data, options):
        for key, value in options.items():
            switcher = {
                "responsive": ChartUtils.set_responsive,
                "legend_pos": ChartUtils.set_legend_pos,
                "title": ChartUtils.set_title,
                "backgroundColor": ChartUtils.set_background_color,
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
    def set_legend_pos(chart_data, value):
        chart_data["options"]["plugins"] = {"legend": {}}
        chart_data["options"]["plugins"]["legend"]["position"] = value.lower()
        
    @staticmethod
    def set_title(chart_data, value):
        chart_data["options"]["plugins"]["title"] = {"display": True, "text": value}

    @staticmethod
    def set_background_color(chart_data, value):
        dataset_length = len(chart_data["data"]["datasets"])
        for i in range(dataset_length):
            chart_data["data"]["datasets"][i]["backgroundColor"] = value

    @staticmethod
    def set_dataset_labels(chart_data, value):
        dataset_length = len(chart_data["data"]["datasets"])
        for index in range(dataset_length):
            if len(value) > index:
                chart_data["data"]["datasets"][index]["label"] = value[index]
    
    @staticmethod
    def dataset_importer(chart_data, value, labels=None):
        dimension = 0
        if isinstance(value, dict):
            chart_data["data"]["labels"].clear()
            chart_data["data"]["datasets"].clear()
            for val in value.values():
                if isinstance(val, dict):
                    dataset_label = (list(value.keys())[dimension])
                    ChartUtils.add_dataset(chart_data, val, dataset_label)
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
    def add_dataset(chart_data, data, dataset_label):
        data_length = len(data)
        random_background_color = []
        for i in range(data_length):
            random_color = np.random.randint(0, 255, 3)
            random_background_color.append(f"rgb({random_color[0]}, {random_color[1]}, {random_color[2]}")
        chart_data["data"]["datasets"].append({
            "label": f"{dataset_label+1}. Dataset" if isinstance(dataset_label, int) else dataset_label,
            "backgroundColor": random_background_color,
            "hoverOffset": 4,
            "data": data,
        })
