import { useState } from 'react'
import { FileText, Download, Trash2, Eye } from 'lucide-react'
import { pdfService } from '../services/pdfService'

export default function PDFList({ files, selectedFile, onSelect, onDelete }) {
  const [deleting, setDeleting] = useState(null)

  const handleDownload = async (file) => {
    try {
      const blob = await pdfService.download(file.file_id)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = file.originalName || file.filename || `${file.file_id}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Download failed:', error)
    }
  }

  const handleDelete = async (file) => {
    if (!window.confirm('Are you sure you want to delete this file?')) return

    setDeleting(file.file_id)
    try {
      await pdfService.delete(file.file_id)
      onDelete(file.file_id)
    } catch (error) {
      console.error('Delete failed:', error)
    } finally {
      setDeleting(null)
    }
  }

  const formatSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  if (files.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <FileText className="h-12 w-12 mx-auto mb-3 text-gray-300" />
        <p>No files uploaded yet</p>
      </div>
    )
  }

  return (
    <div>
      <h3 className="text-sm font-medium text-gray-700 mb-3">
        Uploaded Files ({files.length})
      </h3>

      <div className="space-y-2">
        {files.map((file) => (
          <div
            key={file.file_id}
            className={`group flex items-center p-3 rounded-lg border transition-colors ${
              selectedFile?.file_id === file.file_id
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
            }`}
          >
            <button
              onClick={() => onSelect(file)}
              className="flex items-center flex-1 min-w-0 text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded-md -ml-2 p-2"
              aria-label={`Select ${file.originalName || file.filename}`}
            >
              <div className="flex-shrink-0 w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                <FileText className="h-5 w-5 text-red-600" />
              </div>

              <div className="ml-3 flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {file.originalName || file.filename}
                </p>
                <p className="text-xs text-gray-500">
                  {file.pages} pages • {formatSize(file.size)}
                </p>
              </div>
            </button>

            <div className="flex items-center space-x-2 ml-2">
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  handleDownload(file)
                }}
                className="p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors focus-visible:ring-2 focus-visible:ring-primary-500 focus:outline-none"
                title="Download"
                aria-label={`Download ${file.originalName || file.filename}`}
              >
                <Download className="h-4 w-4" />
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  handleDelete(file)
                }}
                disabled={deleting === file.file_id}
                className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50 focus-visible:ring-2 focus-visible:ring-red-500 focus:outline-none"
                title="Delete"
                aria-label={`Delete ${file.originalName || file.filename}`}
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
