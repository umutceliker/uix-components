import numpy as np

class ChartUtils:
    @staticmethod
    def set_options(chart_data, options):
        for key, value in options.items():
            switcher = {
                "responsive": ChartUtils.set_responsive,
                "legend_pos": ChartUtils.set_legend_pos,
                "title": ChartUtils.set_title,
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
    def dataset_importer(chart_data, value):
        dimension = 0
        if isinstance(value, dict):
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
    @staticmethod
    def add_dataset(chart_data, data, index):
        random_color = np.random.randint(0, 255, 3)
        random_background_color = f"rgba({random_color[0]},{random_color[1]},{random_color[2]},1)"
        chart_data["data"]["datasets"].append({
            "label": f"{index+1}. Dataset",
            "backgroundColor": random_background_color,
            "data": data
        })
