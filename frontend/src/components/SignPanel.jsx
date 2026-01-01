import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { PenLine, Check, Upload } from 'lucide-react'
import { pdfService } from '../services/pdfService'

export default function SignPanel({ files, onSigned }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [signatureFile, setSignatureFile] = useState(null)
  const [page, setPage] = useState(1)
  const [x, setX] = useState(400)
  const [y, setY] = useState(700)
  const [width, setWidth] = useState(150)
  const [height, setHeight] = useState(50)
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setSignatureFile(acceptedFiles[0])
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpg', '.jpeg', '.png', '.gif']
    },
    maxFiles: 1,
  })

  const handleSign = async () => {
    if (!selectedFile) {
      setError('Please select a PDF file')
      return
    }
    if (!signatureFile) {
      setError('Please upload a signature image')
      return
    }

    setProcessing(true)
    setError(null)
    setSuccess(false)

    try {
      const response = await pdfService.sign(
        selectedFile.file_id, signatureFile, page, x, y, width, height
      )

      onSigned({
        file_id: response.file_id,
        filename: `signed_${selectedFile.originalName || selectedFile.filename}`,
        originalName: `signed_${selectedFile.originalName || selectedFile.filename}`,
        pages: selectedFile.pages,
        size: selectedFile.size,
      })
      setSuccess(true)
      setSignatureFile(null)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Signing failed')
    } finally {
      setProcessing(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Sign PDF</h2>
        <p className="text-sm text-gray-500">
          Add your signature image to a PDF document.
        </p>
      </div>

      {/* File selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Select PDF
        </label>
        {files.length === 0 ? (
          <p className="text-sm text-gray-400">No files available. Upload some PDFs first.</p>
        ) : (
          <div className="grid grid-cols-2 gap-2">
            {files.map((file) => (
              <button
                key={file.file_id}
                onClick={() => setSelectedFile(file)}
                className={`flex items-center p-3 rounded-lg border text-left transition-colors ${
                  selectedFile?.file_id === file.file_id
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3 ${
                  selectedFile?.file_id === file.file_id
                    ? 'border-primary-500 bg-primary-500'
                    : 'border-gray-300'
                }`}>
                  {selectedFile?.file_id === file.file_id && (
                    <Check className="h-4 w-4 text-white" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <span className="text-sm truncate block">
                    {file.originalName || file.filename}
                  </span>
                  <span className="text-xs text-gray-400">{file.pages} pages</span>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Signature upload */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Signature Image
        </label>
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-4 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : signatureFile
              ? 'border-green-500 bg-green-50'
              : 'border-gray-300 hover:border-primary-400'
          }`}
        >
          <input {...getInputProps()} />
          {signatureFile ? (
            <div className="flex items-center justify-center space-x-2">
              <Check className="h-5 w-5 text-green-600" />
              <span className="text-green-700">{signatureFile.name}</span>
            </div>
          ) : (
            <>
              <Upload className="h-6 w-6 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-500">
                Drop signature image here or click to select
              </p>
              <p className="text-xs text-gray-400 mt-1">PNG, JPG, GIF supported</p>
            </>
          )}
        </div>
      </div>

      {/* Position settings */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Page Number</label>
        <input
          type="number"
          min="1"
          max={selectedFile?.pages || 999}
          value={page}
          onChange={(e) => setPage(parseInt(e.target.value) || 1)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">X Position</label>
          <input
            type="number"
            value={x}
            onChange={(e) => setX(parseInt(e.target.value) || 0)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Y Position</label>
          <input
            type="number"
            value={y}
            onChange={(e) => setY(parseInt(e.target.value) || 0)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Width</label>
          <input
            type="number"
            value={width}
            onChange={(e) => setWidth(parseInt(e.target.value) || 100)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Height</label>
          <input
            type="number"
            value={height}
            onChange={(e) => setHeight(parseInt(e.target.value) || 50)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
          />
        </div>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-50 text-green-600 px-4 py-3 rounded-lg text-sm">
          PDF signed successfully!
        </div>
      )}

      <button
        onClick={handleSign}
        disabled={processing || !selectedFile || !signatureFile}
        className="w-full bg-primary-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-primary-700 focus:ring-4 focus:ring-primary-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {processing ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            Signing...
          </>
        ) : (
          <>
            <PenLine className="h-5 w-5 mr-2" />
            Sign PDF
          </>
        )}
      </button>
    </div>
  )
}
