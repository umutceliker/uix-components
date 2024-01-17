event_handlers["init-seadragon"] = function (id, value, event_name) {
    console.log(value);
    let config = value
    let viewerConfig = {
        id: id,
        prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/images/",
        animationTime: 0,
        maxZoomPixelRatio: 4,
        tileSources : {"type": "image","url": config.image},
        showNavigationControl: config.hasButtons,
        zoomInButton: undefined,
        zoomOutButton: null,
        homeButton: null,
        fullPageButton: null,
    };

    document.getElementById(id).viewerConfig = config;
    document.getElementById(id).viewer = OpenSeadragon(viewerConfig);

   let viewer = document.getElementById(id).viewer;
   createIcons(viewer);
}

function createIcons(viewer) {
    console.log("create icons")
    viewer.buttonGroup.buttons = [];
    viewer.buttonGroup.element.innerHTML = "";
    buttons = [
        ["zoom-in", "Zoom in"],
        ["zoom-out", "Zoom out"],
        ["home", "Home"],
        ["fullscreen", "Full Page"],
        ["download", "Download"],
        ["save", "Save"],
    ];
    buttons.forEach(function (button) {
        viewer.buttonGroup.buttons.push(createIcon(viewer.element.id, button[0], button[2]));
        
    });
}

function createIcon(id, name, tooltip) {
    const width = "25px";
    const height = "25px";
    const padding = "5px";
    const backgroundColor = "var(--background-mask)";
    const backgroundBlur = "blur(5px)";
    const config = document.getElementById(id).viewerConfig;
    const viewer = document.getElementById(id).viewer;
    image_url = window.location + config.prefixUrl + "ivb_" + name;

    button_click = function (event) {
        clientEmit(id, name, "button_click")
    }
    let button = new OpenSeadragon.Button({
        tooltip: tooltip,
        srcRest: image_url + ".svg",
        srcGroup: image_url + ".svg",
        srcHover: image_url + "-hover.svg",
        srcDown: image_url + "-hover.svg",
        onClick: button_click
    });
    viewer.buttonGroup.element.appendChild(button.element);
    ['imgRest', 'imgGroup','imgHover', 'imgDown'].forEach(imgType => {
        button[imgType].style.width = width;
        button[imgType].style.height = height;
        button[imgType].style.padding = padding;
        button[imgType].style.backgroundColor = backgroundColor;
    });
    return button;
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