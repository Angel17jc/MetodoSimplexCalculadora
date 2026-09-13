import type { components } from '@/lib/api/esquema'

export type Problema = components['schemas']['Problema']
export type RespuestaResolver = components['schemas']['RespuestaResolver']
export type Ejemplo = components['schemas']['Ejemplo']

// En desarrollo Vite reenvía /api al backend; en producción lo hace Nginx.
const URL_BASE: string = import.meta.env.VITE_API_URL ?? '/api/v1'

export class ErrorApi extends Error {
  readonly estado: number
  readonly detalle: unknown

  constructor(estado: number, detalle: unknown) {
    super(typeof detalle === 'string' ? detalle : `La API respondió con el error ${estado}`)
    this.name = 'ErrorApi'
    this.estado = estado
    this.detalle = detalle
  }
}

async function solicitar<T>(ruta: string, opciones: RequestInit = {}): Promise<T> {
  const respuesta = await fetch(`${URL_BASE}${ruta}`, {
    ...opciones,
    headers: { 'Content-Type': 'application/json', ...opciones.headers },
  })

  if (!respuesta.ok) {
    const cuerpo = await respuesta.json().catch(() => null)
    throw new ErrorApi(respuesta.status, cuerpo?.detail ?? cuerpo)
  }

  return (await respuesta.json()) as T
}

export const api = {
  health: () => solicitar<{ estado: string }>('/health'),
  ejemplos: () => solicitar<Ejemplo[]>('/ejemplos'),
  resolver: (problema: Problema) =>
    solicitar<RespuestaResolver>('/resolver', {
      method: 'POST',
      body: JSON.stringify(problema),
    }),
}
