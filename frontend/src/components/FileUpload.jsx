import { useState } from 'react'

export default function FileUpload({ onUploadSuccess }) {
    const [isDragging, setIsDragging] = useState(false)
    const [uploading, setUploading] = useState(false)

    const handleDragOver = (e) => {
        e.preventDefault()
        setIsDragging(true)
    }

    const handleDragLeave = () => {
        setIsDragging(false)
    }

    const handleDrop = async (e) => {
        e.preventDefault()
        setIsDragging(false)
        const files = e.dataTransfer.files
        if (files.length > 0) {
            await uploadFile(files[0])
        }
    }

    const handleFileSelect = async (e) => {
        if (e.target.files.length > 0) {
            await uploadFile(e.target.files[0])
        }
    }

    const uploadFile = async (file) => {
        setUploading(true)
        const formData = new FormData()
        formData.append('file', file)

        try {
            const response = await fetch('http://localhost:8000/upload', {
                method: 'POST',
                body: formData,
            })
            if (response.ok) {
                onUploadSuccess(file.name)
            } else {
                alert("Upload failed")
            }
        } catch (error) {
            console.error("Error:", error)
            alert("Upload error")
        } finally {
            setUploading(false)
        }
    }

    return (
        <div
            className={`border-2 border-dashed rounded-lg p-10 flex flex-col items-center justify-center transition-colors
        ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
        >
            <div className="text-center">
                <p className="text-lg text-gray-600 mb-4">
                    {uploading ? "Uploading..." : "Drag & Drop your document here"}
                </p>
                <p className="text-sm text-gray-400 mb-6">or</p>
                <input
                    type="file"
                    onChange={handleFileSelect}
                    className="hidden"
                    id="fileInput"
                />
                <label
                    htmlFor="fileInput"
                    className={`px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 cursor-pointer ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                    Browse Files
                </label>
            </div>
        </div>
    )
}
