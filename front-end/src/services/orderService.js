import apiClient from './api'

export default {
  getAllOrders() {
    return apiClient.get('/orders')
  },

  getOrderById(id) {
    return apiClient.get(`/orders/${id}`)
  },

  createOrder(orderData) {
    return apiClient.post('/orders', orderData)
  },

  updateOrderStatus(id, status) {
    return apiClient.patch(`/orders/${id}/status`, { status })
  },

  deleteOrder(id) {
    return apiClient.delete(`/orders/${id}`)
  },

  getStatistics() {
    return apiClient.get('/orders/statistics')
  }
}
