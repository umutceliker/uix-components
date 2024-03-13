var canvas = null; 
var paddingValue = 20;
var croppedImageUrl = null;

event_handlers["init-cropper"] = (id, value, event_name) => {
    const doneButton = document.getElementById('doneButton');
    
    if (!canvas) { // Eğer canvas daha önce oluşturulmamışsa
        canvas = new fabric.Canvas(value.cropCanvas);
        canvas.background = '#FFFFFF';
        canvas.renderAll();
    }

    fabric.Image.fromURL(value.imageUrl, function (oImg) {
        // Calculate the maximum dimensions while maintaining aspect ratio
        var maxWidth = canvas.width - paddingValue;
        var maxHeight = canvas.height - paddingValue;
        var imgWidth = oImg.width;
        var imgHeight = oImg.height;
        var ratio = 1;
    
        // Calculate the ratio to fit the image within canvas bounds
        if (imgWidth > maxWidth || imgHeight > maxHeight) {
            var widthRatio = maxWidth / imgWidth;
            var heightRatio = maxHeight / imgHeight;
            ratio = Math.min(widthRatio, heightRatio);
        }
    
        // Resize the image
        oImg.scale(ratio);
    
        // Position the image in the center of the canvas
        oImg.set({
            left: (canvas.width - oImg.width * ratio) / 2,
            top: (canvas.height - oImg.height * ratio) / 2
        });
    
        canvas.clear(); // Clear previous content
        canvas.add(oImg); // Add the resized image to the canvas
        canvas.setPadding(20);
        canvas.renderAll(); 
    });

    canvas.on('object:moving', function(e) {
        const target = e.target;
        const canvasWidth = canvas.getWidth();
        const canvasHeight = canvas.getHeight();
        
        //target.lockRotation = true; // Resmi döndürmeyi kapat
        //target.hasControls = false; // Nesnenin döndürme kollarını devre dışı bırak
        //target.lockScalingX = true; // Resmi boyutlandırmayı kapat
        //target.lockScalingY = true; // Resmi boyutlandırmayı kapat
      
        if (target.left < paddingValue / 2) {
          target.left = paddingValue / 2;
        }
        if (target.top < paddingValue / 2) {
          target.top = paddingValue / 2;
        }
        if (target.left + target.width * target.scaleX > canvasWidth) {
          target.left = (canvasWidth - target.width * target.scaleX) - paddingValue / 2;
        }
        if (target.top + target.height * target.scaleY > canvasHeight) {
          target.top = (canvasHeight - target.height * target.scaleY) - paddingValue / 2;
        }
        canvas.renderAll();
      });
    

    canvas.on({
    'mouse:dblclick': function(obj){ 
        var target = obj.target ? obj.target : null;
        if(target && target.type === 'image'){
        prepareCrop(target);
    }}});

    function prepareCrop(e){
    var i = new fabric.Rect({
        id: "crop-rect",
        top: e.top,
        left: e.left,
        angle: e.angle,
        width: e.getScaledWidth(),
        height: e.getScaledHeight(),
        stroke: "rgb(42, 67, 101)",
        strokeWidth: 2,
        strokeDashArray: [5, 5],
        fill: "rgba(255, 255, 255, 1)",
        globalCompositeOperation: "overlay",
        lockRotation: true,
    });

    var a = new fabric.Rect({
        id: "overlay-rect",
        top: e.top,
        left: e.left,
        angle: e.angle,
        width: e.getScaledWidth(),
        height: e.getScaledHeight(),
        selectable: !1,
        selection: !1,
        fill: "rgba(0, 0, 0, 0.5)",
        lockRotation: true,
    });

    var s = e.cropX,
        o = e.cropY,
        c = e.width,
        l = e.height;
    e.set({
        cropX: null,
        cropY: null,
        left: e.left - s * e.scaleX,
        top: e.top - o * e.scaleY,
        width: e._originalElement.naturalWidth,
        height: e._originalElement.naturalHeight,
        dirty: false
    });
    i.set({
        left: e.left + s * e.scaleX,
        top: e.top + o * e.scaleY,
        width: c * e.scaleX,
        height: l * e.scaleY,
        dirty: false
    });
    a.set({
        left: e.left,
        top: e.top,
        width: e.width * e.scaleX,
        height: e.height * e.scaleY,
        dirty: false
    });
    i.oldScaleX = i.scaleX;
    i.oldScaleY = i.scaleY;

    canvas.add(a),
    canvas.add(i),
    canvas.discardActiveObject(),
    canvas.setActiveObject(i),
    canvas.renderAll(),

    i.on("moving", function () {
    (i.top < e.top || i.left < e.left) &&
    ((i.left = i.left < e.left ? e.left : i.left),
    (i.top = i.top < e.top ? e.top : i.top)),
    (i.top + i.getScaledHeight() > e.top + e.getScaledHeight() ||
    i.left + i.getScaledWidth() > e.left + e.getScaledWidth()) &&
    ((i.top =
        i.top + i.getScaledHeight() > e.top + e.getScaledHeight()
        ? e.top + e.getScaledHeight() - i.getScaledHeight()
        : i.top),
    (i.left =
        i.left + i.getScaledWidth() > e.left + e.getScaledWidth()
        ? e.left + e.getScaledWidth() - i.getScaledWidth()
        : i.left));
        });

    i.on("deselected", function () {
        cropImage(i, e);
        canvas.remove(a);
    });
    }

    function cropImage(i, e){  
        canvas.remove(i);

        var s = (i.left - e.left) / e.scaleX,
            o = (i.top - e.top) / e.scaleY,
            c = (i.width * i.scaleX) / e.scaleX,
            l = (i.height * i.scaleY) / e.scaleY;

        // crop
        e.set({
            cropX: s,
            cropY: o,
            width: c,
            height: l,
            top: e.top + o * e.scaleY,
            left: e.left + s * e.scaleX,
            selectable: true,
            cropped: 1
        });

        var croppedImageData = e.toDataURL()
        const blob = dataURItoBlob(croppedImageData);
        croppedImageUrl = URL.createObjectURL(blob);
        canvas.renderAll();
    }
    
    doneButton.addEventListener('click', function() {
        clientEmit("doneButton", croppedImageUrl, "cropper-done");
    });
    
    // Function to convert data URI to Blob
    function dataURItoBlob(dataURI) {
        var byteString = atob(dataURI.split(',')[1]);
        var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
        var ab = new ArrayBuffer(byteString.length);
        var ia = new Uint8Array(ab);
        for (var i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        return new Blob([ab], { type: mimeString });
    }
    
}



