import apiClient from './api'

export default {
  /**
   * @param {Object} credentials - { username, password }
   * @returns {Promise} Response dari server
   */
  
  login(credentials) {
    return apiClient.post('/auth/login', credentials)
  }
}
