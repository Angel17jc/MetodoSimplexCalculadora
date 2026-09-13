import { useParams } from 'react-router'

export function Solucion() {
  const { slug } = useParams()

  return (
    <section className="space-y-2">
      <h1 className="text-2xl font-semibold">Solución</h1>
      <p className="text-slate-600">
        Aquí va el modo paso a paso con las tablas y cada operación (Sprints 1 y 2).
      </p>
      {slug && <p className="text-sm text-slate-500">Problema compartido: {slug}</p>}
    </section>
  )
}
