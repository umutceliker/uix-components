import uix
uix.html.add_css_file("_basic_alert.css",__file__)

uix.html.add_script("_basic_alert.js","""
event_handlers["alert-open"] = function(id, value, event_name){
    var alertContainer = document.getElementById("comp_alert");
    alertContainer.style.display = "flex";

    var alertDiv = document.createElement("div");
    alertDiv.className = value.type + " alert-child alert-close";
    alertDiv.textContent = value.message;
                    
    const progressBar = document.createElement("div");
                    
    progressBar.className = "alert-progress";
    alertDiv.appendChild(progressBar);
                    
    if(value.icon != null){
        const icon = document.createElement("i");
        icon.className = value.icon;
        alertDiv.appendChild(icon);
    }

    alertContainer.appendChild(alertDiv);

    alertDiv.addEventListener("animationend", function(){
        alertContainer.removeChild(alertDiv);
        if(alertContainer.childElementCount == 0){
            alertContainer.style.display = "none";
        }
    });             
}
                    
    """, beforeMain=False)

class basic_alert(uix.Element):
    def __init__(self, value=None, id=None):
        super().__init__(value, id=id)
        self.cls("alert")

    def open(self, type, value, icon=None):
        opt = {
            "type": type,
            "message": value,
            "icon": icon
        }
        self.session.send(self.id, opt, "alert-open")
