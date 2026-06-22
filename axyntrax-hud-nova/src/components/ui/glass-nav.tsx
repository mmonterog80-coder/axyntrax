'use client';

import { motion } from 'framer-motion';
import { ShieldAlert } from 'lucide-react';
import { cn } from '@/lib/utils';

export function GlassNav() {
  return (
    <motion.nav 
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ type: "spring", stiffness: 100, damping: 20 }}
      className="fixed w-full top-0 z-50 quantum-glass"
    >
      <div className="max-w-7xl mx-auto px-6 h-24 flex items-center justify-between">
        {/* Logo Section */}
        <div className="flex items-center gap-4 cursor-pointer group">
          <div className="w-10 h-10 neo-btn flex items-center justify-center group-hover:shadow-[0_0_15px_rgba(0,243,255,0.3)] transition-all duration-500">
            <div className="w-4 h-4 bg-cyan-l99 rounded-full shadow-[0_0_10px_#00f3ff] animate-pulse" />
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-black tracking-widest uppercase text-white font-mono flex items-center gap-1">
              Axyntrax<span className="text-cyan-l99 text-glow-cyan">.AI</span>
            </span>
            <span className="text-[0.6rem] text-zinc-500 tracking-[0.3em] uppercase">Omni-Core Node L99</span>
          </div>
        </div>

        {/* Links */}
        <div className="hidden lg:flex gap-10">
          {['Arquitectura', 'Telemetría', 'Neural Links', 'Protocolo'].map((item, i) => (
            <a 
              key={item} 
              href={`#${item.toLowerCase()}`}
              className="relative text-xs font-bold tracking-[0.2em] uppercase text-zinc-400 hover:text-cyan-l99 transition-colors group"
            >
              {item}
              <span className="absolute -bottom-2 left-0 w-0 h-[1px] bg-cyan-l99 transition-all group-hover:w-full shadow-[0_0_8px_#00f3ff]" />
            </a>
          ))}
        </div>

        {/* Status / CTA */}
        <div className="flex items-center gap-6">
          <div className="hidden md:flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-emerald-400" />
            <span className="text-xs font-mono text-emerald-400 tracking-widest">SYSTEM OPTIMAL</span>
          </div>
          <button className="neo-btn-cyan px-8 py-3 text-xs font-black tracking-widest uppercase hover:neo-btn-active active:scale-95 group flex items-center gap-3">
            <span>Iniciar Secuencia</span>
            <div className="w-2 h-2 rounded-full bg-cyan-l99 group-hover:shadow-[0_0_10px_#00f3ff] transition-all" />
          </button>
        </div>
      </div>
    </motion.nav>
  );
}
