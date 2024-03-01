import uix

from uix.elements import text, image, div, col

uix.html.add_css("imagecard-css",""".card {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    padding: 5px;
    text-align: center;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    cursor: pointer;
    transition: 0.2s;
}

.card .image {
    width: 100% !important;
    height: 100% !important;
    transition: 0.1s;
}

.card:hover .image {
    transform: scale(1.1);
}

.card .content {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
    border-radius: 5px;
    transition: 0.2s;
}

.from-bottom {
    left: 0;
    height: fit-content;
    position: absolute;
    transition: 0.2s;
    width: 100%;
    bottom: -100%;
    background-color: rgba(0, 0, 0, .65);
    bottom: 0%;
    height: fit-content;
    position: absolute;
    padding: 5px;
}

.absolute-center {
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: var(--background-mask);
    display: flex;
    justify-content: center;
    align-items: center;
                 }
""")

class basic_imagecard(uix.Element):
    def __init__(self, value=None, id=None, imagesrc=None, textstr=None):
        super().__init__(value, id=id)

        self.image = image
        self.textstr = textstr
        self.style("max-width","300px")
        self.style("max-heigth","300px")

        with self:
            with div().cls("card wall hall"):
                with div().cls("content"):
                    with col(id="skeleton "+ id).cls("absolute-center skelaton-loading") as self.loading:
                        div().cls("skelaton-item").style("height","80%")
                        div().cls("skelaton-item").style("height","20%")
                    image(value=imagesrc).cls("image").on('load', self.on_image_load)
                    with div().cls("from-bottom"):
                        text(self.textstr)

    def on_image_load(self, ctx, id, value):    
        self.loading.set_style("display", "none")