import React, { useState } from "react";


const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [filteredProducts, setFilteredProducts] = useState([]);

    const sendMessage = async () => {
        if (!input.trim()) return;

        // Add the user's message to the chat history
        setMessages([...messages, { type: "user", text: input }]);

        try {
            // Send the user's message to the backend
            const response = await fetch("http://127.0.0.1:8000/api/chat/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: input }),
            });

            const data = await response.json();

            // Add the bot's response to the chat history
            setMessages((prev) => [...prev, { type: "bot", text: data.reply }]);

            // If products are included in the response, update the product list
            if (data.products) {
                setFilteredProducts(data.products);
            } else {
                setFilteredProducts([]); // Clear the product list if no products are returned
            }
        } catch (error) {
            console.error("Error communicating with the chatbot API:", error);
            setMessages((prev) => [...prev, { type: "bot", text: "Error: Unable to connect to the server." }]);
        }

        // Clear the input field
        setInput("");
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    };

    return (
        <div className="app-container">
            <h1>Chatbot</h1>
            <div className="chatbot-container">
                <div className="chat-history">
                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`message ${msg.type}`}
                        >
                            {msg.text}
                        </div>
                    ))}
                </div>
                <input
                    type="text"
                    placeholder="Type a message..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                />
                <button onClick={sendMessage}>Send</button>
            </div>

            {/* Display filtered products */}
            {filteredProducts.length > 0 && (
                <div className="filtered-products">
                    <h2>Filtered Products</h2>
                    <div className="product-list">
                        {filteredProducts.map((product, index) => (
                            <div key={index} className="product-item">
                                <img src={product.image} alt={product.name} />
                                <h3>{product.name}</h3>
                                <p>Category: {product.category}</p>
                                <p>Price: ${product.price}</p>
                                <p>Rating: {product.rating}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Chatbot;
