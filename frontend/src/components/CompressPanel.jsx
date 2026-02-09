import { useState } from 'react'
import { Minimize2, Check } from 'lucide-react'
import { pdfService } from '../services/pdfService'

export default function CompressPanel({ files, onCompressed }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [compressing, setCompressing] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const handleCompress = async () => {
    if (!selectedFile) {
      setError('Please select a file')
      return
    }

    setCompressing(true)
    setError(null)
    setResult(null)

    try {
      const response = await pdfService.compress(selectedFile.file_id)
      setResult(response)
      onCompressed({
        file_id: response.file_id,
        filename: `compressed_${selectedFile.originalName || selectedFile.filename}`,
        originalName: `compressed_${selectedFile.originalName || selectedFile.filename}`,
        pages: selectedFile.pages,
        size: response.compressed_size,
      })
    } catch (err) {
      setError(err.response?.data?.detail || 'Compression failed')
    } finally {
      setCompressing(false)
    }
  }

  const formatSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Compress PDF</h2>
        <p className="text-sm text-gray-500">
          Reduce file size while maintaining quality.
        </p>
      </div>

      {/* File selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Select File to Compress
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
                  <span className="text-xs text-gray-400">{formatSize(file.size)}</span>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-green-50 p-4 rounded-lg">
          <h4 className="font-medium text-green-800 mb-2">Compression Complete!</h4>
          <div className="text-sm text-green-700 space-y-1">
            <p>Original size: {formatSize(result.original_size)}</p>
            <p>Compressed size: {formatSize(result.compressed_size)}</p>
            <p className="font-medium">Reduced by: {result.reduction_percent}%</p>
          </div>
        </div>
      )}

      <button
        onClick={handleCompress}
        disabled={compressing || !selectedFile}
        className="w-full bg-primary-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-primary-700 focus:ring-4 focus:ring-primary-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {compressing ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            Compressing...
          </>
        ) : (
          <>
            <Minimize2 className="h-5 w-5 mr-2" />
            Compress PDF
          </>
        )}
      </button>
    </div>
  )
}
