let editor; // Declare editor globally

// Configure Monaco Editor using AMD loader
require.config({ paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.33.0/min/vs' }});
require(['vs/editor/editor.main'], function() {
    // Create the Monaco Editor instance in the #editor container
    editor = monaco.editor.create(document.getElementById('editor'), {
        value: `// Write your code here\nfunction helloWorld() {\n    console.log("Hello, world!");\n}`,
        language: 'javascript',      // Set the default language to JavaScript
        theme: 'vs-dark',            // Set theme ('vs', 'vs-dark', or 'hc-black')
        automaticLayout: false,      // Disable automatic layout to prevent resizing animations
        suggestOnTriggerCharacters: true, // Enable IntelliSense (autocomplete)
        minimap: { enabled: false }  // Optionally disable the minimap
    });

    // Add manual autocomplete trigger (Ctrl+Space)
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Space, function() {
        editor.trigger('anyString', 'editor.action.triggerSuggest', {});
    });

    // Add manual resizing logic
    window.addEventListener('resize', function() {
        editor.layout(); // Trigger manual layout update on window resize
    });
});

// Function to change the language in Monaco Editor
function changeLanguage() {
    const language = document.getElementById("language").value;
    monaco.editor.setModelLanguage(editor.getModel(), language); // Update the language mode
}



// Ensure Monaco Editor resizes correctly when the sidebar is toggled
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const miniSidebar = document.querySelector('.mini-sidebar');

    // Listen for the end of the transition on the sidebar
    sidebar.addEventListener('transitionend', () => {
        editor.layout(); // Trigger Monaco Editor layout update after sidebar transition
    });

    miniSidebar.addEventListener('transitionend', () => {
        editor.layout(); // Trigger Monaco Editor layout update after mini sidebar transition
    });
});

// Submit button event listener to send code to the Flask backend
document.getElementById('Submit').addEventListener('click', function() {
    const user_code = editor.getValue();  // Get the code from the editor
    const guideline_code = '';  // Assuming guideline_code is empty or fetched elsewhere

    // Prepare the data to be sent to the backend
    const data = {
        user_code: user_code,
        guideline_code: guideline_code
    };

    // Make a POST request to the Flask backend
    fetch('/review-code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)  // Send the code data as JSON
    })
    .then(response => response.json())
    .then(data => {
        // Display the feedback (replace with UI update logic as needed)
        alert('Review Result: ' + JSON.stringify(data, null, 2)); // Show the result in an alert box (or better UI)
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while submitting your code');
    });
});
