// Check if the event handler is not already set
if (!event_handlers["init-prompt"]) {
    event_handlers["init-prompt"] = (id, value, event_name) => {
        console.log('init-prompt');
        const inputElement = document.getElementById("prompt-input");
        const bottomElement = document.getElementById('bottom');
        const promptElement = document.getElementById('prompt-wrapper');

        const focusHandler = () => {
            console.log('focus');
            bottomElement.classList.remove('hidden');
            document.addEventListener('click', outSideClickHandler);
            inputElement.addEventListener('keydown', keyupHandler);
        };

        const outSideClickHandler = (e) => {    
            if (!promptElement.contains(e.target)) {
                console.log('outside click');
                bottomElement.classList.add('hidden');
                document.removeEventListener('click', outSideClickHandler);
                inputElement.removeEventListener('keydown', keyupHandler);
            }
        };

        const keyupHandler = (e) => {
            if (e.key == 'Delete' || e.key == 'Backspace') {
                console.log('delete or backspace');
                clientEmit(value.inputID, "prompt", "pop");
            }
        };

        inputElement.addEventListener('focus', focusHandler);
    };
}
