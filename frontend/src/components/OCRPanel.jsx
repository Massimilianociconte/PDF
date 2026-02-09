import { useState } from 'react'
import { FileSearch, Check, Copy } from 'lucide-react'
import { pdfService } from '../services/pdfService'

export default function OCRPanel({ files }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [page, setPage] = useState('')
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)
  const [copied, setCopied] = useState(false)
  const [mode, setMode] = useState('extract') // 'extract' or 'ocr'

  const handleProcess = async () => {
    if (!selectedFile) {
      setError('Please select a file')
      return
    }

    setProcessing(true)
    setError(null)
    setResult(null)

    try {
      const pageNum = page ? parseInt(page) : null
      
      let response
      if (mode === 'ocr') {
        response = await pdfService.ocr(selectedFile.file_id, pageNum)
      } else {
        response = await pdfService.extractText(selectedFile.file_id, pageNum)
      }
      
      setResult(response.text)
    } catch (err) {
      setError(err.response?.data?.detail || 'Processing failed')
    } finally {
      setProcessing(false)
    }
  }

  const copyToClipboard = async () => {
    if (!result) return
    
    try {
      await navigator.clipboard.writeText(result)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Copy failed:', err)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">
          Text Extraction & OCR
        </h2>
        <p className="text-sm text-gray-500">
          Extract text from PDFs or use OCR for scanned documents.
        </p>
      </div>

      {/* Mode selector */}
      <div className="flex space-x-2">
        <button
          onClick={() => setMode('extract')}
          className={`flex-1 py-2 px-4 rounded-lg border transition-colors ${
            mode === 'extract'
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          Extract Text
        </button>
        <button
          onClick={() => setMode('ocr')}
          className={`flex-1 py-2 px-4 rounded-lg border transition-colors ${
            mode === 'ocr'
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          OCR (Scanned)
        </button>
      </div>

      {/* File selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Select File
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

      {/* Page selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Page Number (optional)
        </label>
        <input
          type="number"
          value={page}
          onChange={(e) => setPage(e.target.value)}
          min="1"
          max={selectedFile?.pages || 999}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          placeholder="Leave empty for all pages"
          disabled={!selectedFile}
        />
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      <button
        onClick={handleProcess}
        disabled={processing || !selectedFile}
        className="w-full bg-primary-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-primary-700 focus:ring-4 focus:ring-primary-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {processing ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            Processing...
          </>
        ) : (
          <>
            <FileSearch className="h-5 w-5 mr-2" />
            {mode === 'ocr' ? 'Run OCR' : 'Extract Text'}
          </>
        )}
      </button>

      {/* Result */}
      {result && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-700">Result</h3>
            <button
              onClick={copyToClipboard}
              className="flex items-center text-sm text-primary-600 hover:text-primary-700"
            >
              {copied ? (
                <>
                  <Check className="h-4 w-4 mr-1" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="h-4 w-4 mr-1" />
                  Copy
                </>
              )}
            </button>
          </div>
          <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
            <pre className="text-sm text-gray-700 whitespace-pre-wrap font-mono">
              {result || 'No text found'}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}
