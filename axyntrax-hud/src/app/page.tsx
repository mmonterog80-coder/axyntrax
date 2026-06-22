'use client';

import { GlassPanel } from '@/components/ui/GlassPanel';
import { StatusOrb } from '@/components/ui/StatusOrb';
import { GridOverlay } from '@/components/hud/GridOverlay';
import { TelemetryLog } from '@/components/hud/TelemetryLog';
import { Activity, BrainCircuit, ShieldAlert, Cpu, Server, Fingerprint } from 'lucide-react';
import { motion } from 'framer-motion';

export default function L99Dashboard() {
  return (
    <main className="min-h-screen relative overflow-hidden flex flex-col p-4 sm:p-8">
      <GridOverlay />
      
      {/* Top Navbar */}
      <motion.nav 
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="relative z-10 flex flex-col sm:flex-row justify-between items-center mb-8 border-b border-white/10 pb-6 gap-4"
      >
        <div className="flex items-center gap-4">
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-black border border-white/10 overflow-hidden group cursor-pointer">
            <div className="absolute inset-0 bg-hud-cyan/10 group-hover:bg-hud-cyan/20 transition-colors" />
            <BrainCircuit className="text-hud-cyan w-5 h-5 group-hover:scale-110 transition-transform" />
          </div>
          <div>
            <h1 className="text-2xl font-semibold tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-500">
              AXYNTRAX <span className="font-light text-hud-cyan neon-text-cyan">OMNI-CORE</span>
            </h1>
            <p className="font-mono text-[10px] text-gray-500 tracking-[0.2em] uppercase mt-1">
              Singularity Architecture v1.0
            </p>
          </div>
        </div>

        <div className="flex gap-6 items-center">
          <div className="flex flex-col items-end">
            <span className="font-mono text-xs text-hud-cyan uppercase tracking-widest mb-1">Nexo Activo</span>
            <span className="font-mono text-sm text-white bg-white/5 px-3 py-1 rounded border border-white/10">TELEGRAM</span>
          </div>
          <div className="h-8 w-px bg-white/10" />
          <div className="flex items-center gap-3">
            <span className="font-mono text-xs text-gray-400 uppercase tracking-widest">Estado</span>
            <StatusOrb status="SYNCING" />
          </div>
        </div>
      </motion.nav>

      {/* Main Grid */}
      <div className="relative z-10 flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-[1800px] mx-auto w-full">
        
        {/* Left Column: Systems */}
        <div className="col-span-1 lg:col-span-3 flex flex-col gap-6">
          <GlassPanel delay={0.2} className="p-6">
            <h2 className="font-mono text-xs text-gray-500 uppercase tracking-widest mb-6 flex items-center gap-2">
              <Server className="w-4 h-4" /> Nodos de Infraestructura
            </h2>
            <div className="space-y-6">
              <NodeItem name="Railway API (JARVIS)" ip="10.0.4.12" status="ONLINE" />
              <NodeItem name="Hetzner Node (Vision)" ip="45.132.89.21" status="ONLINE" />
              <NodeItem name="Supabase DB (Core)" ip="db.axyntrax.net" status="ONLINE" />
              <NodeItem name="Vercel Edge (HUD)" ip="edge.axyntrax.net" status="SYNCING" />
            </div>
          </GlassPanel>

          <GlassPanel delay={0.3} className="p-6 flex-1">
            <h2 className="font-mono text-xs text-gray-500 uppercase tracking-widest mb-6 flex items-center gap-2">
              <Cpu className="w-4 h-4" /> Cerebro Dual Activo
            </h2>
            <div className="flex flex-col gap-4">
              <div className="p-4 rounded-xl border border-hud-cyan/30 bg-hud-cyan/5">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-mono text-sm text-hud-cyan font-bold">DEEPSEEK V3</span>
                  <StatusOrb status="ONLINE" />
                </div>
                <p className="text-xs text-gray-400">Orquestador Lógico Principal. Carga: 12%</p>
              </div>
              <div className="p-4 rounded-xl border border-white/10 bg-white/5">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-mono text-sm text-gray-300 font-bold">QWEN 32B (LOCAL)</span>
                  <StatusOrb status="WARNING" />
                </div>
                <p className="text-xs text-gray-500">Asesor de Personal. En espera (Standby).</p>
              </div>
            </div>
          </GlassPanel>
        </div>

        {/* Center Column: Vision / Main Data */}
        <div className="col-span-1 lg:col-span-6 flex flex-col gap-6">
          <GlassPanel delay={0.4} className="p-1 flex-1 min-h-[400px] flex flex-col relative group">
            {/* Corner brackets */}
            <div className="absolute top-4 left-4 w-4 h-4 border-t border-l border-hud-cyan/50 rounded-tl" />
            <div className="absolute top-4 right-4 w-4 h-4 border-t border-r border-hud-cyan/50 rounded-tr" />
            <div className="absolute bottom-4 left-4 w-4 h-4 border-b border-l border-hud-cyan/50 rounded-bl" />
            <div className="absolute bottom-4 right-4 w-4 h-4 border-b border-r border-hud-cyan/50 rounded-br" />
            
            <div className="flex-1 bg-black/60 rounded-xl m-1 flex flex-col items-center justify-center relative overflow-hidden">
               <Activity className="w-16 h-16 text-hud-cyan/20 animate-pulse mb-4" />
               <h3 className="font-sans text-xl font-light text-white tracking-widest mb-2">CANVAS DE VISIÓN L99</h3>
               <p className="text-gray-500 text-sm font-mono tracking-wider">ESPERANDO STREAM RT-DETR (HETZNER)</p>
               <div className="mt-8 flex gap-2 items-center text-xs text-hud-cyan font-mono bg-hud-cyan/10 px-4 py-2 rounded-full border border-hud-cyan/20">
                 <div className="w-2 h-2 bg-hud-cyan rounded-full animate-ping" />
                 MODO DE LECTURA ACTIVO
               </div>
            </div>
          </GlassPanel>
        </div>

        {/* Right Column: Telemetry & Security */}
        <div className="col-span-1 lg:col-span-3 flex flex-col gap-6">
          <GlassPanel delay={0.5} className="p-6">
            <h2 className="font-mono text-xs text-gray-500 uppercase tracking-widest mb-6 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4" /> Matriz de Seguridad
            </h2>
            <div className="flex justify-between items-center bg-white/5 p-3 rounded-lg border border-emerald-500/20">
              <span className="text-sm text-gray-300 flex items-center gap-2">
                <Fingerprint className="w-4 h-4 text-emerald-400" /> Webhook Cifrado
              </span>
              <span className="font-mono text-xs text-emerald-400">ACTIVO</span>
            </div>
            <div className="flex justify-between items-center bg-white/5 p-3 rounded-lg border border-white/5 mt-3">
              <span className="text-sm text-gray-500">API Externa UI</span>
              <span className="font-mono text-xs text-gray-600 line-through">DENEGADO</span>
            </div>
          </GlassPanel>

          <GlassPanel delay={0.6} className="p-6 flex-1 min-h-[300px]">
            <TelemetryLog />
          </GlassPanel>
        </div>

      </div>
    </main>
  );
}

function NodeItem({ name, ip, status }: { name: string, ip: string, status: 'ONLINE' | 'OFFLINE' | 'SYNCING' }) {
  return (
    <div className="flex justify-between items-center group">
      <div>
        <p className="text-sm text-gray-200 group-hover:text-white transition-colors">{name}</p>
        <p className="font-mono text-[10px] text-gray-500 mt-1">{ip}</p>
      </div>
      <StatusOrb status={status} />
    </div>
  );
}
