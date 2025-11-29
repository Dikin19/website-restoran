import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api'


const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})


apiClient.interceptors.request.use(
  config => {
    // Tambahkan token jika ada
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    // Jika data adalah FormData, hapus Content-Type agar browser set otomatis dengan boundary
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    
    console.log(`${config.method.toUpperCase()} ${config.url}`)
    console.log('Request headers:', config.headers)
    console.log('Request data type:', config.data?.constructor?.name)
    return config
  },
  error => {
    console.error('request Error:', error)
    return Promise.reject(error)
  }
)


apiClient.interceptors.response.use(
  response => {
    console.log(`response ${response.config.url}:`, response.data)
    return response
  },
  error => {
    
    if (error.response) {
      
      console.error(`error ${error.response.status}:`, error.response.data)
    } else if (error.request) {
      
      console.error('no response from server')
    } else {
      
      console.error('error:', error.message)
    }
    return Promise.reject(error)
  }
)

export default apiClient
