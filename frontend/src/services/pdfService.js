import api from './api'

export const pdfService = {
  // Upload a PDF file
  upload: async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/pdf/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Get PDF info
  getInfo: async (fileId) => {
    const response = await api.get(`/pdf/info/${fileId}`)
    return response.data
  },

  // Download PDF
  download: async (fileId) => {
    const response = await api.get(`/pdf/download/${fileId}`, {
      responseType: 'blob',
    })
    return response.data
  },

  // Delete PDF
  delete: async (fileId) => {
    const response = await api.delete(`/pdf/${fileId}`)
    return response.data
  },

  // Merge PDFs
  merge: async (fileIds, outputName = 'merged.pdf') => {
    const response = await api.post('/pdf/merge', {
      file_ids: fileIds,
      output_name: outputName,
    })
    return response.data
  },

  // Split PDF
  split: async (fileId, pages) => {
    const response = await api.post('/pdf/split', {
      file_id: fileId,
      pages: pages,
    })
    return response.data
  },

  // Rotate page
  rotate: async (fileId, page, angle) => {
    const formData = new FormData()
    formData.append('page', page)
    formData.append('angle', angle)
    const response = await api.post(`/pdf/rotate/${fileId}`, formData)
    return response.data
  },

  // Extract text
  extractText: async (fileId, page = null) => {
    const params = page ? { page } : {}
    const response = await api.get(`/pdf/text/${fileId}`, { params })
    return response.data
  },

  // OCR PDF
  ocr: async (fileId, page = null) => {
    const formData = new FormData()
    if (page) formData.append('page', page)
    const response = await api.post(`/pdf/ocr/${fileId}`, formData)
    return response.data
  },

  // Get page preview
  getPreview: (fileId, page) => {
    const token = localStorage.getItem('token')
    return `/api/pdf/preview/${fileId}/${page}?token=${token}`
  },

  // Add image to PDF
  addImage: async (fileId, image, page, x, y, width, height) => {
    const formData = new FormData()
    formData.append('image', image)
    formData.append('page', page)
    formData.append('x', x)
    formData.append('y', y)
    if (width) formData.append('width', width)
    if (height) formData.append('height', height)
    const response = await api.post(`/pdf/add-image/${fileId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}

export const conversionService = {
  // Convert image to PDF
  imageToPdf: async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/convert/image-to-pdf', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Convert PDF to images
  pdfToImages: async (fileId, format = 'png', dpi = 150) => {
    const formData = new FormData()
    formData.append('format', format)
    formData.append('dpi', dpi)
    const response = await api.post(`/convert/pdf-to-images/${fileId}`, formData)
    return response.data
  },

  // Convert text to PDF
  textToPdf: async (text, fontSize = 12) => {
    const formData = new FormData()
    formData.append('text', text)
    formData.append('font_size', fontSize)
    const response = await api.post('/convert/text-to-pdf', formData)
    return response.data
  },

  // Convert HTML to PDF
  htmlToPdf: async (html) => {
    const formData = new FormData()
    formData.append('html', html)
    const response = await api.post('/convert/html-to-pdf', formData)
    return response.data
  },
}
