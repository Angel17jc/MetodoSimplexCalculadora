import { useQuery } from '@tanstack/react-query'

import { api } from '@/lib/api/cliente'

export function EstadoApi() {
  const { isPending, isError } = useQuery({
    queryKey: ['health'],
    queryFn: api.health,
    refetchInterval: 30_000,
    retry: false,
  })

  const [color, texto] = isPending
    ? ['bg-slate-400', 'Conectando con la API…']
    : isError
      ? ['bg-red-500', 'API sin conexión']
      : ['bg-emerald-500', 'API conectada']

  return (
    <span className="inline-flex items-center gap-2" role="status">
      <span className={`size-2 rounded-full ${color}`} aria-hidden="true" />
      {texto}
    </span>
  )
}
