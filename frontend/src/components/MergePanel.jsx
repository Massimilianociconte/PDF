import { useState } from 'react'
import { Merge, GripVertical, Plus, Minus, Check, ArrowUp, ArrowDown } from 'lucide-react'
import { pdfService } from '../services/pdfService'

export default function MergePanel({ files, onMerged }) {
  const [selectedFiles, setSelectedFiles] = useState([])
  const [outputName, setOutputName] = useState('merged.pdf')
  const [merging, setMerging] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const toggleFile = (file) => {
    setSelectedFiles((prev) => {
      const exists = prev.find((f) => f.file_id === file.file_id)
      if (exists) {
        return prev.filter((f) => f.file_id !== file.file_id)
      }
      return [...prev, file]
    })
  }

  const moveUp = (index) => {
    if (index === 0) return
    setSelectedFiles((prev) => {
      const newList = [...prev]
      ;[newList[index - 1], newList[index]] = [newList[index], newList[index - 1]]
      return newList
    })
  }

  const moveDown = (index) => {
    if (index === selectedFiles.length - 1) return
    setSelectedFiles((prev) => {
      const newList = [...prev]
      ;[newList[index], newList[index + 1]] = [newList[index + 1], newList[index]]
      return newList
    })
  }

  const handleMerge = async () => {
    if (selectedFiles.length < 2) {
      setError('Please select at least 2 files to merge')
      return
    }

    setMerging(true)
    setError(null)
    setSuccess(false)

    try {
      const fileIds = selectedFiles.map((f) => f.file_id)
      const result = await pdfService.merge(fileIds, outputName)
      onMerged({
        file_id: result.file_id,
        filename: outputName,
        originalName: outputName,
        pages: selectedFiles.reduce((sum, f) => sum + f.pages, 0),
        size: 0,
      })
      setSuccess(true)
      setSelectedFiles([])
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Merge failed')
    } finally {
      setMerging(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Merge PDFs</h2>
        <p className="text-sm text-gray-500">
          Select files to merge and arrange them in the desired order.
        </p>
      </div>

      {/* Available files */}
      <div>
        <h3 className="text-sm font-medium text-gray-700 mb-3">
          Available Files
        </h3>
        {files.length === 0 ? (
          <p className="text-sm text-gray-400">No files available. Upload some PDFs first.</p>
        ) : (
          <div className="grid grid-cols-2 gap-2">
            {files.map((file) => {
              const isSelected = selectedFiles.find((f) => f.file_id === file.file_id)
              return (
                <button
                  key={file.file_id}
                  onClick={() => toggleFile(file)}
                  className={`flex items-center p-3 rounded-lg border text-left transition-colors ${
                    isSelected
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3 ${
                    isSelected ? 'border-primary-500 bg-primary-500' : 'border-gray-300'
                  }`}>
                    {isSelected && <Check className="h-4 w-4 text-white" />}
                  </div>
                  <span className="text-sm truncate flex-1">
                    {file.originalName || file.filename}
                  </span>
                </button>
              )
            })}
          </div>
        )}
      </div>

      {/* Selected files order */}
      {selectedFiles.length > 0 && (
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-3">
            Merge Order
          </h3>
          <div className="space-y-2">
            {selectedFiles.map((file, index) => (
              <div
                key={file.file_id}
                className="flex items-center p-3 bg-gray-50 rounded-lg"
              >
                <GripVertical className="h-5 w-5 text-gray-400 mr-2" />
                <span className="text-sm font-medium text-gray-500 mr-3">
                  {index + 1}
                </span>
                <span className="text-sm flex-1 truncate">
                  {file.originalName || file.filename}
                </span>
                <div className="flex space-x-1">
                  <button
                    onClick={() => moveUp(index)}
                    disabled={index === 0}
                    className="p-1 hover:bg-gray-200 rounded disabled:opacity-30 focus:outline-none focus:ring-2 focus:ring-primary-500"
                    aria-label="Move file up"
                    title="Move file up"
                  >
                    <ArrowUp className="h-4 w-4 text-gray-600" />
                  </button>
                  <button
                    onClick={() => moveDown(index)}
                    disabled={index === selectedFiles.length - 1}
                    className="p-1 hover:bg-gray-200 rounded disabled:opacity-30 focus:outline-none focus:ring-2 focus:ring-primary-500"
                    aria-label="Move file down"
                    title="Move file down"
                  >
                    <ArrowDown className="h-4 w-4 text-gray-600" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Output name */}
      <div>
        <label htmlFor="output-filename" className="block text-sm font-medium text-gray-700 mb-2">
          Output Filename
        </label>
        <input
          id="output-filename"
          type="text"
          value={outputName}
          onChange={(e) => setOutputName(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          placeholder="merged.pdf"
        />
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-50 text-green-600 px-4 py-3 rounded-lg text-sm">
          Files merged successfully!
        </div>
      )}

      <button
        onClick={handleMerge}
        disabled={merging || selectedFiles.length < 2}
        className="w-full bg-primary-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-primary-700 focus:ring-4 focus:ring-primary-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {merging ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            Merging...
          </>
        ) : (
          <>
            <Merge className="h-5 w-5 mr-2" />
            Merge {selectedFiles.length} Files
          </>
        )}
      </button>
    </div>
  )
}
