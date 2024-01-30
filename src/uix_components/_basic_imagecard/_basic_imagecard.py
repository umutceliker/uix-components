import uix

from uix.elements import text, image, div

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
}

.card:hover .content .from-bottom {
    position: absolute;
    width: 100%;
    background-color: rgba(0, 0, 0, .65);
    bottom: 0%;
    height: fit-content;
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
                    image(value=imagesrc).cls("image")
                    with div().cls("from-bottom"):
                        text(self.textstr)
