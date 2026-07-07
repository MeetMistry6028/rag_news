import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

export async function searchArticles(query, topK = 5) {
  const response = await client.post('/search', { query, top_k: topK })
  return response.data
}

export async function askQuestion(question, topK = 5) {
  const response = await client.post('/ask', { question, top_k: topK })
  return response.data
}

export async function healthCheck() {
  const response = await client.get('/health')
  return response.data
}