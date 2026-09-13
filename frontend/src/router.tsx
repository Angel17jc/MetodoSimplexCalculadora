import { createBrowserRouter, Navigate } from 'react-router'

import { Layout } from '@/components/layout/Layout.tsx'
import { Calculadora } from '@/pages/Calculadora.tsx'
import { Ejemplos } from '@/pages/Ejemplos.tsx'
import { Historial } from '@/pages/Historial.tsx'
import { NoEncontrada } from '@/pages/NoEncontrada.tsx'
import { Solucion } from '@/pages/Solucion.tsx'

export const rutas = [
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Navigate to="/calculadora" replace /> },
      { path: 'calculadora', element: <Calculadora /> },
      { path: 'solucion/:slug?', element: <Solucion /> },
      { path: 'historial', element: <Historial /> },
      { path: 'ejemplos', element: <Ejemplos /> },
      { path: '*', element: <NoEncontrada /> },
    ],
  },
]

export const router = createBrowserRouter(rutas)
