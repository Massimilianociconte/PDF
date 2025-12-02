import { useState } from 'react'
import { 
  FileText, 
  Upload, 
  Merge, 
  Scissors, 
  RotateCw, 
  FileSearch,
  Image,
  LogOut,
  Download,
  Trash2,
  ChevronRight,
  Minimize2,
  Droplet,
  Lock,
  PenTool,
  ListOrdered,
  FileEdit,
  PenLine
} from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import FileUploader from '../components/FileUploader'
import PDFList from '../components/PDFList'
import MergePanel from '../components/MergePanel'
import SplitPanel from '../components/SplitPanel'
import ConvertPanel from '../components/ConvertPanel'
import OCRPanel from '../components/OCRPanel'
import CompressPanel from '../components/CompressPanel'
import WatermarkPanel from '../components/WatermarkPanel'
import SecurityPanel from '../components/SecurityPanel'
import AnnotatePanel from '../components/AnnotatePanel'
import PageToolsPanel from '../components/PageToolsPanel'
import MetadataPanel from '../components/MetadataPanel'
import SignPanel from '../components/SignPanel'

const tabs = [
  { id: 'upload', name: 'Upload', icon: Upload },
  { id: 'merge', name: 'Merge', icon: Merge },
  { id: 'split', name: 'Split', icon: Scissors },
  { id: 'convert', name: 'Convert', icon: Image },
  { id: 'ocr', name: 'OCR', icon: FileSearch },
  { id: 'compress', name: 'Compress', icon: Minimize2 },
  { id: 'watermark', name: 'Watermark', icon: Droplet },
  { id: 'security', name: 'Security', icon: Lock },
  { id: 'annotate', name: 'Annotate', icon: PenTool },
  { id: 'pagetools', name: 'Page Tools', icon: ListOrdered },
  { id: 'metadata', name: 'Metadata', icon: FileEdit },
  { id: 'sign', name: 'Sign', icon: PenLine },
]

export default function DashboardPage() {
  const { user, logout } = useAuth()
  const [activeTab, setActiveTab] = useState('upload')
  const [files, setFiles] = useState([])
  const [selectedFile, setSelectedFile] = useState(null)

  const handleFileUploaded = (fileInfo) => {
    setFiles(prev => [...prev, fileInfo])
  }

  const handleFileDeleted = (fileId) => {
    setFiles(prev => prev.filter(f => f.file_id !== fileId))
    if (selectedFile?.file_id === fileId) {
      setSelectedFile(null)
    }
  }

  const renderPanel = () => {
    switch (activeTab) {
      case 'upload':
        return (
          <div className="space-y-6">
            <FileUploader onFileUploaded={handleFileUploaded} />
            <PDFList 
              files={files} 
              selectedFile={selectedFile}
              onSelect={setSelectedFile}
              onDelete={handleFileDeleted}
            />
          </div>
        )
      case 'merge':
        return <MergePanel files={files} onMerged={handleFileUploaded} />
      case 'split':
        return <SplitPanel files={files} onSplit={handleFileUploaded} />
      case 'convert':
        return <ConvertPanel onConverted={handleFileUploaded} />
      case 'ocr':
        return <OCRPanel files={files} />
      case 'compress':
        return <CompressPanel files={files} onCompressed={handleFileUploaded} />
      case 'watermark':
        return <WatermarkPanel files={files} onWatermarked={handleFileUploaded} />
      case 'security':
        return <SecurityPanel files={files} onProcessed={handleFileUploaded} />
      case 'annotate':
        return <AnnotatePanel files={files} onProcessed={handleFileUploaded} />
      case 'pagetools':
        return <PageToolsPanel files={files} onProcessed={handleFileUploaded} />
      case 'metadata':
        return <MetadataPanel files={files} onProcessed={handleFileUploaded} />
      case 'sign':
        return <SignPanel files={files} onSigned={handleFileUploaded} />
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <FileText className="h-8 w-8 text-primary-600" />
              <span className="ml-2 text-xl font-semibold text-gray-900">
                PDF Manipulator
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                {user?.username}
              </span>
              <button
                onClick={logout}
                className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-12 gap-6">
          {/* Sidebar */}
          <aside className="col-span-12 md:col-span-3">
            <nav className="bg-white rounded-xl shadow-sm p-2">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center px-4 py-3 rounded-lg text-left transition-colors ${
                      activeTab === tab.id
                        ? 'bg-primary-50 text-primary-700'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="h-5 w-5 mr-3" />
                    <span className="font-medium">{tab.name}</span>
                    {activeTab === tab.id && (
                      <ChevronRight className="h-5 w-5 ml-auto" />
                    )}
                  </button>
                )
              })}
            </nav>
          </aside>

          {/* Content */}
          <div className="col-span-12 md:col-span-9">
            <div className="bg-white rounded-xl shadow-sm p-6">
              {renderPanel()}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
