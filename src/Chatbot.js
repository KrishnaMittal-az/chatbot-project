// src/Chatbot.js
import React, { useState } from 'react';
import './Chatbot.css';

const Chatbot = () => {
    const [messages, setMessages] = useState([]); // State to hold chat messages
    const [input, setInput] = useState('');       // State to manage user input
    const [isLoading, setIsLoading] = useState(false); // State to indicate loading status

    // Predefined bot response
    const botResponse = "Your Trumio post has been posted on LinkedIn";

    // Function to handle sending messages
    const handleSend = () => {
        if (input.trim()) {
            const userMessage = { sender: 'user', text: input };

            // Add the user's message to the messages list
            setMessages([...messages, userMessage]);
            setInput('');

            // Start loading process
            setIsLoading(true);

            // Simulate a loading delay (e.g., 2 seconds)
            setTimeout(() => {
                const botMessage = { sender: 'bot', text: botResponse };

                // Add bot's message after the delay
                setMessages((prevMessages) => [...prevMessages, botMessage]);
                setIsLoading(false);
            }, 2000); // Adjust the delay time in milliseconds (2000ms = 2 seconds)
        }
    };

    return (
        <div className="chatbot-container">
            {/* Chat display area */}
            <div className="chatbox">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
                    >
                        {message.text}
                    </div>
                ))}

                {/* Display loading indicator when the bot is preparing its reply */}
                {isLoading && (
                    <div className="message bot-message loading">
                        Typing...
                    </div>
                )}
            </div>

            {/* Input area */}
            <div className="input-container">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                />
                <button onClick={handleSend} disabled={isLoading}>Send</button>
            </div>
        </div>
    );
};

export default Chatbot;
