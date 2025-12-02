import { useState } from 'react'
import { PenTool, Type, Highlighter, EyeOff, Check } from 'lucide-react'
import { pdfService } from '../services/pdfService'

export default function AnnotatePanel({ files, onProcessed }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [mode, setMode] = useState('text') // text, highlight, redact
  
  // Common options
  const [page, setPage] = useState(1)
  
  // Text options
  const [text, setText] = useState('')
  const [x, setX] = useState(50)
  const [y, setY] = useState(50)
  const [fontSize, setFontSize] = useState(12)
  const [color, setColor] = useState('#000000')
  
  // Area options (for highlight/redact)
  const [x0, setX0] = useState(50)
  const [y0, setY0] = useState(50)
  const [x1, setX1] = useState(200)
  const [y1, setY1] = useState(100)
  const [highlightColor, setHighlightColor] = useState('#ffff00')
  
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
    if (result) {
      return `${parseInt(result[1], 16) / 255},${parseInt(result[2], 16) / 255},${parseInt(result[3], 16) / 255}`
    }
    return '0,0,0'
  }

  const handleProcess = async () => {
    if (!selectedFile) {
      setError('Please select a file')
      return
    }

    setProcessing(true)
    setError(null)
    setSuccess(false)

    try {
      let response
      if (mode === 'text') {
        if (!text.trim()) {
          setError('Please enter text')
          setProcessing(false)
          return
        }
        response = await pdfService.addText(
          selectedFile.file_id, text, page, x, y, fontSize, hexToRgb(color)
        )
      } else if (mode === 'highlight') {
        response = await pdfService.addHighlight(
          selectedFile.file_id, page, x0, y0, x1, y1, hexToRgb(highlightColor)
        )
      } else {
        response = await pdfService.redact(
          selectedFile.file_id, page, x0, y0, x1, y1
        )
      }
      
      const prefix = mode === 'text' ? 'annotated' : mode === 'highlight' ? 'highlighted' : 'redacted'
      onProcessed({
        file_id: response.file_id,
        filename: `${prefix}_${selectedFile.originalName || selectedFile.filename}`,
        originalName: `${prefix}_${selectedFile.originalName || selectedFile.filename}`,
        pages: selectedFile.pages,
        size: selectedFile.size,
      })
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Operation failed')
    } finally {
      setProcessing(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Annotate PDF</h2>
        <p className="text-sm text-gray-500">
          Add text, highlights, or redact sensitive information.
        </p>
      </div>

      {/* Mode selection */}
      <div className="flex space-x-2">
        <button
          onClick={() => setMode('text')}
          className={`flex-1 flex items-center justify-center py-2 px-3 rounded-lg border transition-colors ${
            mode === 'text'
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          <Type className="h-4 w-4 mr-1" />
          Text
        </button>
        <button
          onClick={() => setMode('highlight')}
          className={`flex-1 flex items-center justify-center py-2 px-3 rounded-lg border transition-colors ${
            mode === 'highlight'
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          <Highlighter className="h-4 w-4 mr-1" />
          Highlight
        </button>
        <button
          onClick={() => setMode('redact')}
          className={`flex-1 flex items-center justify-center py-2 px-3 rounded-lg border transition-colors ${
            mode === 'redact'
              ? 'border-red-500 bg-red-50 text-red-700'
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          <EyeOff className="h-4 w-4 mr-1" />
          Redact
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

      {/* Page number */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Page Number</label>
        <input
          type="number"
          min="1"
          max={selectedFile?.pages || 999}
          value={page}
          onChange={(e) => setPage(parseInt(e.target.value) || 1)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
      </div>

      {/* Text mode options */}
      {mode === 'text' && (
        <>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Text</label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              rows={3}
              placeholder="Enter text to add..."
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
              <label className="block text-sm font-medium text-gray-700 mb-2">Font Size</label>
              <input
                type="number"
                min="6"
                max="72"
                value={fontSize}
                onChange={(e) => setFontSize(parseInt(e.target.value) || 12)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Color</label>
              <input
                type="color"
                value={color}
                onChange={(e) => setColor(e.target.value)}
                className="w-full h-10 rounded-lg cursor-pointer"
              />
            </div>
          </div>
        </>
      )}

      {/* Highlight/Redact options */}
      {(mode === 'highlight' || mode === 'redact') && (
        <>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">X Start</label>
              <input
                type="number"
                value={x0}
                onChange={(e) => setX0(parseInt(e.target.value) || 0)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Y Start</label>
              <input
                type="number"
                value={y0}
                onChange={(e) => setY0(parseInt(e.target.value) || 0)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">X End</label>
              <input
                type="number"
                value={x1}
                onChange={(e) => setX1(parseInt(e.target.value) || 0)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Y End</label>
              <input
                type="number"
                value={y1}
                onChange={(e) => setY1(parseInt(e.target.value) || 0)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>
          </div>
          {mode === 'highlight' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Highlight Color</label>
              <input
                type="color"
                value={highlightColor}
                onChange={(e) => setHighlightColor(e.target.value)}
                className="w-full h-10 rounded-lg cursor-pointer"
              />
            </div>
          )}
        </>
      )}

      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-50 text-green-600 px-4 py-3 rounded-lg text-sm">
          Annotation added successfully!
        </div>
      )}

      <button
        onClick={handleProcess}
        disabled={processing || !selectedFile}
        className={`w-full text-white py-2.5 px-4 rounded-lg font-medium focus:ring-4 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center ${
          mode === 'redact' 
            ? 'bg-red-600 hover:bg-red-700 focus:ring-red-200' 
            : 'bg-primary-600 hover:bg-primary-700 focus:ring-primary-200'
        }`}
      >
        {processing ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            Processing...
          </>
        ) : (
          <>
            <PenTool className="h-5 w-5 mr-2" />
            {mode === 'text' ? 'Add Text' : mode === 'highlight' ? 'Add Highlight' : 'Redact Area'}
          </>
        )}
      </button>
    </div>
  )
}
