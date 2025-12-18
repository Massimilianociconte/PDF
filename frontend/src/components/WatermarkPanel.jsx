import { useState } from 'react'
import { Droplet, Check } from 'lucide-react'
import { pdfService } from '../services/pdfService'

export default function WatermarkPanel({ files, onWatermarked }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [text, setText] = useState('')
  const [opacity, setOpacity] = useState(0.3)
  const [angle, setAngle] = useState(45)
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleAddWatermark = async () => {
    if (!selectedFile) {
      setError('Please select a file')
      return
    }
    if (!text.trim()) {
      setError('Please enter watermark text')
      return
    }

    setProcessing(true)
    setError(null)
    setSuccess(false)

    try {
      const response = await pdfService.watermark(selectedFile.file_id, text, opacity, angle)
      onWatermarked({
        file_id: response.file_id,
        filename: `watermarked_${selectedFile.originalName || selectedFile.filename}`,
        originalName: `watermarked_${selectedFile.originalName || selectedFile.filename}`,
        pages: selectedFile.pages,
        size: selectedFile.size,
      })
      setSuccess(true)
      setText('')
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Watermark failed')
    } finally {
      setProcessing(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Add Watermark</h2>
        <p className="text-sm text-gray-500">
          Add a text watermark to all pages of your PDF.
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

      {/* Watermark text */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Watermark Text
        </label>
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          placeholder="e.g., CONFIDENTIAL, DRAFT, SAMPLE"
        />
      </div>

      {/* Opacity slider */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Opacity: {(opacity * 100).toFixed(0)}%
        </label>
        <input
          type="range"
          min="0.1"
          max="1"
          step="0.1"
          value={opacity}
          onChange={(e) => setOpacity(parseFloat(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
      </div>

      {/* Angle */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Angle: {angle}°
        </label>
        <input
          type="range"
          min="0"
          max="90"
          step="15"
          value={angle}
          onChange={(e) => setAngle(parseInt(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-50 text-green-600 px-4 py-3 rounded-lg text-sm">
          Watermark added successfully!
        </div>
      )}

      <button
        onClick={handleAddWatermark}
        disabled={processing || !selectedFile || !text.trim()}
        className="w-full bg-primary-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-primary-700 focus:ring-4 focus:ring-primary-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {processing ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            Adding Watermark...
          </>
        ) : (
          <>
            <Droplet className="h-5 w-5 mr-2" />
            Add Watermark
          </>
        )}
      </button>
    </div>
  )
}
