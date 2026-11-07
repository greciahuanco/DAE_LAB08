import { useEffect, useState } from 'react'
import { movies } from '../data/movies.js'

const premiereMovies = movies.slice(0, 3)
const requestDelay = 1200
const loadingState = { status: 'loading', data: [], error: null }

export function usePremieres({ shouldFail = false } = {}) {
  const [request, setRequest] = useState(null)

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const result = shouldFail
        ? { status: 'error', data: [], error: 'No se pudieron cargar los estrenos' }
        : { status: 'success', data: premiereMovies, error: null }

      setRequest({ shouldFail, result })
    }, requestDelay)

    return () => window.clearTimeout(timer)
  }, [shouldFail])

  return request?.shouldFail === shouldFail ? request.result : loadingState
}
