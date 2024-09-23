

//Functions that will be called via the front end to send/recieve data


//Function to send the problem desctiption, will be activated as soon as the page is loaded or the refresh button is triggered
async function send_problem_description() {
    const response = await fetch('http://127.0.0.1:8000/api/echo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: "idk" })
    });

    const data = await response.json();

    //We return the message retrieved from the API 

    return data.message


}

async function send_compare_response() {
    const response = await fetch('http://127.0.0.1:8000/api/other-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: "Message from API 2" })
    });

    const data = await response.json();
    document.getElementById("response2").innerText = data.message;
}

async function send_chat_response() {
    const response = await fetch('http://127.0.0.1:8000/api/third-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: "Message from API 3" })
    });

    const data = await response.json();
    document.getElementById("response3").innerText = data.message;
}



export default {send_problem_description}