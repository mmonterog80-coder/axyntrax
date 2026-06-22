'use client';

import { useState } from 'react';
import { useAIAssistant } from '@/hooks/useAIAssistant';

export default function Home() {
  const { isProcessing, lastResponse, injectIndustryData } = useAIAssistant('clinica');
  const [status, setStatus] = useState<string>('Esperando órdenes...');

  const handleInjectData = async () => {
    setStatus('Inyectando esquema de clínica...');
    const result = await injectIndustryData({
      targetModules: ['pacientes', 'citas'],
      schema: {
        pacientes: { camposExtra: ['historial_medico', 'alergias'] }
      }
    });
    
    if (result.success) {
      setStatus(`¡Éxito! La IA adaptó el CRM: ${JSON.stringify((result as any).data?.adaptedModules)}`);
    } else {
      setStatus(`Error: ${result.error}`);
    }
  };

  return (
    <main>
      <h2>Panel de Control CRM</h2>
      <p>Este CRM está potenciado por <strong>Bones (IA Creadora)</strong> y acoplado al Constructor de Ecosistemas.</p>
      
      <div style={{ marginTop: '20px', padding: '15px', border: '1px solid #444', borderRadius: '8px' }}>
        <h3>Prueba de Integración IA</h3>
        <button 
          onClick={handleInjectData}
          disabled={isProcessing}
          style={{ padding: '10px 20px', background: isProcessing ? '#555' : '#0070f3', color: '#fff', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
        >
          {isProcessing ? 'Procesando...' : 'Adaptar CRM a Clínica'}
        </button>
        <p style={{ marginTop: '10px', color: '#00ff00' }}>{status}</p>
      </div>

      {lastResponse && (
        <pre style={{ marginTop: '20px', background: '#111', padding: '15px', overflowX: 'auto' }}>
          {JSON.stringify(lastResponse, null, 2)}
        </pre>
      )}
    </main>
  );
}
