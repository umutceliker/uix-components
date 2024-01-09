import uix

from uix.elements import grid, col, button

from src.uix_components import basic_slider, component_list

def basic_slider_example():
    return basic_slider(name="Deneme", id = "mySlider", callback = lambda ctx, id, value: print(f"Slider {id} changed to: {value}"))

def comp1():
    def callback(ctx, id, value):
        print(f"Slider {id} changed to: {value}")
    basic_slider(name="Deneme1", id = "mySlider1", callback = callback)

def comp2():
    def callback(ctx, id, value):
        print(f"Slider {id} changed to: {value}")
    basic_slider(name="Deneme2", id = "mySlider2",callback=callback)

def component_list_example():
    return component_list(id = "comp_main", components = [comp1,comp2])

examples = { "Slider Example": basic_slider_example,
            "Component List Example": component_list_example}


def on_change_example(ctx, id, value):
    print("Example =", value)
    content = ctx.elements["content"]
    if value in examples:
        content.update(examples[value])
    


with grid("",columns = "1fr 5fr") as main:
    with col() as menu:
        menu.cls("border")
        button("Slider Example", id = "slider_example").on("click", on_change_example)
        button("Component List Example", id = "comp_list_example").on("click", on_change_example)
    with col(id = "content") as content:
        content.cls("container border")
        basic_slider_example()



uix.start(ui=main, config={"debug": True})