'use client';

import { motion } from 'framer-motion';
import { Terminal } from 'lucide-react';
import { useState, useEffect } from 'react';

interface Log {
  id: number;
  time: string;
  source: string;
  message: string;
  type: 'info' | 'warn' | 'error' | 'success';
}

export function TelemetryLog() {
  const [logs, setLogs] = useState<Log[]>([]);

  useEffect(() => {
    // Simulaci\u00f3n de log stream L99
    const dummyLogs = [
      { source: 'OMNI-CORE', message: 'Iniciando handshakes seguros', type: 'info' },
      { source: 'QWEN-32B', message: 'Modelo local cargado en memoria unificada', type: 'success' },
      { source: 'DEEPSEEK', message: 'Enrutador as\u00edncrono sincronizado', type: 'success' },
      { source: 'TELEGRAM', message: 'Webhook anclado en Railway', type: 'success' },
      { source: 'HETZNER', message: 'Nodo vision-core listo para inferencia RT-DETR', type: 'info' },
    ];

    let i = 0;
    const interval = setInterval(() => {
      if (i < dummyLogs.length) {
        const newLog: Log = {
          id: Date.now(),
          time: new Date().toISOString().split('T')[1].slice(0, -1),
          source: dummyLogs[i].source,
          message: dummyLogs[i].message,
          type: dummyLogs[i].type as Log['type']
        };
        setLogs(prev => [...prev, newLog]);
        i++;
      } else {
        clearInterval(interval);
      }
    }, 800);

    return () => clearInterval(interval);
  }, []);

  const getColor = (type: string) => {
    switch (type) {
      case 'info': return 'text-hud-cyan';
      case 'success': return 'text-hud-emerald';
      case 'warn': return 'text-amber-400';
      case 'error': return 'text-hud-danger';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-2 mb-4 border-b border-white/10 pb-3">
        <Terminal className="w-4 h-4 text-hud-cyan" />
        <span className="font-mono text-xs text-gray-400 tracking-widest uppercase">Flujo de Telemetría RAW</span>
      </div>
      
      <div className="flex-1 overflow-y-auto space-y-2 pr-2 font-mono text-[11px] sm:text-xs">
        {logs.map((log) => (
          <motion.div 
            key={log.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex gap-3 hover:bg-white/5 p-1 rounded transition-colors group cursor-crosshair"
          >
            <span className="text-gray-600 w-24 shrink-0">[{log.time}]</span>
            <span className={getColor(log.type) + " w-20 shrink-0 uppercase opacity-80"}>
              {log.source}
            </span>
            <span className="text-gray-300 group-hover:text-white transition-colors">
              {log.message}
            </span>
          </motion.div>
        ))}
        {logs.length === 5 && (
          <motion.div 
            initial={{ opacity: 0 }} 
            animate={{ opacity: 1 }} 
            className="flex gap-3 p-1 animate-pulse mt-4"
          >
            <span className="text-gray-600 w-24 shrink-0">[{new Date().toISOString().split('T')[1].slice(0, 8)}]</span>
            <span className="text-hud-cyan w-20 shrink-0 uppercase opacity-80">SISTEMA</span>
            <span className="text-gray-400">Esperando directivas del CEO por Telegram...</span>
          </motion.div>
        )}
      </div>
    </div>
  );
}
