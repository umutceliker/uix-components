import uix
from uix.elements import text, image, div 

uix.html.add_css("loading-css", """
@keyframes loading-bar {
    0% {
        width: 0%;
        background-color: #00573d;
    }
    
    100% {
        background-color: #333333;
        width: 100%;
    }
}         

@keyframes ping-black {
    0% {
        opacity: 0.7;
    }
    75% {
        opacity: 1;
    }
    100% {
        opacity: 0.7;
    }
}   

.loading-bar {
    border-radius: 3px;
    animation: loading-bar 10000ms ease-in-out forwards, ping-black 1.5s infinite;
}

.ait-search-logo {
    position: absolute;
    top: 45%;
    left: 45%;  
    }

    hidden {
    display: none;
}""")

class basic_loading(uix.Element):
    def __init__(self, value = None, id = None):
        super().__init__(value, id = id)
        
        self.estimate_time = 10000
        (
            self
                .cls("wall hall")
                .style("justify-content","flex-start")
                .style("gap","0")
                .style("position","relative")
        )

        with self:
            with div().cls("hall loading-bar").style("width","0%"):
                pass
            with div().style("position","absolute").style("top","0").style("left","70%"):
                text(
                    value = "Estimated Time: " + str(self.estimate_time) + " ms"
                ).cls("loading-title")

            with div().cls("ait-search-logo"):
                image(value="https://aitools.ait.com.tr/AIT_AI_LOGO.png").cls("logo").style("height","100px")

    def start(self):
        self.remove_class("hidden")

    def stop(self):
        self.add_class("hidden")