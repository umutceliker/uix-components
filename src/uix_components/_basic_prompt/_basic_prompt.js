// Check if the event handler is not already set
if (!event_handlers["init-prompt"]) {
    event_handlers["init-prompt"] = (id, value, event_name) => {
        const inputElement = document.getElementById("prompt-input");
        const bottomElement = document.getElementById('bottom');
        const promptElement = document.getElementById('prompt-wrapper');

        const focusHandler = () => {
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
    };
}
