import apiClient from './api'

export default {
  /**
   * @param {Object} params - { page, limit, kategori, search }
   * @returns {Promise} Response dari server
   * Endpoint: GET /api/menu?page=1&limit=10&kategori=Makanan&search=nasi
   */
  getAllMenus(params = {}) {
    return apiClient.get('/menu', { params })
  },

  /**
   * @param {Number} id - ID menu
   * @returns {Promise} Response dari server
   */
  getMenuById(id) {
    return apiClient.get(`/menu/${id}`)
  },

  /**
   * @param {FormData} formData - Data menu dengan gambar
   * @returns {Promise} Response dari server
   * Endpoint: POST /api/menu
   * 
   * Penjelasan:
   * - Pakai FormData karena ada upload file
   * - Header Content-Type otomatis jadi multipart/form-data
   */
  createMenu(formData) {
    return apiClient.post('/menu', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  /**
   * @param {Number} id - ID menu yang akan diupdate
   * @param {FormData} formData - Data baru
   * @returns {Promise} Response dari server
   * Endpoint: PUT /api/menu/{id}
   */
  updateMenu(id, formData) {
    return apiClient.put(`/menu/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  /**
   * @param {Number} id - ID menu yang akan dihapus
   * @returns {Promise} Response dari server
   * Endpoint: DELETE /api/menu/{id}
   */
  deleteMenu(id) {
    return apiClient.delete(`/menu/${id}`)
  },

  /**
   * @param {Number} id - ID menu
   * @returns {Promise} Response dari server
   * Endpoint: PATCH /api/menu/{id}/toggle
   */
  toggleTersedia(id) {
    return apiClient.patch(`/menu/${id}/toggle`)
  }
}
