import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { rutas } from '@/router.tsx'

function renderizarEn(ruta: string) {
  const router = createMemoryRouter(rutas, { initialEntries: [ruta] })
  const clienteConsultas = new QueryClient({ defaultOptions: { queries: { retry: false } } })

  render(
    <QueryClientProvider client={clienteConsultas}>
      <RouterProvider router={router} />
    </QueryClientProvider>,
  )
}

describe('navegación', () => {
  beforeEach(() => {
    const respuesta = new Response(JSON.stringify({ estado: 'ok' }), { status: 200 })
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(respuesta))
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('redirige la raíz a la calculadora', async () => {
    renderizarEn('/')

    expect(await screen.findByRole('heading', { name: 'Calculadora' })).toBeInTheDocument()
  })

  it('cambia de página desde el menú y marca el enlace activo', async () => {
    renderizarEn('/calculadora')

    await userEvent.click(screen.getByRole('link', { name: 'Ejemplos' }))

    expect(await screen.findByRole('heading', { name: 'Ejemplos' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Ejemplos' })).toHaveAttribute('aria-current', 'page')
  })

  it('muestra el estado de la API en el pie de página', async () => {
    renderizarEn('/calculadora')

    expect(await screen.findByText('API conectada')).toBeInTheDocument()
  })

  it('muestra una página para direcciones que no existen', async () => {
    renderizarEn('/no-existe')

    expect(
      await screen.findByRole('heading', { name: 'Página no encontrada' }),
    ).toBeInTheDocument()
  })
})
