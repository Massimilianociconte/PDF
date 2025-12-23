import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Image, FileText, Upload, Check } from 'lucide-react'
import { conversionService, pdfService } from '../services/pdfService'

export default function ConvertPanel({ onConverted }) {
  const [conversionType, setConversionType] = useState('image-to-pdf')
  const [converting, setConverting] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const [text, setText] = useState('')
  const [html, setHtml] = useState('')

  const onDropImage = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0]
    if (!file) return

    setConverting(true)
    setError(null)
    setSuccess(false)

    try {
      const result = await conversionService.imageToPdf(file)
      onConverted({
        file_id: result.file_id,
        filename: `${file.name}.pdf`,
        originalName: `${file.name}.pdf`,
        pages: 1,
        size: file.size,
      })
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Conversion failed')
    } finally {
      setConverting(false)
    }
  }, [onConverted])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: onDropImage,
    accept: {
      'image/*': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    },
    maxFiles: 1,
    disabled: converting
  })

  const handleTextToPdf = async () => {
    if (!text.trim()) {
      setError('Please enter some text')
      return
    }

    setConverting(true)
    setError(null)
    setSuccess(false)

    try {
      const result = await conversionService.textToPdf(text)
      onConverted({
        file_id: result.file_id,
        filename: 'text.pdf',
        originalName: 'text.pdf',
        pages: 1,
        size: 0,
      })
      setSuccess(true)
      setText('')
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Conversion failed')
    } finally {
      setConverting(false)
    }
  }

  const handleHtmlToPdf = async () => {
    if (!html.trim()) {
      setError('Please enter some HTML')
      return
    }

    setConverting(true)
    setError(null)
    setSuccess(false)

    try {
      const result = await conversionService.htmlToPdf(html)
      onConverted({
        file_id: result.file_id,
        filename: 'html.pdf',
        originalName: 'html.pdf',
        pages: 1,
        size: 0,
      })
      setSuccess(true)
      setHtml('')
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Conversion failed')
    } finally {
      setConverting(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Convert to PDF</h2>
        <p className="text-sm text-gray-500">
          Convert various formats to PDF.
        </p>
      </div>

      {/* Conversion type selector */}
      <div className="flex space-x-2">
        {[
          { id: 'image-to-pdf', label: 'Image', icon: Image },
          { id: 'text-to-pdf', label: 'Text', icon: FileText },
          { id: 'html-to-pdf', label: 'HTML', icon: FileText },
        ].map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setConversionType(id)}
            className={`flex items-center px-4 py-2 rounded-lg border transition-colors ${
              conversionType === id
                ? 'border-primary-500 bg-primary-50 text-primary-700'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <Icon className="h-4 w-4 mr-2" />
            {label}
          </button>
        ))}
      </div>

      {/* Image to PDF */}
      {conversionType === 'image-to-pdf' && (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : converting
              ? 'border-gray-200 bg-gray-50 cursor-not-allowed'
              : 'border-gray-300 hover:border-primary-400 hover:bg-primary-50'
          }`}
        >
          <input {...getInputProps()} />

          {converting ? (
            <div className="space-y-3">
              <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600 mx-auto"></div>
              <p className="text-gray-600">Converting...</p>
            </div>
          ) : success ? (
            <div className="space-y-3">
              <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                <Check className="h-6 w-6 text-green-600" />
              </div>
              <p className="text-green-600 font-medium">Conversion successful!</p>
            </div>
          ) : (
            <>
              <Image className="h-10 w-10 text-gray-400 mx-auto mb-3" />
              <p className="text-gray-600">
                {isDragActive
                  ? 'Drop the image here'
                  : 'Drag & drop an image here, or click to select'}
              </p>
              <p className="text-sm text-gray-400 mt-2">
                Supports JPG, PNG, GIF, BMP, TIFF, WebP
              </p>
            </>
          )}
        </div>
      )}

      {/* Text to PDF */}
      {conversionType === 'text-to-pdf' && (
        <div className="space-y-4">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="w-full h-48 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
            placeholder="Enter your text here..."
          />
          <button
            onClick={handleTextToPdf}
            disabled={converting || !text.trim()}
            className="w-full bg-primary-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-primary-700 focus:ring-4 focus:ring-primary-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {converting ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Converting...
              </>
            ) : (
              <>
                <FileText className="h-5 w-5 mr-2" />
                Convert to PDF
              </>
            )}
          </button>
        </div>
      )}

      {/* HTML to PDF */}
      {conversionType === 'html-to-pdf' && (
        <div className="space-y-4">
          <textarea
            value={html}
            onChange={(e) => setHtml(e.target.value)}
            className="w-full h-48 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none font-mono text-sm"
            placeholder="<h1>Hello World</h1>&#10;<p>Your HTML content here...</p>"
          />
          <button
            onClick={handleHtmlToPdf}
            disabled={converting || !html.trim()}
            className="w-full bg-primary-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-primary-700 focus:ring-4 focus:ring-primary-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {converting ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Converting...
              </>
            ) : (
              <>
                <FileText className="h-5 w-5 mr-2" />
                Convert to PDF
              </>
            )}
          </button>
        </div>
      )}

      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {success && conversionType !== 'image-to-pdf' && (
        <div className="bg-green-50 text-green-600 px-4 py-3 rounded-lg text-sm">
          Conversion successful!
        </div>
      )}
    </div>
  )
}
