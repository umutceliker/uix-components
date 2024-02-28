if (!event_handlers["init-prompt"]) {
    event_handlers["init-prompt"] = (id, value, event_name) => {
        const inputElement = document.getElementById(value.inputID);
        const bottomElement = document.getElementById('bottom');
        const promptElement = document.getElementById('prompt-wrapper');

        console.log("init-prompt", id, value, event_name);

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
                    console.log("prompt", "pop");
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
