import { useState } from 'react'
import { Scissors, Plus, X, Check } from 'lucide-react'
import { pdfService } from '../services/pdfService'

export default function SplitPanel({ files, onSplit }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [pages, setPages] = useState('')
  const [splitting, setSplitting] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const parsePages = (pagesStr) => {
    if (!pagesStr.trim()) return []
    
    const result = []
    const parts = pagesStr.split(',')
    
    for (const part of parts) {
      const trimmed = part.trim()
      if (trimmed.includes('-')) {
        const [start, end] = trimmed.split('-').map(Number)
        if (!isNaN(start) && !isNaN(end)) {
          for (let i = start; i <= end; i++) {
            if (!result.includes(i)) result.push(i)
          }
        }
      } else {
        const num = parseInt(trimmed)
        if (!isNaN(num) && !result.includes(num)) {
          result.push(num)
        }
      }
    }
    
    return result.sort((a, b) => a - b)
  }

  const handleSplit = async () => {
    if (!selectedFile) {
      setError('Please select a file')
      return
    }

    const pageNumbers = parsePages(pages)
    if (pageNumbers.length === 0) {
      setError('Please enter valid page numbers')
      return
    }

    // Validate page numbers
    const maxPage = selectedFile.pages
    const invalidPages = pageNumbers.filter(p => p < 1 || p > maxPage)
    if (invalidPages.length > 0) {
      setError(`Invalid pages: ${invalidPages.join(', ')}. File has ${maxPage} pages.`)
      return
    }

    setSplitting(true)
    setError(null)
    setSuccess(false)

    try {
      const result = await pdfService.split(selectedFile.file_id, pageNumbers)
      onSplit({
        file_id: result.file_id,
        filename: `split_${selectedFile.filename}`,
        originalName: `split_${selectedFile.originalName || selectedFile.filename}`,
        pages: pageNumbers.length,
        size: 0,
      })
      setSuccess(true)
      setPages('')
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Split failed')
    } finally {
      setSplitting(false)
    }
  }

  const parsedPages = parsePages(pages)

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Split PDF</h2>
        <p className="text-sm text-gray-500">
          Extract specific pages from a PDF file.
        </p>
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
          Pages to Extract
        </label>
        <input
          type="text"
          value={pages}
          onChange={(e) => setPages(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          placeholder="e.g., 1, 3, 5-10"
          disabled={!selectedFile}
        />
        <p className="text-xs text-gray-400 mt-1">
          Enter page numbers separated by commas. Use ranges with hyphens (e.g., 1-5).
        </p>
        {parsedPages.length > 0 && (
          <p className="text-sm text-primary-600 mt-2">
            Selected pages: {parsedPages.join(', ')}
          </p>
        )}
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-50 text-green-600 px-4 py-3 rounded-lg text-sm">
          Pages extracted successfully!
        </div>
      )}

      <button
        onClick={handleSplit}
        disabled={splitting || !selectedFile || parsedPages.length === 0}
        className="w-full bg-primary-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-primary-700 focus:ring-4 focus:ring-primary-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {splitting ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            Splitting...
          </>
        ) : (
          <>
            <Scissors className="h-5 w-5 mr-2" />
            Extract {parsedPages.length} Pages
          </>
        )}
      </button>
    </div>
  )
}
