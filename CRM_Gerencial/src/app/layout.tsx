export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body>
        <div style={{ padding: '20px', background: '#0a0a0a', color: '#fff', minHeight: '100vh' }}>
          <header style={{ borderBottom: '1px solid #333', paddingBottom: '10px', marginBottom: '20px' }}>
            <h1>Axyntrax CRM - Modo Modular (Bones AI)</h1>
          </header>
          {children}
        </div>
      </body>
    </html>
  )
}
