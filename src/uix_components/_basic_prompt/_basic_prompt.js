if (!event_handlers["init-prompt"]) {
    event_handlers["init-prompt"] = (id, value, event_name) => {
        const inputElement = document.getElementById(value.inputID);
        const bottomElement = document.getElementById('bottom');
        const promptElement = document.getElementById(value.promptID);

        const focusHandler = () => {
            if(bottomElement === null) {
                return;
            }
            bottomElement.classList.remove('hidden');
            document.addEventListener('click', outSideClickHandler);
            inputElement.addEventListener('keydown', keyupHandler);
        };

        const outSideClickHandler = (e) => {    
            if (!promptElement.contains(e.target)) {
                bottomElement.classList.add('hidden');
                document.removeEventListener('click', outSideClickHandler);
                inputElement.removeEventListener('keydown', keyupHandler);
            }
        };

        const keyupHandler = (e) => {
            if (e.key == 'Delete' || e.key == 'Backspace') {
                if (inputElement.value === '') {
                    clientEmit(value.inputID, "prompt", "pop");
                }
            }
        };

        inputElement.addEventListener('focus', focusHandler);
        // Make sure to call the focus handler initially if needed
        if (document.activeElement === inputElement) {
            focusHandler();
        }
    };
} else {
    console.error("init-prompt is already defined");
}

if (!event_handlers["delete-prompt-image"]) {
event_handlers["delete-prompt-image"] = (id, value, event_name) => {
    const targetElement = document.getElementById("prompt-generator-prompt-area");
    const selectedElement = document.getElementById(value.id);
    const target = targetElement.children.length > 0 ? targetElement.lastElementChild : targetElement;
    const targetRect = target.getBoundingClientRect();
    const selectedRect = selectedElement.getBoundingClientRect();
    const transitionTime = 0.3;
    const offsetY = targetRect.top - selectedRect.top;
    const offsetX = targetRect.left - selectedRect.left;

    selectedElement.style.transition = "transform " + transitionTime + "s ease-in-out , opacity " + transitionTime + "s ease-in-out";
    selectedElement.style.transform = `translate(${offsetX}px,${offsetY-100}px)`;
    selectedElement.style.opacity = 0.1;
    
    setTimeout(() => {
        selectedElement.remove();
        clientEmit("prompt-generator-prompt", value, "add-prompt")
    }
    , transitionTime * 1000);
}
} else {
console.error("delete-prompt-image is already defined");
}

if (!event_handlers["take-back-prompt-image"]) {
event_handlers["add-prompt-image"] = (id, value, event_name) => {
    const targetElement = document.getElementById("prompt-generator-prompt-area");
    const newElement = document.createElement("img");
    newElement.src = value.src;
    newElement.id = value.id;
    newElement.className = "prompt-image";
    newElement.style.transition = "transform 0.2s ease-in-out";
    targetElement.appendChild(newElement);
}
}