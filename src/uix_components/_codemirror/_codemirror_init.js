event_handlers['codemirror-init'] = function(id, value, event_name) {
    
    // Get the target element based on the provided ID
    const targetElement = document.getElementById("codemirror"); 

    // Create a new CodeMirror editor instance
    let editor = new window.CodeMirror.fromTextArea(targetElement, {
      indentWithTabs: false,  // Use tabs for indentation
      value: "def my_function():\n  return 'Hello, CodeMirror!'",
      lineNumbers: true, // Enable line numbers
    });
    
    // Check if CodeMirror library is globally available
    if (typeof CodeMirror === 'undefined') {
      console.error('CodeMirror library not found. Please include it before calling this function.');
      return;
    }
  

    editor.setValue(value.string); // Set the editor content
    editor.on("change", function() {
        editor.save(); // Save the editor content on change
    });

    // Add ctrl + s event listener to save the editor content
    editor.addKeyMap({
        "Ctrl-S": function(cm) {
            clientEmit('codemirror',editor.getValue(),'save');
            editor.save(); // Save the editor content
        }
    });

  };