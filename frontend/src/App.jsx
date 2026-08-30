import { useEffect, useState } from 'react'
import axios from 'axios'

export default function App() {
  const [capsulas, setCapsulas] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Busca as cápsulas salvas no backend Django
    axios.get('http://127.0.0.1:8000/api/capsulas/')
      .then(response => {
        setCapsulas(response.data)
        setLoading(false)
      })
      .catch(error => {
        console.error('Erro ao buscar cápsulas:', error)
        setLoading(false)
      })
  }, [])

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-blue-400 mb-6 text-center">
          Cápsulas do Tempo
        </h1>

        {loading ? (
          <p className="text-center text-slate-400">Carregando cápsulas...</p>
        ) : capsulas.length === 0 ? (
          <div className="bg-slate-800 p-6 rounded-xl text-center border border-slate-700">
            <p className="text-slate-400">Nenhuma cápsula cadastrada ainda.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {capsulas.map((capsula) => (
              <div 
                key={capsula.id} 
                className="bg-slate-800 p-5 rounded-xl border border-slate-700 shadow-md"
              >
                <h2 className="text-xl font-bold text-blue-300 mb-2">{capsula.titulo}</h2>
                <p className="text-slate-300 mb-4">{capsula.conteudo}</p>
                <div className="text-xs text-slate-400 flex justify-between">
                  <span>Lat: {capsula.latitude}</span>
                  <span>Lng: {capsula.longitude}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}