# from ._basic_slider._basic_slider import basic_slider
# from ._component_list._component_list import component_list
# from ._basic_checkbox._basic_checkbox import basic_checkbox
# from ._basic_select._basic_select import basic_select
# from ._basic_dialog._basic_dialog import basic_dialog
# from ._basic_datalist._basic_datalist import basic_datalist
# from ._basic_loading._basic_loading import basic_loading
# from ._basic_imagecard._basic_imagecard import basic_imagecard
# from ._basic_prompt._basic_prompt import basic_prompt
# from ._basic_details._basic_details import basic_details
# from ._basic_alert._basic_alert import basic_alert
# from ._credit_card._credit_card import credit_card
# from ._image_viewer._image_viewer import image_viewer
# from ._basic_tree_view._basic_tree_view import basic_tree_view
# from ._chart._chart import chart
# from ._tooltip._tooltip import tooltip
# from ._button_group._button_group import button_group
# from ._address_form._address_form import address_form
# from ._fabric._fabric import fabric
# from ._toggle_checkbox._toggle_checkbox import toggle_checkbox
# from ._chart_bar._chart_bar import chart_bar
# from ._chart_line._chart_line import chart_line
# from ._chart_scatter._chart_scatter import chart_scatter
# from ._chart_pie._chart_pie import chart_pie

"""
Elements
========
This module contains all the elements that are used in the UIX library.

"""
import sys
import os
from types import ModuleType
import importlib
__modules = []
print("uix_components",__file__)
for _folder_name in os.listdir(os.path.dirname(__file__)):
    if _folder_name.startswith("_") and _folder_name != "__init__.py" and _folder_name != "__pycache__":
        __modules.append(_folder_name[1:])

def __getattr__(name):
    if name in __modules:
        module_name=f"uix_components._{name}._{name}"
        module = importlib.import_module(module_name)
        attr = getattr(module, name)
        return attr
    raise AttributeError(f"module {__name__} has no attribute {name}")
    

__all__ = list(__modules)
__version__ = "0.1.0"
def __dir__():
    """Just show what we want to show."""
    result = list(__modules)
    result.extend(
        (
            "__file__",
            "__doc__",
            "__all__",
            "__docformat__",
            "__name__",
            "__path__",
            "__package__",
            "__version__",
        )
    )
    return result