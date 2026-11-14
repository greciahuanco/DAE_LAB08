import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/',
  timeout: 8000,
})

function authenticated(token) {
  return { headers: { Authorization: `Token ${token}` } }
}

export async function listExams(token, page, signal) {
  const { data } = await api.get('exams/', {
    ...authenticated(token),
    params: { page, ordering: '-id' },
    signal,
  })
  return data
}

export async function createExam(token, title) {
  const { data } = await api.post('exams/', { title }, authenticated(token))
  return data
}

export function deleteExam(token, id) {
  return api.delete(`exams/${id}/`, authenticated(token))
}

export function getApiError(error) {
  if (error.response?.status === 401 || error.response?.status === 403) {
    return 'Verifica el token de acceso a Django'
  }
  return error.response?.data?.detail
    || 'No se pudo completar la petición. Comprueba que la API de Django esté en ejecución'
}
