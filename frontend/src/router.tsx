import { createBrowserRouter } from 'react-router'

import App from '@/App.tsx'
import { Layout } from '@/components/layout/Layout.tsx'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [{ index: true, element: <App /> }],
  },
])
