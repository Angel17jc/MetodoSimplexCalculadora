import { Link } from 'react-router'

export function NoEncontrada() {
  return (
    <section className="space-y-2">
      <h1 className="text-2xl font-semibold">Página no encontrada</h1>
      <p className="text-slate-600">
        La dirección no existe.{' '}
        <Link to="/calculadora" className="font-medium text-slate-900 underline">
          Ir a la calculadora
        </Link>
      </p>
    </section>
  )
}
