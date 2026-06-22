
"use client";
import { motion } from 'framer-motion';
import Link from 'next/link';
import * as Icons from 'lucide-react';

const modules = [{"id":"agentic-automation","name":"Agentic Automation","icon":"Bot","desc":"Robotic Process Automation orquestado por Enjambres de IA.","color":"cyan"},{"id":"soc-sentinel","name":"SOC Sentinel","icon":"ShieldAlert","desc":"Centro de Operaciones de Seguridad Cibernética Autónomo.","color":"red"},{"id":"voice-cloning","name":"Voice Cloning & Pitching","icon":"Mic","desc":"Clonación vocal neuronal para ventas B2B multilingüe.","color":"purple"},{"id":"deepfake-defense","name":"Deepfake Defense","icon":"ScanFace","desc":"Verificador forense contra fraudes de identidad sintética.","color":"emerald"},{"id":"generative-3d","name":"Generative 3D Weaver","icon":"Box","desc":"Conversión de texto a mallas 3D para comercio y Metaverso.","color":"blue"},{"id":"video-lipsync","name":"Video Lip-Sync","icon":"Video","desc":"Generación de avatares sintéticos hiperrealistas para marketing.","color":"pink"},{"id":"legal-ai","name":"Legal AI Drafter","icon":"Scale","desc":"Redacción y auditoría de contratos mediante LLMs legales.","color":"amber"},{"id":"algo-trading","name":"Algo-Trading Core","icon":"TrendingUp","desc":"Control de bots financieros de alta frecuencia (HFT).","color":"green"},{"id":"telemed","name":"Telemed Diagnostics","icon":"Stethoscope","desc":"Triaje médico asistido por visión computacional.","color":"teal"},{"id":"smart-city","name":"Smart City Grid","icon":"Building2","desc":"Optimización de tráfico y consumo energético municipal.","color":"orange"},{"id":"agri-drone","name":"Agri-Drone AI","icon":"Tractor","desc":"Rutas predictivas multiespectrales para agroexportadoras.","color":"lime"},{"id":"genomics","name":"Genomic Analyst","icon":"Dna","desc":"Panel predictivo de salud basado en secuenciación genética.","color":"indigo"},{"id":"bci-neural","name":"BCI Neural Interface","icon":"Brain","desc":"Visualizador de interfaces Cerebro-Computadora en tiempo real.","color":"fuchsia"},{"id":"satellite","name":"Satellite Tracker","icon":"Satellite","desc":"Rastreo de órbitas y activos logísticos nivel aeroespacial.","color":"sky"},{"id":"metaverse-npc","name":"Metaverse NPC Control","icon":"Gamepad2","desc":"Controlador de personalidades para avatares virtuales.","color":"violet"},{"id":"real-estate","name":"Real Estate Predictor","icon":"Home","desc":"Valuador predictivo de propiedades mediante IA satelital.","color":"rose"},{"id":"music-composer","name":"Soundtrack Composer","icon":"Music","desc":"Generador de bandas sonoras corporativas neuronales.","color":"yellow"},{"id":"quantum-sim","name":"Quantum Sim API","icon":"Atom","desc":"Simulador de optimización logística mediante circuitos cuánticos.","color":"cyan"},{"id":"swarm-control","name":"Swarm Control Dashboard","icon":"Network","desc":"Monitoreo absoluto de todos los agentes IA de la corporación.","color":"red"},{"id":"no-code-ai","name":"No-Code AI Builder","icon":"Workflow","desc":"Constructor visual Drag & Drop para flujos de IA.","color":"blue"}];

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
            <Link href={`/modulos/${mod.id}`} key={mod.id}>
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
