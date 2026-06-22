
"use client";
import { motion } from 'framer-motion';
import * as Icons from 'lucide-react';
import { useState } from 'react';

export default function metaverseNpcModule() {
  const [active, setActive] = useState(false);
  const Icon = (Icons as any)['Gamepad2'] || Icons.Box;

  return (
    <div className="max-w-5xl mx-auto h-full flex flex-col">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold flex items-center gap-3">
            <Icon className="text-violet-500 w-10 h-10" />
            { 'Metaverse NPC Control' }
          </h1>
          <p className="text-gray-400 mt-2">{ 'Controlador de personalidades para avatares virtuales.' }</p>
        </div>
        <button 
          onClick={() => setActive(!active)}
          className={`px-6 py-2 rounded-full font-bold uppercase tracking-wider text-sm transition-all ${active ? 'bg-red-500/20 text-red-400 border border-red-500' : 'bg-cyan-500 text-black hover:bg-cyan-400 shadow-[0_0_20px_rgba(6,182,212,0.4)]'}`}
        >
          {active ? 'Desactivar Núcleo' : 'Inicializar Módulo'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
        {/* Panel Principal */}
        <motion.div 
          className="lg:col-span-2 bg-black/40 border border-white/10 rounded-2xl p-6 relative overflow-hidden backdrop-blur-xl"
          animate={{ borderColor: active ? '#06b6d4' : 'rgba(255,255,255,0.1)' }}
        >
          {active && <div className="absolute inset-0 bg-cyan-500/5 animate-pulse mix-blend-screen pointer-events-none"></div>}
          <div className="h-full flex flex-col items-center justify-center min-h-[300px]">
            {active ? (
              <div className="text-center">
                <div className="relative inline-block mb-6">
                  <div className="w-24 h-24 rounded-full border-t-2 border-cyan-500 animate-spin"></div>
                  <div className="absolute inset-0 w-24 h-24 rounded-full border-r-2 border-blue-500 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
                  <Icon className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-cyan-400 w-8 h-8" />
                </div>
                <h2 className="text-xl font-bold text-cyan-400 mb-2">Conectado a Enjambre Global</h2>
                <p className="text-gray-400 font-mono text-sm">Flujo de datos estabilizado. Procesamiento cuántico online.</p>
              </div>
            ) : (
              <div className="text-center text-gray-600">
                <Icons.Power className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p>Módulo inactivo. Esperando autorización de despliegue.</p>
              </div>
            )}
          </div>
        </motion.div>

        {/* Panel Lateral (Métricas) */}
        <div className="space-y-6">
          <motion.div className="bg-white/5 border border-white/10 rounded-2xl p-5 backdrop-blur-md">
            <h3 className="text-gray-400 text-sm font-semibold mb-4 uppercase flex items-center gap-2"><Icons.Activity className="w-4 h-4"/> Estado del Sistema</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-400">Carga Neural</span>
                  <span className="text-white">{active ? '84%' : '0%'}</span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-1.5 overflow-hidden">
                  <motion.div className="bg-cyan-500 h-full" initial={{width:0}} animate={{width: active ? '84%' : '0%'}} transition={{duration:1}} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-400">Sincronización</span>
                  <span className="text-white">{active ? '100%' : 'Desconectado'}</span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-1.5 overflow-hidden">
                  <motion.div className="bg-blue-500 h-full" initial={{width:0}} animate={{width: active ? '100%' : '0%'}} transition={{duration:1.5}} />
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div className="bg-white/5 border border-white/10 rounded-2xl p-5 backdrop-blur-md">
            <h3 className="text-gray-400 text-sm font-semibold mb-4 uppercase flex items-center gap-2"><Icons.Terminal className="w-4 h-4"/> Logs de Operación</h3>
            <div className="font-mono text-xs text-green-400/80 space-y-2 h-32 overflow-y-auto">
              <p>{'>'} Inicializando protocolo de seguridad...</p>
              <p>{'>'} Verificando nodos Axyntrax Perú...</p>
              {active && (
                <>
                  <p>{'>'} Bypass cuántico aceptado.</p>
                  <p>{'>'} Modelos hiperparamétricos cargados.</p>
                  <p className="text-cyan-400">{'>'} Módulo Metaverse NPC Control ONLINE.</p>
                </>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
