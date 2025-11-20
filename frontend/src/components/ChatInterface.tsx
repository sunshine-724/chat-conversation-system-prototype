"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
    role: "user" | "assistant";
    content: string;
}

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [selectedModel, setSelectedModel] = useState("");
    const [models, setModels] = useState<string[]>([]);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        fetch("http://localhost:8000/models")
            .then((res) => res.json())
            .then((data) => {
                setModels(data.models);
                if (data.models.length > 0) {
                    setSelectedModel(data.models[0]);
                }
            })
            .catch((err) => console.error("Failed to fetch models:", err));
    }, []);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || !selectedModel) return;

        const userMessage: Message = { role: "user", content: input };
        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setIsLoading(true);

        // Add empty assistant message to start streaming into
        setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

        try {
            const response = await fetch(
                `http://localhost:8000/chat?message=${encodeURIComponent(input)}&model=${encodeURIComponent(selectedModel)}`,
                {
                    method: "POST",
                }
            );

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            if (!response.body) return;

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let done = false;

            while (!done) {
                const { value, done: doneReading } = await reader.read();
                done = doneReading;
                const chunkValue = decoder.decode(value, { stream: true });

                setMessages((prev) => {
                    const newMessages = [...prev];
                    const lastMessageIndex = newMessages.length - 1;
                    const lastMessage = { ...newMessages[lastMessageIndex] }; // Create a copy

                    if (lastMessage.role === "assistant") {
                        lastMessage.content += chunkValue;
                        newMessages[lastMessageIndex] = lastMessage; // Update the array with the copy
                    }
                    return newMessages;
                });
            }
        } catch (error) {
            console.error("Error:", error);
            setMessages((prev) => [
                ...prev,
                { role: "assistant", content: "Sorry, something went wrong." },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleExport = async () => {
        try {
            const response = await fetch("http://localhost:8000/export", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ messages }),
            });

            if (!response.ok) throw new Error("Export failed");

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `chat_history_${new Date().toISOString().slice(0, 19).replace(/:/g, "-")}.json`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error("Export error:", error);
            alert("Failed to export chat history");
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gray-900 text-gray-100">
            <header className="p-4 border-b border-gray-800 bg-gray-950 flex justify-between items-center">
                <h1 className="text-xl font-semibold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                    AI Chat Prototype
                </h1>
                <div className="flex gap-2">
                      <select
                        value={selectedModel}
                        onChange={(e) => setSelectedModel(e.target.value)}
                        className="bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        disabled={models.length === 0}
                      >
                        {models.length === 0 ? (
                            <option value="">No models found</option>
                        ) : (
                            models.map((model) => (
                                <option key={model} value={model}>
                                    {model}
                                </option>
                            ))
                        )}
                    </select>
                    <button
                        onClick={handleExport}
                        className="bg-gray-800 hover:bg-gray-700 border border-gray-700 text-white rounded-lg px-3 py-1 text-sm transition-colors"
                        title="Export Chat"
                    >
                        Export
                    </button>
                </div>
            </header>

            <main className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 && (
                    <div className="flex items-center justify-center h-full text-gray-500">
                        <p>Start a conversation...</p>
                    </div>
                )}
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"
                            }`}
                    >
                        <div
                            className={`max-w-[80%] rounded-2xl px-4 py-2 ${msg.role === "user"
                                ? "bg-blue-600 text-white"
                                : "bg-gray-800 text-gray-200"
                                }`}
                        >
                            {msg.content}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-gray-800 rounded-2xl px-4 py-2 text-gray-400 animate-pulse">
                            Thinking...
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </main>

            <footer className="p-4 border-t border-gray-800 bg-gray-950">
                <form onSubmit={handleSubmit} className="flex gap-2 max-w-3xl mx-auto">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder={models.length === 0 ? "No models available" : "Type your message..."}
                        className="flex-1 bg-gray-800 border-gray-700 text-white rounded-xl px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
                        disabled={isLoading || models.length === 0}
                    />
                    <button
                        type="submit"
                        disabled={isLoading || models.length === 0}
                        className="bg-blue-600 hover:bg-blue-700 text-white rounded-xl px-6 py-2 font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Send
                    </button>
                </form>
            </footer>
        </div>
    );
}
