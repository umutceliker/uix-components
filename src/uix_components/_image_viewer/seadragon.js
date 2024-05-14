
event_handlers["init-seadragon"] = function (id, value, event_name) {
    let config = value

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

    if (config.buttonGroup !== null) {
        createIcons(viewer, config.buttonGroup);
    }
}

function createIcons(viewer,config) {
    clearButtonGroupElements(viewer.buttonGroup);
    viewer.buttonGroup.element.style.display = "flex";
    viewer.buttonGroup.element.style.flexDirection = "row";

    buttons = config

    for (const [key, value] of Object.entries(buttons)) {
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
    const display = "flex";
    const justifyContent = "center";
    const alignItems = "center";
    image_url = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/webfonts/fa-solid-900.svg"
    
    button_click = function (event) {
        clientEmit(id, name, "button_click");
    }

    let button = new OpenSeadragon.Button({
        tooltip: name,
        srcRest: image_url,
        srcGroup: image_url,
        srcHover: image_url,
        srcDown: image_url,
        onClick: button_click,
    });

    button.element.style.width = width;
    button.element.style.height = height;
    button.element.style.padding = padding;
    button.element.style.backgroundColor = backgroundColor;
    button.element.style.backgroundBlur = backgroundBlur;
    button.element.style.display = display;
    button.element.style.justifyContent = justifyContent;
    button.element.style.alignItems = alignItems;

    const iconElement = document.createElement('i');
    iconElement.classList.add('fas'); // Add FontAwesome base class
    
    iconClasses.split(' ').forEach(iconClass => {
        iconElement.classList.add(iconClass);
    });
    
    if (value.icon_styles){
        applyStyles(iconElement, value.icon_styles);
    }

    clearButtonGroupElements(button);
    button.element.appendChild(iconElement);
    viewer.buttonGroup.element.appendChild(button.element);
    
    return button;
}
function clearButtonGroupElements(button) {
    const buttonGroupElement = button.element;
    while (buttonGroupElement.firstChild) {
        buttonGroupElement.removeChild(buttonGroupElement.firstChild);
    }

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

        case "zoomIn":
            viewer.viewport.zoomBy(1.5);
            break;
        
        case "zoomOut":
            viewer.viewport.zoomBy(0.5);
            break;

        case "home":
            viewer.viewport.goHome();
            break;
        
        case "fullscreen":
            if (viewer.isFullPage()) {
                viewer.setFullScreen(false);
                return;
            }
            viewer.setFullScreen(true);
            break;

        case "download":
            downloadFullImage();
            break;
    }
    function genRandomNumbers(){
        const array = new Uint32Array(10);
        crypto.getRandomValues(array);
        return Array.from(array).map(n => n.toString(16)).join('');
    };
    function downloadFullImage() {
        const viewer = document.getElementById(id).viewer;
        let tileSources = viewer.world.getItemAt(0).source;
        let imageUrl = tileSources.url || tileSources[0].url;

        if (!imageUrl) {
            console.error('Full image URL not found');
            return;
        }

        var link = document.createElement('a');
        link.href = imageUrl;
        const fileExtension = imageUrl.split('.').pop();
        link.download = `${genRandomNumbers()}.${fileExtension}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}