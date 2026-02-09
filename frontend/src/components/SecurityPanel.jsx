import { useState } from 'react'
import { Lock, Unlock, Check, Eye, EyeOff } from 'lucide-react'
import { pdfService } from '../services/pdfService'

export default function SecurityPanel({ files, onProcessed }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [mode, setMode] = useState('encrypt') // encrypt, decrypt
  const [userPassword, setUserPassword] = useState('')
  const [ownerPassword, setOwnerPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleProcess = async () => {
    if (!selectedFile) {
      setError('Please select a file')
      return
    }
    if (!userPassword) {
      setError('Please enter a password')
      return
    }

    setProcessing(true)
    setError(null)
    setSuccess(false)

    try {
      let response
      if (mode === 'encrypt') {
        response = await pdfService.encrypt(
          selectedFile.file_id, 
          userPassword, 
          ownerPassword || null
        )
      } else {
        response = await pdfService.decrypt(selectedFile.file_id, userPassword)
      }
      
      onProcessed({
        file_id: response.file_id,
        filename: `${mode === 'encrypt' ? 'protected' : 'unlocked'}_${selectedFile.originalName || selectedFile.filename}`,
        originalName: `${mode === 'encrypt' ? 'protected' : 'unlocked'}_${selectedFile.originalName || selectedFile.filename}`,
        pages: selectedFile.pages,
        size: selectedFile.size,
      })
      setSuccess(true)
      setUserPassword('')
      setOwnerPassword('')
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || `${mode === 'encrypt' ? 'Encryption' : 'Decryption'} failed`)
    } finally {
      setProcessing(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">PDF Security</h2>
        <p className="text-sm text-gray-500">
          Protect your PDF with a password or remove existing protection.
        </p>
      </div>

      {/* Mode selection */}
      <div className="flex space-x-2">
        <button
          onClick={() => setMode('encrypt')}
          className={`flex-1 flex items-center justify-center py-2 px-4 rounded-lg border transition-colors ${
            mode === 'encrypt'
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          <Lock className="h-4 w-4 mr-2" />
          Encrypt
        </button>
        <button
          onClick={() => setMode('decrypt')}
          className={`flex-1 flex items-center justify-center py-2 px-4 rounded-lg border transition-colors ${
            mode === 'decrypt'
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          <Unlock className="h-4 w-4 mr-2" />
          Decrypt
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

      {/* Password input */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          {mode === 'encrypt' ? 'User Password' : 'Password'}
        </label>
        <div className="relative">
          <input
            type={showPassword ? 'text' : 'password'}
            value={userPassword}
            onChange={(e) => setUserPassword(e.target.value)}
            className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            placeholder={mode === 'encrypt' ? 'Enter password to protect PDF' : 'Enter password to unlock'}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
          >
            {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Owner password (encrypt only) */}
      {mode === 'encrypt' && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Owner Password (Optional)
          </label>
          <input
            type={showPassword ? 'text' : 'password'}
            value={ownerPassword}
            onChange={(e) => setOwnerPassword(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            placeholder="For advanced permissions (leave empty for same as user)"
          />
          <p className="text-xs text-gray-400 mt-1">
            Owner password allows editing even when user password is set.
          </p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-50 text-green-600 px-4 py-3 rounded-lg text-sm">
          {mode === 'encrypt' ? 'PDF encrypted successfully!' : 'PDF decrypted successfully!'}
        </div>
      )}

      <button
        onClick={handleProcess}
        disabled={processing || !selectedFile || !userPassword}
        className="w-full bg-primary-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-primary-700 focus:ring-4 focus:ring-primary-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {processing ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            {mode === 'encrypt' ? 'Encrypting...' : 'Decrypting...'}
          </>
        ) : (
          <>
            {mode === 'encrypt' ? <Lock className="h-5 w-5 mr-2" /> : <Unlock className="h-5 w-5 mr-2" />}
            {mode === 'encrypt' ? 'Encrypt PDF' : 'Decrypt PDF'}
          </>
        )}
      </button>
    </div>
  )
}
