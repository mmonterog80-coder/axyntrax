'use client';

import { motion } from 'framer-motion';
import { ArrowRight, Brain, Shield, Zap } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function Home() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({
        x: e.clientX,
        y: e.clientY,
      });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div className="min-h-screen bg-[var(--background)] text-white selection:bg-[#00f0ff] selection:text-black font-sans overflow-hidden">
      {/* Dynamic Background */}
      <div 
        className="fixed inset-0 pointer-events-none opacity-20"
        style={{
          background: `radial-gradient(800px circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(0, 240, 255, 0.08), transparent 40%)`
        }}
      />
      
      {/* Grid Overlay */}
      <div className="fixed inset-0 pointer-events-none" style={{ backgroundImage: 'linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px)', backgroundSize: '50px 50px' }} />

      {/* Navigation */}
      <nav className="fixed w-full top-0 z-50 glass-nav">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg shadow-[inset_2px_2px_4px_#00f0ff,2px_2px_8px_#000] bg-[#121214] flex items-center justify-center border border-[#00f0ff]/30">
                <div className="w-4 h-4 bg-[#00f0ff] rounded-full blur-[2px]" />
            </div>
            <span className="text-xl font-black tracking-tighter uppercase">Axyntrax<span className="text-[#00f0ff] text-neon-cyan">.AI</span></span>
          </div>
          <div className="hidden md:flex gap-8 text-sm font-medium tracking-wide text-zinc-400">
            <a href="#technology" className="hover:text-white transition-colors uppercase hover:text-neon-cyan">Tecnología</a>
            <a href="#solutions" className="hover:text-white transition-colors uppercase hover:text-neon-cyan">Soluciones</a>
            <a href="#security" className="hover:text-white transition-colors uppercase hover:text-neon-cyan">Seguridad L99</a>
          </div>
          <button className="neo-button hover:neo-button-active text-[#00f0ff] px-6 py-2.5 text-sm font-bold uppercase transition-all cursor-pointer">
            Acceso Omni-Core
          </button>
        </div>
      </nav>

      <main className="pt-32 pb-16 px-6 relative z-10 max-w-7xl mx-auto">
        
        {/* HERO SECTION */}
        <div className="min-h-[80vh] flex flex-col justify-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded-full text-xs font-mono mb-8 text-[#00f0ff]">
              <span className="w-2 h-2 rounded-full bg-[#00f0ff] animate-pulse" />
              DEEPSEEK V4 EN LÍNEA
            </div>
            
            <h1 className="text-6xl md:text-8xl font-black tracking-tighter leading-[0.9] uppercase">
              La Evolución del <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-white via-zinc-400 to-zinc-800">Cerebro Digital.</span>
            </h1>
            
            <p className="mt-8 text-xl text-zinc-400 max-w-2xl font-light leading-relaxed">
              Orquestación autónoma impulsada por Inteligencia Artificial Multimodal. 
              Transforme su clínica o empresa en un ecosistema predictivo, seguro y brutalmente eficiente.
            </p>

            <div className="mt-12 flex flex-col sm:flex-row gap-6">
              <button className="neo-button hover:neo-button-active group text-[#00f0ff] px-8 py-4 font-bold uppercase flex items-center justify-center gap-2 transition-all cursor-pointer">
                Desplegar Arquitectura
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform text-[#00f0ff]" />
              </button>
              <button className="neo-button hover:neo-button-active px-8 py-4 font-bold uppercase flex items-center justify-center gap-2 transition-all text-zinc-300 cursor-pointer">
                Ver Telemetría
              </button>
            </div>
          </motion.div>
        </div>

        {/* NEOMORPHISM FEATURE CARDS */}
        <div id="technology" className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-32">
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="group relative neo-panel p-8 transition-all overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-32 h-32 bg-[#00f0ff]/5 blur-3xl group-hover:bg-[#00f0ff]/15 transition-colors" />
            <div className="w-16 h-16 neo-button flex items-center justify-center mb-6">
              <Brain className="w-8 h-8 text-[#00f0ff]" />
            </div>
            <h3 className="text-2xl font-black uppercase mb-4 text-white">DeepSeek Neural</h3>
            <p className="text-zinc-400 text-sm leading-relaxed">
              Clasificación de intenciones L99 en microsegundos. El núcleo V4 procesa audios, imágenes y texto sin latencia estructural.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="group relative neo-panel p-8 transition-all overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/5 blur-3xl group-hover:bg-amber-500/15 transition-colors" />
            <div className="w-16 h-16 neo-button flex items-center justify-center mb-6">
              <Zap className="w-8 h-8 text-amber-500" />
            </div>
            <h3 className="text-2xl font-black uppercase mb-4 text-white">Omni-Core Node</h3>
            <p className="text-zinc-400 text-sm leading-relaxed">
              Motor WebSocket asíncrono. Gestiona reservas, pagos y validación OCR en tiempo real.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="group relative glass-panel p-8 transition-all overflow-hidden border-[#00f0ff]/20"
          >
            <div className="absolute top-0 right-0 w-32 h-32 bg-[#00f0ff]/10 blur-3xl group-hover:bg-[#00f0ff]/20 transition-colors" />
            <div className="w-16 h-16 neo-button flex items-center justify-center mb-6 border-[#00f0ff]/30">
              <Shield className="w-8 h-8 text-[#00f0ff]" />
            </div>
            <h3 className="text-2xl font-black uppercase mb-4 text-white">Seguridad L99</h3>
            <p className="text-zinc-300 text-sm leading-relaxed">
              Protección nativa contra inyecciones SQL y evasión de prompts. Validadores fotográficos impenetrables.
            </p>
          </motion.div>

        </div>

      </main>

      <footer className="border-t border-white/10 bg-[#121214] mt-32">
        <div className="max-w-7xl mx-auto px-6 py-12 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded shadow-[inset_1px_1px_2px_#00f0ff] bg-[#121214] flex items-center justify-center">
                <div className="w-2 h-2 bg-[#00f0ff] rounded-full" />
            </div>
            <span className="text-lg font-black tracking-tighter uppercase">Axyntrax<span className="text-[#00f0ff]">.AI</span></span>
          </div>
          <div className="text-zinc-500 text-sm font-mono">
            &copy; {new Date().getFullYear()} AXYNTRAX CORPORATION. SISTEMA L99.
          </div>
        </div>
      </footer>
    </div>
  );
}
