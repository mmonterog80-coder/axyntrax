'use client';

import { useState, useEffect } from 'react';

export default function VisionDashboard() {
  const [systemState, setSystemState] = useState('VERIFICANDO ENLACES');
  
  useEffect(() => {
    // Simular conexi\u00f3n a Railway/Hetzner
    const bootSequence = async () => {
      setSystemState('INICIALIZANDO NEXO RAILWAY...');
      await new Promise(r => setTimeout(r, 1000));
      setSystemState('CONECTANDO A VISION CORE (HETZNER)...');
      await new Promise(r => setTimeout(r, 1000));
      setSystemState('SINCRONIZANDO OLLAMA 32B...');
      await new Promise(r => setTimeout(r, 1000));
      setSystemState('SISTEMA EN L\u00cdNEA - MODO S\u00d3LO LECTURA (L99)');
    };
    bootSequence();
  }, []);

  return (
    <div className="min-h-screen bg-[#050505] text-white font-sans overflow-hidden flex flex-col relative">
      {/* Background FX */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-cyan-900/20 via-black to-black z-0"></div>
      
      {/* Top Navigation */}
      <nav className="relative z-10 p-6 border-b border-cyan-500/20 bg-black/40 backdrop-blur-md flex justify-between items-center">
        <div className="flex items-center gap-4">
          <div className="w-3 h-3 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_15px_#22d3ee]"></div>
          <h1 className="text-xl tracking-widest font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
            AXYNTRAX <span className="font-light text-gray-400">| CLOUD HUD</span>
          </h1>
        </div>
        <div className="flex gap-4 text-xs font-mono text-cyan-500/70 tracking-widest">
          <div className="px-3 py-1 border border-cyan-500/30 rounded bg-cyan-950/30">NEXO: TELEGRAM</div>
          <div className="px-3 py-1 border border-cyan-500/30 rounded bg-cyan-950/30">CORE: DEEPSEEK</div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="relative z-10 flex-1 p-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Status Panel */}
        <div className="col-span-1 border border-white/5 rounded-2xl bg-white/5 backdrop-blur-xl p-6 shadow-2xl flex flex-col">
          <h2 className="text-sm tracking-widest text-gray-400 mb-6 border-b border-white/10 pb-2">ESTADO DE LA FLOTA</h2>
          
          <div className="space-y-4 flex-1">
            <StatusRow label="Omni-Core (Railway)" status="CONECTADO" color="text-emerald-400" />
            <StatusRow label="Vision Node (Hetzner)" status="OPERATIVO" color="text-emerald-400" />
            <StatusRow label="Base de Datos (Supabase)" status="SINCRONIZADO" color="text-emerald-400" />
            <StatusRow label="Cerebro Local (Qwen 32B)" status="EN ESPERA" color="text-cyan-400" />
          </div>

          <div className="mt-8 p-4 bg-black/50 rounded-xl border border-white/5">
            <p className="text-xs font-mono text-gray-500">ÚLTIMO REGISTRO SISTEMA</p>
            <p className="text-sm text-cyan-400 font-mono mt-2 animate-pulse">{systemState}</p>
          </div>
        </div>

        {/* Telemetry / Feed */}
        <div className="col-span-1 md:col-span-2 border border-white/5 rounded-2xl bg-white/5 backdrop-blur-xl p-6 shadow-2xl flex flex-col items-center justify-center relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent z-10 pointer-events-none"></div>
          
          {/* Radar Grid Simulation */}
          <div className="absolute inset-0 opacity-20 pointer-events-none" 
               style={{ backgroundImage: 'linear-gradient(#22d3ee 1px, transparent 1px), linear-gradient(90deg, #22d3ee 1px, transparent 1px)', backgroundSize: '40px 40px' }}>
          </div>
          
          <div className="z-20 text-center">
            <h3 className="text-2xl font-light text-white tracking-widest mb-2">TELEMETRÍA VISUAL <span className="text-cyan-500 font-bold">L99</span></h3>
            <p className="text-gray-400 text-sm">El panel interactivo ha sido deshabilitado. Todas las órdenes deben ingresar por Telegram.</p>
            
            <div className="mt-8 flex justify-center gap-4">
               <div className="w-16 h-16 border-2 border-dashed border-cyan-500/50 rounded-full animate-[spin_4s_linear_infinite] flex items-center justify-center">
                  <div className="w-8 h-8 bg-cyan-500/20 rounded-full"></div>
               </div>
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}

function StatusRow({ label, status, color }: { label: string, status: string, color: string }) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-white/5 last:border-0">
      <span className="text-sm text-gray-300 font-medium">{label}</span>
      <span className={`text-xs font-mono ${color} tracking-widest bg-white/5 px-2 py-1 rounded`}>{status}</span>
    </div>
  );
}
