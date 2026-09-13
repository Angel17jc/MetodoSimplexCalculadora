import { afterEach, describe, expect, it, vi } from 'vitest'

import { api, ErrorApi } from '@/lib/api/cliente'

function respuestaJson(cuerpo: unknown, estado = 200): Response {
  return new Response(JSON.stringify(cuerpo), {
    status: estado,
    headers: { 'Content-Type': 'application/json' },
  })
}

describe('cliente de la API', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('consulta /api/v1/health', async () => {
    const fetchSimulado = vi.fn().mockResolvedValue(respuestaJson({ estado: 'ok' }))
    vi.stubGlobal('fetch', fetchSimulado)

    await expect(api.health()).resolves.toEqual({ estado: 'ok' })
    expect(fetchSimulado).toHaveBeenCalledWith('/api/v1/health', expect.any(Object))
  })

  it('lanza ErrorApi con el detalle que envía el backend', async () => {
    const detalle = 'El motor simplex se implementa en el Sprint 1'
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(respuestaJson({ detail: detalle }, 501)))

    const error = await api
      .resolver({ objetivo: 'max', coef_objetivo: ['1'], restricciones: [] })
      .catch((motivo: unknown) => motivo)

    expect(error).toBeInstanceOf(ErrorApi)
    expect(error).toMatchObject({ estado: 501, message: detalle })
  })
})
