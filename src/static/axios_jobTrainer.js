// Initialize Monaco editor
require.config({ paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.33.0/min/vs' }});
require(['vs/editor/editor.main'], function() {
    // Set up the editor with default language
    window.editor = monaco.editor.create(document.getElementById('editor'), {
        value: "// Write your code here...",
        language: 'javascript',
        theme: 'vs-dark',
        automaticLayout: true,
    });
});

// Function to change the language in the editor
function changeLanguage() {
    const selectedLanguage = document.getElementById('language').value;
    monaco.editor.setModelLanguage(window.editor.getModel(), selectedLanguage);
}

// Reference to the submit button
document.getElementById('Submit').addEventListener('click', async function () {
    const code = window.editor.getValue(); // Get the code from Monaco editor
    const language = document.getElementById('language').value; // Get the selected language

    try {
        // Make an Axios POST request to the Flask backend
        const response = await axios.post('/processing/process', {
            code: code,       // Send the user's code
            language: language // Send the selected language
        }); 

        // Display the result (you may want to show this in a more structured way)
        alert('Result: ' + JSON.stringify(response.data));
    } catch (error) {
        console.error("There was an error!", error);
        alert('Error: ' + error.response?.data?.error || error.message);
    }
});
