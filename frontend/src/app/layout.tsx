import type { Metadata } from 'next'
import {
  ColorSchemeScript,
  mantineHtmlProps,
  MantineProvider
} from '@mantine/core'
import { theme } from '@/theme'

import '@/assets/styles/index.css'

export const metadata: Metadata = {
  title: 'K12 R&D',
  description: 'Next.js project with Mantine and Tailwind CSS'
}

export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" {...mantineHtmlProps}>
      <head>
        <ColorSchemeScript />
        <link rel="shortcut icon" href="/favicon.svg" />
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width, user-scalable=no"
        />
      </head>
      <body>
        <MantineProvider theme={theme}>{children}</MantineProvider>
      </body>
    </html>
  )
}
