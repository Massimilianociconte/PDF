import { useState, useEffect } from 'react'
import { FileText, Check, Save } from 'lucide-react'
import { pdfService } from '../services/pdfService'

export default function MetadataPanel({ files, onProcessed }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [metadata, setMetadata] = useState({
    title: '',
    author: '',
    subject: '',
    keywords: '',
  })
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    if (selectedFile) {
      loadMetadata()
    }
  }, [selectedFile])

  const loadMetadata = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await pdfService.getMetadata(selectedFile.file_id)
      setMetadata({
        title: data.title || '',
        author: data.author || '',
        subject: data.subject || '',
        keywords: data.keywords || '',
      })
    } catch (err) {
      setError('Failed to load metadata')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    if (!selectedFile) return

    setSaving(true)
    setError(null)
    setSuccess(false)

    try {
      const response = await pdfService.updateMetadata(
        selectedFile.file_id,
        metadata.title || null,
        metadata.author || null,
        metadata.subject || null,
        metadata.keywords || null
      )
      
      onProcessed({
        file_id: response.file_id,
        filename: selectedFile.originalName || selectedFile.filename,
        originalName: selectedFile.originalName || selectedFile.filename,
        pages: selectedFile.pages,
        size: selectedFile.size,
      })
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save metadata')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Edit Metadata</h2>
        <p className="text-sm text-gray-500">
          View and edit PDF document properties.
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
                <span className="text-sm truncate flex-1">
                  {file.originalName || file.filename}
                </span>
              </button>
            ))}
          </div>
        )}
      </div>

      {loading && (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      )}

      {selectedFile && !loading && (
        <>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Title</label>
            <input
              type="text"
              value={metadata.title}
              onChange={(e) => setMetadata({ ...metadata, title: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="Document title"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Author</label>
            <input
              type="text"
              value={metadata.author}
              onChange={(e) => setMetadata({ ...metadata, author: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="Author name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Subject</label>
            <input
              type="text"
              value={metadata.subject}
              onChange={(e) => setMetadata({ ...metadata, subject: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="Document subject"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Keywords</label>
            <input
              type="text"
              value={metadata.keywords}
              onChange={(e) => setMetadata({ ...metadata, keywords: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="Comma-separated keywords"
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
          Metadata saved successfully!
        </div>
      )}

      <button
        onClick={handleSave}
        disabled={saving || !selectedFile || loading}
        className="w-full bg-primary-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-primary-700 focus:ring-4 focus:ring-primary-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {saving ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            Saving...
          </>
        ) : (
          <>
            <Save className="h-5 w-5 mr-2" />
            Save Metadata
          </>
        )}
      </button>
    </div>
  )
}
