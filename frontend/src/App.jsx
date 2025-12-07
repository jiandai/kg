import { useState } from 'react'
import FileUpload from './components/FileUpload'
import ChatInterface from './components/ChatInterface'

function App() {
  const [fileUploaded, setFileUploaded] = useState(false)
  const [filename, setFilename] = useState("")

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">Single Doc Q&A</h1>

      <div className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6">
        {!fileUploaded ? (
          <FileUpload onUploadSuccess={(name) => {
            setFileUploaded(true)
            setFilename(name)
          }} />
        ) : (
          <div className="flex flex-col h-[600px]">
            <div className="flex justify-between items-center mb-4 border-b pb-2">
              <span className="font-semibold text-gray-700">Document: {filename}</span>
              <button
                onClick={() => setFileUploaded(false)}
                className="text-sm text-red-500 hover:text-red-700 hover:underline"
              >
                Change Document
              </button>
            </div>
            <ChatInterface />
          </div>
        )}
      </div>
    </div>
  )
}

export default App
