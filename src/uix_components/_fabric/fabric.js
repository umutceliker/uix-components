event_handlers["init-fabric"] = function (id, value, event_name) {
    const canvas = new fabric.Canvas(id);
    const rect = new fabric.Rect({
        top: 100,
        left: 100,
        width: 60,
        height: 70,
        fill: 'red',
    });
  canvas.add(rect);
}
