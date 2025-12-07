import { useState, useRef, useEffect } from 'react'

export default function ChatInterface() {
    const [messages, setMessages] = useState([
        { role: 'system', content: 'Document loaded. You can now ask questions.' }
    ])
    const [input, setInput] = useState("")
    const [loading, setLoading] = useState(false)
    const [strategy, setStrategy] = useState("auto")
    const bottomRef = useRef(null)

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])

    const sendMessage = async () => {
        if (!input.trim()) return

        const userMsg = { role: 'user', content: input }
        setMessages(prev => [...prev, userMsg])
        setInput("")
        setLoading(true)

        try {
            const res = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMsg.content, strategy })
            })
            const data = await res.json()
            setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', content: "Error communicating with server." }])
        } finally {
            setLoading(false)
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    return (
        <div className="flex flex-col h-full">
            <div className="flex justify-end mb-2">
                <select
                    value={strategy}
                    onChange={(e) => setStrategy(e.target.value)}
                    className="text-xs border rounded p-1 bg-gray-50 text-gray-600"
                >
                    <option value="auto">Auto Strategy</option>
                    <option value="vanilla">Vanilla RAG</option>
                    <option value="graph">Graph RAG</option>
                </select>
            </div>
            <div className="flex-1 overflow-y-auto mb-4 p-4 border rounded bg-gray-50">
                {messages.map((msg, i) => (
                    <div key={i} className={`mb-3 flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div
                            className={`max-w-[80%] p-3 rounded-lg ${msg.role === 'user'
                                    ? 'bg-blue-600 text-white rounded-br-none'
                                    : msg.role === 'system' ? 'bg-gray-200 text-gray-800 text-center text-xs w-full'
                                        : 'bg-white border invalid-border text-gray-800 rounded-bl-none'
                                }`}
                        >
                            {msg.content}
                        </div>
                    </div>
                ))}
                {loading && <div className="text-xs text-gray-400 italic">Thinking...</div>}
                <div ref={bottomRef} />
            </div>

            <div className="flex gap-2">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask a question..."
                    className="flex-1 p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={loading}
                />
                <button
                    onClick={sendMessage}
                    disabled={loading}
                    className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                >
                    Send
                </button>
            </div>
        </div>
    )
}
