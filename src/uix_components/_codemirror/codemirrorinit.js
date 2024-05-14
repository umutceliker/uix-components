event_handlers['codemirrorinit'] = function(id, value, event_name) {
    console.log('codemirrorinit');
  
    // Check if CodeMirror library is globally available
    if (typeof CodeMirror === 'undefined') {
      console.error('CodeMirror library not found. Please include it before calling this function.');
      return;
    }
  
    // Get the target element based on the provided ID
    const targetElement = document.getElementById("codemirror");        
  
    console.log(window.CodeMirror.modes.hasOwnProperty('python'));
    // Create a new CodeMirror editor instance
    let editor = new window.CodeMirror.fromTextArea(targetElement, {
        value: "function myScript(){return 100;}\n", // Set initial value (optional)
        mode: "python", // Set editor mode
        lineNumbers: true, // Enable line numbers
        lineWrapping: true, // Enable line wrapping
        autoCloseTags: true, // Enable auto-closing tags
        autoCloseBrackets: true, // Enable auto-closing brackets
        foldGutter: true, // Enable code folding
        dragDrop: true, // Enable drag-and-drop
        theme: "dark", // Use a visually appealing theme (optional)
        gutters: ["lint"], // Add a linter gutter for code analysis (optional)
        lint: true
        // Add other editor customization options as needed
      });

    editor.setValue(value.string); // Set the editor content
    editor.on("change", function() {
        editor.save(); // Save the editor content on change
        console.log(editor.getValue()); // Log the editor content
    });

    // Add ctrl + s event listener to save the editor content
    editor.addKeyMap({
        "Ctrl-S": function(cm) {
            clientEmit('codemirror',editor.getValue(),'save');
            editor.save(); // Save the editor content
        }
    });

  };