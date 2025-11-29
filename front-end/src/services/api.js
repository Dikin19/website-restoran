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
    
    console.log(`${config.method.toUpperCase()} ${config.url}`)
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
