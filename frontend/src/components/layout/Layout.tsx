import { NavLink, Outlet } from 'react-router'

const ENLACES = [
  { a: '/calculadora', texto: 'Calculadora' },
  { a: '/ejemplos', texto: 'Ejemplos' },
  { a: '/historial', texto: 'Historial' },
]

export function Layout() {
  return (
    <div className="flex min-h-svh flex-col bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-4 py-3">
          <NavLink to="/calculadora" className="flex items-center gap-2 font-semibold">
            <img src="/icono.svg" alt="" className="size-7" />
            Simplex Paso a Paso
          </NavLink>
          <nav aria-label="Principal">
            <ul className="flex gap-1">
              {ENLACES.map((enlace) => (
                <li key={enlace.a}>
                  <NavLink
                    to={enlace.a}
                    className={({ isActive }) =>
                      `rounded-md px-3 py-2 text-sm font-medium ${
                        isActive ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-100'
                      }`
                    }
                  >
                    {enlace.texto}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </header>

      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8">
        <Outlet />
      </main>

      <footer className="border-t border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-4 py-3 text-sm text-slate-500">
          Método simplex y Dos Fases · Investigación de Operaciones
        </div>
      </footer>
    </div>
  )
}
