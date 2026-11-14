import { useState } from 'react'
import { createExam, getApiError } from '../../api/exams.js'
import Button from '../Button/Button.jsx'

export default function ExamForm({ token }) {
  const [title, setTitle] = useState('')
  const [saving, setSaving] = useState(false)
  const [errors, setErrors] = useState({})

  async function handleSubmit(event) {
    event.preventDefault()
    setSaving(true)
    setErrors({})

    try {
      await createExam(token, title)
      window.location.hash = 'exams'
    } catch (error) {
      const titleErrors = error.response?.data?.title
      setErrors(Array.isArray(titleErrors) ? { title: titleErrors.join(' ') } : { general: getApiError(error) })
    } finally {
      setSaving(false)
    }
  }

  return (
    <form className="stack" onSubmit={handleSubmit}>
      <div>
        <label className="form-label" htmlFor="exam-title">Título</label>
        <input id="exam-title" className="form-control" value={title} onChange={(event) => setTitle(event.target.value)}
          aria-invalid={Boolean(errors.title)} aria-describedby={errors.title ? 'exam-title-error' : undefined} />
        {errors.title && <p id="exam-title-error" role="alert" className="exams-field-error">{errors.title}</p>}
      </div>
      {errors.general && <p role="alert" className="status-message status-message--error">{errors.general}</p>}
      <div className="cluster">
        <Button type="submit" disabled={saving}>{saving ? 'Guardando…' : 'Guardar examen'}</Button>
        <a href="#exams">Volver al listado</a>
      </div>
    </form>
  )
}
