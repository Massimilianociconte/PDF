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

  // ============= ADVANCED FEATURES =============

  // Compress PDF
  compress: async (fileId) => {
    const response = await api.post(`/pdf/compress/${fileId}`)
    return response.data
  },

  // Add watermark
  watermark: async (fileId, text, opacity = 0.3, angle = 45) => {
    const response = await api.post('/pdf/watermark', {
      file_id: fileId,
      text: text,
      opacity: opacity,
      angle: angle,
    })
    return response.data
  },

  // Encrypt PDF
  encrypt: async (fileId, userPassword, ownerPassword = null) => {
    const response = await api.post('/pdf/encrypt', {
      file_id: fileId,
      user_password: userPassword,
      owner_password: ownerPassword,
    })
    return response.data
  },

  // Decrypt PDF
  decrypt: async (fileId, password) => {
    const response = await api.post('/pdf/decrypt', {
      file_id: fileId,
      password: password,
    })
    return response.data
  },

  // Delete pages
  deletePages: async (fileId, pages) => {
    const response = await api.post('/pdf/delete-pages', {
      file_id: fileId,
      pages: pages,
    })
    return response.data
  },

  // Reorder pages
  reorderPages: async (fileId, newOrder) => {
    const response = await api.post('/pdf/reorder-pages', {
      file_id: fileId,
      new_order: newOrder,
    })
    return response.data
  },

  // Add text annotation
  addText: async (fileId, text, page, x, y, fontSize = 12, color = '0,0,0') => {
    const formData = new FormData()
    formData.append('text', text)
    formData.append('page', page)
    formData.append('x', x)
    formData.append('y', y)
    formData.append('font_size', fontSize)
    formData.append('color', color)
    const response = await api.post(`/pdf/add-text/${fileId}`, formData)
    return response.data
  },

  // Add highlight
  addHighlight: async (fileId, page, x0, y0, x1, y1, color = '1,1,0') => {
    const formData = new FormData()
    formData.append('page', page)
    formData.append('x0', x0)
    formData.append('y0', y0)
    formData.append('x1', x1)
    formData.append('y1', y1)
    formData.append('color', color)
    const response = await api.post(`/pdf/highlight/${fileId}`, formData)
    return response.data
  },

  // Redact area
  redact: async (fileId, page, x0, y0, x1, y1) => {
    const formData = new FormData()
    formData.append('page', page)
    formData.append('x0', x0)
    formData.append('y0', y0)
    formData.append('x1', x1)
    formData.append('y1', y1)
    const response = await api.post(`/pdf/redact/${fileId}`, formData)
    return response.data
  },

  // Add page numbers
  addPageNumbers: async (fileId, position = 'bottom', alignment = 'center', startNum = 1) => {
    const response = await api.post('/pdf/page-numbers', {
      file_id: fileId,
      position: position,
      alignment: alignment,
      start_num: startNum,
    })
    return response.data
  },

  // Add header/footer
  addHeaderFooter: async (fileId, headerText = null, footerText = null) => {
    const response = await api.post('/pdf/header-footer', {
      file_id: fileId,
      header_text: headerText,
      footer_text: footerText,
    })
    return response.data
  },

  // Get metadata
  getMetadata: async (fileId) => {
    const response = await api.get(`/pdf/metadata/${fileId}`)
    return response.data
  },

  // Update metadata
  updateMetadata: async (fileId, title, author, subject, keywords) => {
    const response = await api.post('/pdf/metadata', {
      file_id: fileId,
      title: title,
      author: author,
      subject: subject,
      keywords: keywords,
    })
    return response.data
  },

  // Extract images
  extractImages: async (fileId) => {
    const response = await api.post(`/pdf/extract-images/${fileId}`)
    return response.data
  },

  // Sign PDF
  sign: async (fileId, signatureFile, page, x, y, width = 100, height = 50) => {
    const formData = new FormData()
    formData.append('signature', signatureFile)
    formData.append('page', page)
    formData.append('x', x)
    formData.append('y', y)
    formData.append('width', width)
    formData.append('height', height)
    const response = await api.post(`/pdf/sign/${fileId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Flatten PDF
  flatten: async (fileId) => {
    const response = await api.post(`/pdf/flatten/${fileId}`)
    return response.data
  },

  // Crop page
  crop: async (fileId, page, x0, y0, x1, y1) => {
    const formData = new FormData()
    formData.append('page', page)
    formData.append('x0', x0)
    formData.append('y0', y0)
    formData.append('x1', x1)
    formData.append('y1', y1)
    const response = await api.post(`/pdf/crop/${fileId}`, formData)
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
