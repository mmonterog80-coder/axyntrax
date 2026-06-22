const fs = require('fs');
const path = require('path');

const modules = [
  { id: 'agentic-automation', name: 'Agentic Automation', icon: 'Bot', desc: 'Robotic Process Automation orquestado por Enjambres de IA.', color: 'cyan' },
  { id: 'soc-sentinel', name: 'SOC Sentinel', icon: 'ShieldAlert', desc: 'Centro de Operaciones de Seguridad Cibernética Autónomo.', color: 'red' },
  { id: 'voice-cloning', name: 'Voice Cloning & Pitching', icon: 'Mic', desc: 'Clonación vocal neuronal para ventas B2B multilingüe.', color: 'purple' },
  { id: 'deepfake-defense', name: 'Deepfake Defense', icon: 'ScanFace', desc: 'Verificador forense contra fraudes de identidad sintética.', color: 'emerald' },
  { id: 'generative-3d', name: 'Generative 3D Weaver', icon: 'Box', desc: 'Conversión de texto a mallas 3D para comercio y Metaverso.', color: 'blue' },
  { id: 'video-lipsync', name: 'Video Lip-Sync', icon: 'Video', desc: 'Generación de avatares sintéticos hiperrealistas para marketing.', color: 'pink' },
  { id: 'legal-ai', name: 'Legal AI Drafter', icon: 'Scale', desc: 'Redacción y auditoría de contratos mediante LLMs legales.', color: 'amber' },
  { id: 'algo-trading', name: 'Algo-Trading Core', icon: 'TrendingUp', desc: 'Control de bots financieros de alta frecuencia (HFT).', color: 'green' },
  { id: 'telemed', name: 'Telemed Diagnostics', icon: 'Stethoscope', desc: 'Triaje médico asistido por visión computacional.', color: 'teal' },
  { id: 'smart-city', name: 'Smart City Grid', icon: 'Building2', desc: 'Optimización de tráfico y consumo energético municipal.', color: 'orange' },
  { id: 'agri-drone', name: 'Agri-Drone AI', icon: 'Tractor', desc: 'Rutas predictivas multiespectrales para agroexportadoras.', color: 'lime' },
  { id: 'genomics', name: 'Genomic Analyst', icon: 'Dna', desc: 'Panel predictivo de salud basado en secuenciación genética.', color: 'indigo' },
  { id: 'bci-neural', name: 'BCI Neural Interface', icon: 'Brain', desc: 'Visualizador de interfaces Cerebro-Computadora en tiempo real.', color: 'fuchsia' },
  { id: 'satellite', name: 'Satellite Tracker', icon: 'Satellite', desc: 'Rastreo de órbitas y activos logísticos nivel aeroespacial.', color: 'sky' },
  { id: 'metaverse-npc', name: 'Metaverse NPC Control', icon: 'Gamepad2', desc: 'Controlador de personalidades para avatares virtuales.', color: 'violet' },
  { id: 'real-estate', name: 'Real Estate Predictor', icon: 'Home', desc: 'Valuador predictivo de propiedades mediante IA satelital.', color: 'rose' },
  { id: 'music-composer', name: 'Soundtrack Composer', icon: 'Music', desc: 'Generador de bandas sonoras corporativas neuronales.', color: 'yellow' },
  { id: 'quantum-sim', name: 'Quantum Sim API', icon: 'Atom', desc: 'Simulador de optimización logística mediante circuitos cuánticos.', color: 'cyan' },
  { id: 'swarm-control', name: 'Swarm Control Dashboard', icon: 'Network', desc: 'Monitoreo absoluto de todos los agentes IA de la corporación.', color: 'red' },
  { id: 'no-code-ai', name: 'No-Code AI Builder', icon: 'Workflow', desc: 'Constructor visual Drag & Drop para flujos de IA.', color: 'blue' }
];

const basePath = path.join('C:', 'AXYNTRAX', 'axyntrax-hud-nova', 'src', 'app', 'modulos');

if (!fs.existsSync(basePath)) {
  fs.mkdirSync(basePath, { recursive: true });
}

// Generar Layout Maestro
const layoutContent = `
import { ReactNode } from 'react';
import Link from 'next/link';
import * as Icons from 'lucide-react';

export default function ModulosLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-[#050505] text-white font-sans flex flex-col">
      <header className="sticky top-0 z-50 bg-[#0A0A0A]/80 backdrop-blur-md border-b border-white/10 px-6 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <Link href="/hud" className="text-gray-400 hover:text-cyan-400 transition-colors">
            <Icons.ArrowLeft className="w-5 h-5" />
          </Link>
          <div className="flex items-center space-x-2">
            <Icons.Hexagon className="w-6 h-6 text-cyan-500 animate-pulse" />
            <span className="font-bold tracking-widest text-lg">AXYNTRAX <span className="text-cyan-500">GLOBAL</span></span>
          </div>
        </div>
        <div className="flex space-x-6 text-sm font-medium">
          <Link href="/modulos" className="text-cyan-400 hover:text-cyan-300">Hub Principal</Link>
          <span className="text-gray-600">|</span>
          <span className="text-green-400 flex items-center"><span className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span> Sistema Operativo</span>
        </div>
      </header>

      <main className="flex-1 overflow-hidden relative">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-cyan-900/20 via-[#050505] to-[#050505] pointer-events-none"></div>
        <div className="relative z-10 h-full overflow-y-auto p-6 md:p-12">
          {children}
        </div>
      </main>
    </div>
  );
}
`;
fs.writeFileSync(path.join(basePath, 'layout.tsx'), layoutContent);

// Generar Hub Page
const hubPageContent = `
"use client";
import { motion } from 'framer-motion';
import Link from 'next/link';
import * as Icons from 'lucide-react';

const modules = ${JSON.stringify(modules)};

export default function ModulosHub() {
  return (
    <div className="max-w-7xl mx-auto">
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-12"
      >
        <h1 className="text-4xl md:text-5xl font-black mb-4 tracking-tighter">
          VANGUARDIA <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-600">GLOBAL</span>
        </h1>
        <p className="text-gray-400 text-lg max-w-2xl border-l-2 border-cyan-500 pl-4">
          Acceso a los 20 Módulos de Inteligencia Artificial de Nivel Aeroespacial. Seleccione un subsistema para inicialización local.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {modules.map((mod, i) => {
          const Icon = (Icons as any)[mod.icon] || Icons.Box;
          return (
            <Link href={\`/modulos/\${mod.id}\`} key={mod.id}>
              <motion.div 
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
                className="group relative h-full bg-white/[0.02] border border-white/5 hover:border-cyan-500/50 rounded-2xl p-6 overflow-hidden hover:bg-white/[0.04] transition-all cursor-pointer"
              >
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                <div className="mb-4 inline-flex p-3 rounded-xl bg-white/5 group-hover:bg-cyan-500/20 group-hover:text-cyan-400 transition-colors text-gray-300">
                  <Icon className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-bold mb-2 group-hover:text-white transition-colors">{mod.name}</h3>
                <p className="text-sm text-gray-500 group-hover:text-gray-300 transition-colors">{mod.desc}</p>
                <div className="mt-6 flex items-center text-cyan-500 text-sm font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
                  <span>Acceder al Módulo</span>
                  <Icons.ChevronRight className="w-4 h-4 ml-1" />
                </div>
              </motion.div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
`;
fs.writeFileSync(path.join(basePath, 'page.tsx'), hubPageContent);

// Generar cada módulo
modules.forEach(mod => {
  const modPath = path.join(basePath, mod.id);
  if (!fs.existsSync(modPath)) fs.mkdirSync(modPath);

  const pageContent = `
"use client";
import { motion } from 'framer-motion';
import * as Icons from 'lucide-react';
import { useState } from 'react';

export default function ${mod.id.replace(/-./g, x=>x[1].toUpperCase())}Module() {
  const [active, setActive] = useState(false);
  const Icon = (Icons as any)['${mod.icon}'] || Icons.Box;

  return (
    <div className="max-w-5xl mx-auto h-full flex flex-col">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold flex items-center gap-3">
            <Icon className="text-${mod.color}-500 w-10 h-10" />
            { '${mod.name}' }
          </h1>
          <p className="text-gray-400 mt-2">{ '${mod.desc}' }</p>
        </div>
        <button 
          onClick={() => setActive(!active)}
          className={\`px-6 py-2 rounded-full font-bold uppercase tracking-wider text-sm transition-all \${active ? 'bg-red-500/20 text-red-400 border border-red-500' : 'bg-cyan-500 text-black hover:bg-cyan-400 shadow-[0_0_20px_rgba(6,182,212,0.4)]'}\`}
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
                  <p className="text-cyan-400">{'>'} Módulo ${mod.name} ONLINE.</p>
                </>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
`;
  fs.writeFileSync(path.join(modPath, 'page.tsx'), pageContent);
});

console.log("¡Los 20 módulos de lujo fueron generados con éxito!");
