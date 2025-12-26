import { useState } from 'react'
import { ListOrdered, Hash, FileText, Check } from 'lucide-react'
import { pdfService } from '../services/pdfService'

export default function PageToolsPanel({ files, onProcessed }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [mode, setMode] = useState('numbers') // numbers, header-footer

  // Page numbers options
  const [position, setPosition] = useState('bottom')
  const [alignment, setAlignment] = useState('center')
  const [startNum, setStartNum] = useState(1)

  // Header/Footer options
  const [headerText, setHeaderText] = useState('')
  const [footerText, setFooterText] = useState('')

  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

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
      if (mode === 'numbers') {
        response = await pdfService.addPageNumbers(selectedFile.file_id, position, alignment, startNum)
      } else {
        if (!headerText && !footerText) {
          setError('Please enter header or footer text')
          setProcessing(false)
          return
        }
        response = await pdfService.addHeaderFooter(selectedFile.file_id, headerText || null, footerText || null)
      }

      onProcessed({
        file_id: response.file_id,
        filename: `${mode === 'numbers' ? 'numbered' : 'headered'}_${selectedFile.originalName || selectedFile.filename}`,
        originalName: `${mode === 'numbers' ? 'numbered' : 'headered'}_${selectedFile.originalName || selectedFile.filename}`,
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
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Page Tools</h2>
        <p className="text-sm text-gray-500">
          Add page numbers, headers, and footers to your PDF.
        </p>
      </div>

      {/* Mode selection */}
      <div className="flex space-x-2">
        <button
          onClick={() => setMode('numbers')}
          className={`flex-1 flex items-center justify-center py-2 px-4 rounded-lg border transition-colors ${
            mode === 'numbers'
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          <Hash className="h-4 w-4 mr-2" />
          Page Numbers
        </button>
        <button
          onClick={() => setMode('header-footer')}
          className={`flex-1 flex items-center justify-center py-2 px-4 rounded-lg border transition-colors ${
            mode === 'header-footer'
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          <FileText className="h-4 w-4 mr-2" />
          Header/Footer
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
                <span className="text-sm truncate flex-1">
                  {file.originalName || file.filename}
                </span>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Page Numbers options */}
      {mode === 'numbers' && (
        <>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Position</label>
            <div className="flex space-x-2">
              {['top', 'bottom'].map((pos) => (
                <button
                  key={pos}
                  onClick={() => setPosition(pos)}
                  className={`flex-1 py-2 px-4 rounded-lg border transition-colors capitalize ${
                    position === pos
                      ? 'border-primary-500 bg-primary-50 text-primary-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  {pos}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Alignment</label>
            <div className="flex space-x-2">
              {['left', 'center', 'right'].map((align) => (
                <button
                  key={align}
                  onClick={() => setAlignment(align)}
                  className={`flex-1 py-2 px-4 rounded-lg border transition-colors capitalize ${
                    alignment === align
                      ? 'border-primary-500 bg-primary-50 text-primary-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  {align}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Start Number</label>
            <input
              type="number"
              min="1"
              value={startNum}
              onChange={(e) => setStartNum(parseInt(e.target.value) || 1)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
        </>
      )}

      {/* Header/Footer options */}
      {mode === 'header-footer' && (
        <>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Header Text</label>
            <input
              type="text"
              value={headerText}
              onChange={(e) => setHeaderText(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="e.g., Document Title"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Footer Text</label>
            <input
              type="text"
              value={footerText}
              onChange={(e) => setFooterText(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="e.g., Confidential"
            />
          </div>
        </>
      )}

      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-50 text-green-600 px-4 py-3 rounded-lg text-sm">
          {mode === 'numbers' ? 'Page numbers added!' : 'Header/Footer added!'}
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
            <ListOrdered className="h-5 w-5 mr-2" />
            {mode === 'numbers' ? 'Add Page Numbers' : 'Add Header/Footer'}
          </>
        )}
      </button>
    </div>
  )
}
