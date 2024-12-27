const BASE_URL = "http://127.0.0.1:8000/api";

export const sendMessageToChatbot = async (query) => {
    const response = await fetch(`${BASE_URL}/chat/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
    });
    return response.json();
};


