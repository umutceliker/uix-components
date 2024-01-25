event_handlers["init-seadragon"] = function (id, value, event_name) {
    let config = value
    console.log("init-seadragon", id, config.buttonGroup, event_name);
    let viewerConfig = {
        id: id,
        prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/images/",
        animationTime: 0,
        maxZoomPixelRatio: 4,
        tileSources : {"type": "image","url": config.image},
        showNavigationControl: true,
    };

    document.getElementById(id).viewerConfig = config.buttonGroup;
    document.getElementById(id).viewer = OpenSeadragon(viewerConfig);

   let viewer = document.getElementById(id).viewer;

createIcons(viewer,config.buttonGroup);
}

function createIcons(viewer,config) {
    console.log("create icons")
    
    console.log("create icons", config)
    viewer.buttonGroup.buttons = [];
    const buttonGroupElement = viewer.buttonGroup.element;
    while (buttonGroupElement.firstChild) {
        buttonGroupElement.removeChild(buttonGroupElement.firstChild);
    }
    viewer.buttonGroup.element.innerHTML = "";

    buttons = config
    // for (const [key, value] of Object.entries(buttons)) {
    //     console.log(key, value);
    //   }
    for (const [key, value] of Object.entries(buttons)) {
        console.log(key, value, "create icons");
        let button = createIcon(viewer.id, key, value, value.icon);
    
        viewer.buttonGroup.buttons.push(button);
    }
}
function applyStyles(element, styles) {
    for (const [property, value] of Object.entries(styles)) {
        element.style[property] = value;
    }
    element.addEventListener('mouseover', function() {
        element.style.filter = 'brightness(1.5)'; // Add a filter on mouseover
    });
    element.addEventListener('mouseout', function() {
        element.style.filter = 'brightness(1)'; // Remove the filter on mouseout
    });
}
function createIcon(id, name, value, iconClasses) {
    const viewer = document.getElementById(id).viewer;
    const width = "25px";
    const height = "25px";
    const padding = "5px";
    const backgroundColor = "var(--background-mask)";
    const backgroundBlur = "blur(5px)";

    button_click = function (event) {
        clientEmit(id, name, "button_click");
    }

    let button = new OpenSeadragon.Button({
        tooltip: name,
        onClick: button_click,
    });

    button.element.style.width = width;
    button.element.style.height = height;
    button.element.style.padding = padding;
    button.element.style.backgroundColor = backgroundColor;
    button.element.style.backgroundBlur = backgroundBlur;

    const iconElement = document.createElement('i');
    iconElement.classList.add('fas'); 
    iconElement.classList.add(value.icon)// Add FontAwesome base class
    
    
    if (value.icon_styles){
        applyStyles(iconElement, value.icon_styles);
    }

    clearButtonGroupElements(button);
    button.element.appendChild(iconElement);
    viewer.buttonGroup.element.appendChild(button.element);
    
    return button;
}

function clearButtonGroupElements(button) {

   console.log("clearButtonGroupElements", button)
    const buttonGroupElement = button.element;
    while (buttonGroupElement.firstChild) {
        buttonGroupElement.removeChild(buttonGroupElement.firstChild);
    }

    console.log("clearButtonGroupElements5", button)
}

event_handlers["seadragon"] = function (id, command, event_name) {
    const viewer = document.getElementById(id).viewer;
    switch (command.action) {
        case "open":
            viewer.open(command.value);
            break;
        case 'close':
            viewer.close();
            break;
        case "set-scroll-zoom":
            const cmd = command.value === "true";
            viewer.gestureSettingsMouse.scrollToZoom = cmd;
            viewer.gestureSettingsMouse.clickToZoom = cmd;
            viewer.gestureSettingsMouse.dragToPan = cmd;
            break;
    }
}