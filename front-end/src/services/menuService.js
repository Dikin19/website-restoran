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
   * Note: Axios otomatis set Content-Type untuk FormData
   */
  createMenu(formData) {
    return apiClient.post('/menu', formData)
  },

  /**
   * @param {Number} id - ID menu yang akan diupdate
   * @param {FormData} formData - Data baru
   * @returns {Promise} Response dari server
   * Endpoint: POST /api/menu/update/{id}
   */
  updateMenu(id, formData) {
    return apiClient.post(`/menu/update/${id}`, formData)
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
