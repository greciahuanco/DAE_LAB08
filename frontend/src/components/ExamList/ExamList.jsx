import { useEffect, useState } from 'react'
import { deleteExam, getApiError, listExams } from '../../api/exams.js'
import Button from '../Button/Button.jsx'

export default function ExamList({ token }) {
  const [page, setPage] = useState(1)
  const [query, setQuery] = useState(0)
  const [result, setResult] = useState(null)
  const [deleting, setDeleting] = useState(null)
  const [deleteError, setDeleteError] = useState('')
  const current = result?.page === page && result.query === query ? result : null

  useEffect(() => {
    const controller = new AbortController()
    listExams(token, page, controller.signal)
      .then((data) => setResult({ page, query, data }))
      .catch((error) => {
        if (!controller.signal.aborted) setResult({ page, query, error: getApiError(error) })
      })

    return () => controller.abort()
  }, [token, page, query])

  async function handleDelete(exam) {
    if (!window.confirm(`¿Eliminar «${exam.title}»?`)) return
    setDeleting(exam.id)
    setDeleteError('')

    try {
      await deleteExam(token, exam.id)
      if (current.data.results.length === 1 && page > 1) setPage(page - 1)
      setQuery((value) => value + 1)
    } catch (error) {
      setDeleteError(getApiError(error))
    } finally {
      setDeleting(null)
    }
  }

  return (
    <>
      <div className="cluster exams-actions">
        <a href="#exams/new">Crear examen</a>
        <Button variant="secondary" disabled={!current || deleting !== null} onClick={() => setQuery(query + 1)}>
          Actualizar listado
        </Button>
      </div>

      {!current && (
        <div className="exams-skeleton" role="status">
          <p>Cargando exámenes…</p>
          <div aria-hidden="true" />
          <div aria-hidden="true" />
          <div aria-hidden="true" />
        </div>
      )}

      {current?.error && (
        <div className="stack">
          <p role="alert" className="status-message status-message--error">{current.error}</p>
          <Button variant="secondary" onClick={() => setQuery(query + 1)}>Reintentar</Button>
        </div>
      )}

      {deleteError && <p role="alert" className="status-message status-message--error">{deleteError}</p>}

      {current?.data && (
        <>
          <div className="exams-table-wrap">
            <table className="exams-table" aria-label="Exámenes registrados">
              <thead><tr><th scope="col">ID</th><th scope="col">Título</th><th scope="col">Preguntas</th><th scope="col">Acciones</th></tr></thead>
              <tbody>
                {current.data.results.map((exam) => (
                  <tr key={exam.id}>
                    <td>{exam.id}</td>
                    <td>{exam.title}</td>
                    <td>{exam.question_count}</td>
                    <td>
                      <Button variant="secondary" disabled={deleting !== null} onClick={() => handleDelete(exam)}>
                        {deleting === exam.id ? 'Eliminando…' : 'Eliminar'}
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {current.data.count === 0 && <p role="status">Todavía no hay exámenes registrados</p>}
          {(current.data.previous || current.data.next) && (
            <div className="cluster exams-actions">
              <Button variant="secondary" disabled={!current.data.previous || deleting !== null} onClick={() => setPage(page - 1)}>Anterior</Button>
              <span>Página {page}</span>
              <Button variant="secondary" disabled={!current.data.next || deleting !== null} onClick={() => setPage(page + 1)}>Siguiente</Button>
            </div>
          )}
        </>
      )}
    </>
  )
}
