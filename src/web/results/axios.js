    // Reference to the form
    const form = document.getElementById('codeForm');

    form.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent the form from submitting in the default way

        // Gather the values from the textarea inputs
        const guidelineCode = document.getElementById('guideline_code').value;
        const userCode = document.getElementById('user_code').value;

        // Ensure that both fields have content
        if (!guidelineCode || !userCode) {
            alert("Both code fields must be filled out!");
            return;
        }

        try {
            // Make an Axios POST request to the Flask backend
            const response = await axios.post('/review-code', {
                guideline_code: guidelineCode,
                user_code: userCode
            });

            // Display the result
            document.getElementById('result').textContent = JSON.stringify(response.data, null, 2);
        } catch (error) {
            console.error("There was an error!", error);
            document.getElementById('result').textContent = `Error: ${error.response?.data?.error || error.message}`;
        }
    });