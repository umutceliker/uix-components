let ORIGINAL_SCALE = 0.3;
let currentScale = ORIGINAL_SCALE;
let brushSize = 140;

const MIN_SCALE = 0.15;
const MAX_SCALE = 5;

fabric.Object.prototype.hoverCursor = 'default';

event_handlers["init-image-cropper"] = function (id, value, event_name) {
  let canvas = new fabric.Canvas(id);
  let firstParent = document.getElementById(id).parentElement;
  let parentElement = firstParent.parentElement; 


  document.getElementById(id).canvas = canvas;
  document.getElementById(id).image = null;
  document.getElementById(id).patternGroup = null;
  document.getElementById(id).lastModified = { x: null, y: null };
  document.getElementById(id).latestCombinedImage = null;
  document.getElementById(id).moveRates = { x: 1, y: 1 };
  document.getElementById(id).lastAxisMoved = 'x';

  canvas.on('object:added', function(event) {
    // Check if the added object is an image
    if (event.target.type === 'image') {
        clientEmit(id, {"message": "Image loaded"}, "image-loaded");

        // Additional actions here
    } 


});

  canvas.setWidth(parentElement.offsetWidth);
  canvas.setHeight(parentElement.offsetHeight);

  window.addEventListener('resize', function() {
    canvas.setWidth(parentElement.parentElement.offsetWidth);
    canvas.setHeight(   parentElement.parentElement.offsetHeight);
    canvas.renderAll();
    
  });

  canvas.on('mouse:wheel', function (opt) {
    opt.e.preventDefault();
    var delta = opt.e.deltaY;
    var proposedScale = currentScale;
    if (proposedScale >= MIN_SCALE && proposedScale <= MAX_SCALE) {
      currentScale = proposedScale;
      if (typeof repeater_checkbox !== 'undefined' && repeater_checkbox && repeater_checkbox.checked) {
        var zoom = canvas.getZoom();
        zoom *= 0.999 ** delta;
        if (zoom > MAX_SCALE) zoom = MAX_SCALE;
        if (zoom < MIN_SCALE) zoom = MIN_SCALE;

        var center = canvas.getCenter();
        canvas.zoomToPoint({ x: center.left, y: center.top }, zoom);
        let axisToUse = document.getElementById(id).lastAxisMoved;
        let scaleToUse = document.getElementById(id).moveRates[axisToUse];
        updateImagePattern(canvas, document.getElementById(id).image, currentScale, id, axisToUse, scaleToUse);

        if (typeof input_canvas_id !== 'undefined' && input_canvas_id) {
          let inputCanvas = document.getElementById(input_canvas_id).canvas;
          inputCanvas.zoomToPoint({ x: center.left, y: center.top }, zoom);
          updateImagePattern(inputCanvas, document.getElementById(input_canvas_id).image, currentScale, input_canvas_id, axisToUse, scaleToUse);
        }
        return;
      }
      var zoom = canvas.getZoom();
      zoom *= 0.999 ** delta;
      if (zoom > MAX_SCALE) zoom = MAX_SCALE;
      if (zoom < MIN_SCALE) zoom = MIN_SCALE;

      var center = canvas.getCenter();
      canvas.zoomToPoint({ x: center.left, y: center.top }, zoom);
    }


    opt.e.stopPropagation();
  });

  canvas.on('mouse:move', function(opt) {
    if (opt.e.buttons === 1 && !opt.e.ctrlKey) {
      panCanvas(opt.e.movementX, opt.e.movementY);
    }
  });

  canvas.on('touch:drag', function(opt) {
    if (!opt.e.touches) {
      this.lastPosX = undefined;
      this.lastPosY = undefined;
      this.lastDistance = undefined;
    }

    if (opt.e.touches?.length > 0) {
      const isPan = opt.e.touches.length === 1;
      const isPinchZoom = opt.e.touches.length === 2;
  
      if (isPan) {
        const touch = opt.e.touches[0];
        if (this.lastPosX !== undefined && this.lastPosY !== undefined) {
          var deltaX = touch.clientX - this.lastPosX;
          var deltaY = touch.clientY - this.lastPosY;
          panCanvas(deltaX, deltaY);
        }
        this.lastPosX = touch.clientX;
        this.lastPosY = touch.clientY;
      }
  
      if (isPinchZoom) {
        const touch1 = opt.e.touches[0];
        const touch2 = opt.e.touches[1];
  
        const distance = Math.hypot(
          touch2.clientX - touch1.clientX,
          touch2.clientY - touch1.clientY
        );
  
        if (this.lastDistance !== undefined) {
          const deltaDistance = distance - this.lastDistance;
          handlePinchZoom(deltaDistance);
        }
  
        this.lastDistance = distance;
      }
    }
  });

  function panCanvas(deltaX, deltaY) {
    var delta = new fabric.Point(deltaX, deltaY);
    canvas.relativePan(delta);

    if (typeof input_canvas_id !== 'undefined' && input_canvas_id) {
      let inputCanvas = document.getElementById(input_canvas_id).canvas;
      inputCanvas.relativePan(delta);
    }
  }

  function handlePinchZoom(deltaDistance) {
    var proposedScale = currentScale;
    if (proposedScale >= MIN_SCALE && proposedScale <= MAX_SCALE) {
      currentScale = proposedScale;
      if (typeof repeater_checkbox !== 'undefined' && repeater_checkbox && repeater_checkbox.checked) {
        var zoom = canvas.getZoom();
        zoom *= 1 + deltaDistance * 0.01;
        if (zoom > MAX_SCALE) zoom = MAX_SCALE;
        if (zoom < MIN_SCALE) zoom = MIN_SCALE;
  
        var center = canvas.getCenter();
        canvas.zoomToPoint({ x: center.left, y: center.top }, zoom);
        let axisToUse = document.getElementById(id).lastAxisMoved;
        let scaleToUse = document.getElementById(id).moveRates[axisToUse];
        updateImagePattern(canvas, document.getElementById(id).image, currentScale, id, axisToUse, scaleToUse);
  
        if (typeof input_canvas_id !== 'undefined' && input_canvas_id) {
          let inputCanvas = document.getElementById(input_canvas_id).canvas;
          inputCanvas.zoomToPoint({ x: center.left, y: center.top }, zoom);
          updateImagePattern(inputCanvas, document.getElementById(input_canvas_id).image, currentScale, input_canvas_id, axisToUse, scaleToUse);
        }
        return;
      }
      var zoom = canvas.getZoom();
      zoom *= 1 + deltaDistance * 0.01;
      if (zoom > MAX_SCALE) zoom = MAX_SCALE;
      if (zoom < MIN_SCALE) zoom = MIN_SCALE;
  
      var center = canvas.getCenter();
      canvas.zoomToPoint({ x: center.left, y: center.top }, zoom);
  
      if (typeof input_canvas_id !== 'undefined' && input_canvas_id) {
        let inputCanvas = document.getElementById(input_canvas_id).canvas;
        inputCanvas.zoomToPoint({ x: center.left, y: center.top }, zoom);
      }
    }
  }

  event_handlers["repeater-checkbox"](id, value, event_name);
  brush_element_id.addEventListener('change', function (e) {
    brushSize = this.value * 2;
    updateAndMoveImage(id, document.getElementById(id), document.getElementById(id).lastAxisMoved, document.getElementById(id).canvas, document.getElementById(input_canvas_id).scale);
  });

  brush_slider_text_input_id.addEventListener('change', function (e) {
    brush_element_id.value = this.value;
    brush_element_id.dispatchEvent(new Event('change'));
  });

  resetButton=document.getElementById('repeater-tool-reset-button');
  resetButton.addEventListener('click', function (e) {
    brushSize =70 * 2;
    repeater_checkbox.checked = false;    
    updateAndMoveImage(id, document.getElementById(id), document.getElementById(id).lastAxisMoved, document.getElementById(id).canvas, document.getElementById(input_canvas_id).scale);
  });
};


function resetImage(id) {
  const canvas = document.getElementById(id).canvas;
  const originalImage = document.getElementById(id).image;

  document.getElementById(id).lastModified = { x: null, y: null };
  document.getElementById(id).latestCombinedImage = null;

  canvas.clear();
  canvas.add(originalImage);
  canvas.requestRenderAll();
}

event_handlers["image-cropper"] = function (id, command, event_name) {
  switch (command.action) {
    case "loadImage":
      fabric.Image.fromURL(command.value, function (img) {
        document.getElementById(id).canvas.clear();
        // let parentElement = document.getElementById(input_canvas_id).parentElement;
        // parentElement.style.display = "none"
        img.scale(ORIGINAL_SCALE);
        img.set({
          left: (document.getElementById(id).canvas.width - img.width * img.scaleX) / 2,
          top: (document.getElementById(id).canvas.height - img.height * img.scaleY) / 2,
          hasControls: false,
          hasBorders: false,
          lockScalingFlip: true,
          transparentCorners: false,
          noScaleCache: false,
          strokeWidth: 0,
          lockMovementX: true,
          lockMovementY: true,
          patternGroup: true,
          objectCaching: false,
          lockRotation: true
        });
        document.getElementById(id).canvas.add(img);
        document.getElementById(id).image = img;
        document.getElementById(id).latestCombinedImage = img;
        if (id === input_canvas_id)
          updateAndMoveImage(id, document.getElementById(id), 'x', document.getElementById(id).canvas, 1);
      });


      break;
    case "cropAndMove":
      const axis = command.value.axis.toLowerCase();
      const element = document.getElementById(id);
      const canvas = element.canvas;
      const scale = command.value.scale;
      updateAndMoveImage(id, element, axis, canvas, scale);
      break;
    case "resetImage":
      resetImage(id);
    case "close":
      document.getElementById(id).canvas.clear();;
      break;
    default:
      break;
  }
};

event_handlers["repeater-checkbox"] = (id, value, event_name) => {
  if (typeof repeater_checkbox !== 'undefined' && repeater_checkbox) {
    repeater_checkbox.addEventListener('change', function () {
      if (this.checked) {
        let inputCanvas = document.getElementById(input_canvas_id).canvas;
        const imageToUseInput = document.getElementById(input_canvas_id).latestCombinedImage || document.getElementById(input_canvas_id).image;

        let outputCanvas = document.getElementById(output_canvas_id).canvas;
        const imageToUseOutput = document.getElementById(output_canvas_id).latestCombinedImage || document.getElementById(output_canvas_id).image;

        let axisToUse = document.getElementById(output_canvas_id).lastAxisMoved;
        let scaleToUse = document.getElementById(output_canvas_id).moveRates[axisToUse];

        updateImagePattern(inputCanvas, imageToUseInput, currentScale, input_canvas_id, axisToUse, scaleToUse);
        updateImagePattern(outputCanvas, imageToUseOutput, currentScale, output_canvas_id, axisToUse, scaleToUse);

        inputCanvas.remove(document.getElementById(input_canvas_id).image);
        outputCanvas.remove(document.getElementById(output_canvas_id).image);

      } else {
        let inputCanvas = document.getElementById(input_canvas_id).canvas;
        const imageToUseInput = document.getElementById(input_canvas_id).latestCombinedImage || document.getElementById(input_canvas_id).image;

        let outputCanvas = document.getElementById(output_canvas_id).canvas;
        const imageToUseOutput = document.getElementById(output_canvas_id).latestCombinedImage || document.getElementById(output_canvas_id).image;

        inputCanvas.getObjects().forEach(function (obj) {
          if (obj.patternGroup) {
            inputCanvas.remove(obj);
          }
        });
        outputCanvas.getObjects().forEach(function (obj) {
          if (obj.patternGroup) {
            outputCanvas.remove(obj);
          }
        });
        inputCanvas.add(imageToUseInput);
        outputCanvas.add(imageToUseOutput);
        inputCanvas.requestRenderAll();
        outputCanvas.requestRenderAll();
      }

    });

  }
};

// Define a function to update the pattern and perform image movement
const updateAndMoveImage = (id, element, axis, canvas, scale) => {
  const imageToUse = element.latestCombinedImage || element.image;
  element.lastAxisMoved = axis;
  element.scale = scale;
  canvas.clear();

  canvas.getObjects().forEach(obj => {
    if (obj.patternGroup) {
      canvas.remove(obj);
    }
  });

  canvas.add(imageToUse);
  canvas.requestRenderAll();

  moveImage(axis, canvas, element.image, element.scale, id);

  if (repeater_checkbox && repeater_checkbox.checked) {
    element.patternGroup = updateImagePattern(canvas, imageToUse, currentScale, id, axis, element.scale);
    canvas.remove(element.image);
  }
};

function moveImage(axis, canvas, originalImage, reportRate, id) {
  canvas.clear();
  document.getElementById(id).moveRates[axis] = reportRate;

  if (axis === 'x' && document.getElementById(id).moveRates['y'] !== 1) {
    document.getElementById(id).moveRates['y'] = 1;
  } else if (axis === 'y' && document.getElementById(id).moveRates['x'] !== 1) {
    document.getElementById(id).moveRates['x'] = 1;
  }

  const rateX = originalImage.width * document.getElementById(id).moveRates['x'];
  const rateY = originalImage.height * document.getElementById(id).moveRates['y'];

  const finalCanvas = document.createElement('canvas');
  finalCanvas.width = originalImage.width;
  finalCanvas.height = originalImage.height;

  const finalCtx = finalCanvas.getContext('2d');

  finalCtx.drawImage(originalImage._element, rateX, rateY, originalImage.width - rateX, originalImage.height - rateY, 0, 0, originalImage.width - rateX, originalImage.height - rateY);
  finalCtx.drawImage(originalImage._element, 0, rateY, rateX, originalImage.height - rateY, originalImage.width - rateX, 0, rateX, originalImage.height - rateY);
  finalCtx.drawImage(originalImage._element, rateX, 0, originalImage.width - rateX, rateY, 0, originalImage.height - rateY, originalImage.width - rateX, rateY);
  finalCtx.drawImage(originalImage._element, 0, 0, rateX, rateY, originalImage.width - rateX, originalImage.height - rateY, rateX, rateY);


  if (id === input_canvas_id && isBrushChecked.checked) {
    drawRect(finalCtx, originalImage, brushSize, rateX, rateY);
  }

  const expandedImage = new fabric.Image(finalCanvas, {
    left: originalImage.left,
    top: originalImage.top,
    scaleX: originalImage.scaleX,
    scaleY: originalImage.scaleY,
    hasControls: false,
    hasBorders: false,
    lockScalingFlip: true,
    transparentCorners: false,
    noScaleCache: false,
    strokeWidth: 0,
    lockMovementX: true,
    lockMovementY: true,
    lockRotation: true,
  });

  canvas.remove(originalImage);
  if (document.getElementById(id).lastModified[axis]) {
    canvas.remove(document.getElementById(id).lastModified[axis]);
  }


  canvas.add(expandedImage);
  document.getElementById(id).lastModified[axis] = expandedImage;
  document.getElementById(id).latestCombinedImage = expandedImage;
  canvas.requestRenderAll();


}

function updateImagePattern(canvas, originalImage, scale, id, axis, reportRate) {

  const image = document.getElementById(id).latestCombinedImage || originalImage;

  canvas.clear();

  if (image) {

    const scaledWidth = image.width * scale;
    const scaledHeight = image.height * scale;

    const zoomFactor = canvas.getZoom();

    const visibleWidth = canvas.width / zoomFactor;
    const visibleHeight = canvas.height / zoomFactor;

    const cols = Math.ceil(visibleWidth / scaledWidth) * 2 + 1;
    const rows = Math.ceil(visibleHeight / scaledHeight) * 2 + 1;

    const imagesArray = [];

    let offset = 0;

    const loop1 = axis === 'y' ? cols : rows;
    const loop2 = axis === 'y' ? rows : cols;

    for (let i = -Math.floor(loop1 / 2); i <= Math.floor(loop1 / 2); i++) {
      for (let j = -Math.floor(loop2 / 2); j <= Math.floor(loop2 / 2); j++) {
        const clonedImg = fabric.util.object.clone(image);

        let col = axis === 'y' ? i : j;
        let row = axis === 'y' ? j : i;

        let left = (canvas.width - scaledWidth) / 2 + col * scaledWidth;
        let top = (canvas.height - scaledHeight) / 2 + row * scaledHeight;

        if (axis === 'x') {
          left += offset % scaledWidth;
        } else {
          top += offset % scaledHeight;
        }

        clonedImg.set({
          left: left,
          top: top,
          scaleX: scale,
          scaleY: scale,
          hasControls: false,
          hasBorders: false,
          lockScalingFlip: true,
          transparentCorners: false,
          noScaleCache: false,
          strokeWidth: 0,
          lockMovementX: true,
          lockMovementY: true,
          patternGroup: true,
          objectCaching: false,
          lockRotation: true,
        });
        imagesArray.push(clonedImg);
      }


      offset += (axis === 'x' ? scaledWidth : scaledHeight) * reportRate;

    }

    const group = new fabric.Group(imagesArray, {
      hasControls: false,
      hasBorders: false,
      lockScalingFlip: true,
      transparentCorners: false,
      noScaleCache: false,
      strokeWidth: 0,
      lockMovementX: true,
      lockMovementY: true,
      patternGroup: true,
      objectCaching: false,
      lockRotation: true,
    });

    canvas.add(group);

    canvas.requestRenderAll();

    return group;
  }
}


function drawRect(finalCtx, originalImage, brushSize, rateX, rateY) {
  finalCtx.beginPath();

  finalCtx.rect((originalImage.width - rateX) - brushSize / 2, 0, brushSize, originalImage.height);
  finalCtx.rect(0, (originalImage.height - rateY) - brushSize / 2, originalImage.width, brushSize);

  if (originalImage.width - rateX == 0 || rateX == 0) {
    finalCtx.rect((originalImage.width) - brushSize / 2, 0, brushSize, originalImage.height);
    finalCtx.rect(0, 0, brushSize / 2, originalImage.height);
  }
  if (originalImage.height - rateY == 0 || rateY == 0) {
    finalCtx.rect(0, (originalImage.height) - brushSize / 2, originalImage.width, brushSize);
    finalCtx.rect(0, 0, originalImage.width, brushSize / 2);
  }
  finalCtx.fillStyle = 'rgba(0,0,0,0.5)';
  finalCtx.fill();
  finalCtx.closePath();

}
