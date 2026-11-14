import { useState } from 'react'
import Button from '../Button/Button.jsx'
import ExamForm from '../ExamForm/ExamForm.jsx'
import ExamList from '../ExamList/ExamList.jsx'
import './ExamsPage.css'

const tokenStorageKey = 'dae-lab12-token'

export default function ExamsPage({ creating }) {
  const [token, setToken] = useState(() => sessionStorage.getItem(tokenStorageKey) || '')
  const [tokenInput, setTokenInput] = useState('')

  function connect(event) {
    event.preventDefault()
    const nextToken = tokenInput.trim()
    if (!nextToken) return
    sessionStorage.setItem(tokenStorageKey, nextToken)
    setToken(nextToken)
    setTokenInput('')
  }

  function disconnect() {
    sessionStorage.removeItem(tokenStorageKey)
    setToken('')
  }

  return (
    <main className="container exams-page">
      <div className="cluster exams-actions">
        <a href="#inicio">Volver a la cartelera</a>
        {token && <Button variant="secondary" onClick={disconnect}>Desconectar API</Button>}
      </div>
      <h1>{creating && token ? 'Crear examen' : 'Exámenes'}</h1>
      {!token ? (
        <form className="stack" onSubmit={connect}>
          <div>
            <label className="form-label" htmlFor="api-token">Token de Django</label>
            <input id="api-token" className="form-control" type="password" autoComplete="off" required
              value={tokenInput} onChange={(event) => setTokenInput(event.target.value)} />
          </div>
          <Button type="submit">Conectar API</Button>
        </form>
      ) : creating ? <ExamForm token={token} /> : <ExamList token={token} />}
    </main>
  )
}
