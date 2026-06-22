'use client';

import { motion } from 'framer-motion';
import { ArrowRight, Terminal } from 'lucide-react';

export function HeroSection() {
  return (
    <div className="relative min-h-screen flex flex-col justify-center pt-20">
      
      {/* Decorative vertical line */}
      <motion.div 
        initial={{ scaleY: 0 }}
        animate={{ scaleY: 1 }}
        transition={{ duration: 1.5, ease: "circOut" }}
        className="absolute left-0 top-1/4 bottom-1/4 w-[1px] bg-gradient-to-b from-transparent via-cyan-l99/50 to-transparent origin-top hidden md:block"
      />

      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.9, type: 'spring', damping: 20 }}
        className="max-w-5xl relative z-10"
      >
        <div className="inline-flex items-center gap-3 px-4 py-2 bg-[#050505]/80 quantum-glass rounded-full text-[0.65rem] font-mono tracking-[0.2em] mb-10 text-cyan-l99 border border-cyan-l99/20 uppercase shadow-[0_0_20px_rgba(0,243,255,0.1)]">
          <span className="w-2 h-2 rounded-full bg-cyan-l99 animate-pulse shadow-[0_0_8px_#00f3ff]" />
          Axyntrax Protocol v15.0 Active
        </div>
        
        <h1 className="text-6xl md:text-8xl lg:text-9xl font-black tracking-tighter leading-[0.85] uppercase text-white mb-8">
          Diseño <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-zinc-100 via-zinc-500 to-[#020202]">
            Autónomo.
          </span>
        </h1>
        
        <p className="text-lg md:text-xl text-zinc-400 max-w-2xl font-light leading-relaxed tracking-wide mb-12">
          Orquestación absoluta de interfaces digitales. 
          Motor Neomórfico L99 sincronizado con DeepSeek V4. 
          Diseñado para dominar la web moderna con latencia cero.
        </p>

        <div className="flex flex-col sm:flex-row gap-6 items-center">
          <button className="w-full sm:w-auto neo-btn-cyan px-10 py-5 font-black uppercase tracking-[0.2em] flex items-center justify-center gap-3 transition-all hover:-translate-y-1 group text-sm">
            <span>Desplegar Hub</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-2 transition-transform text-cyan-l99" />
          </button>
          
          <button className="w-full sm:w-auto neo-btn px-10 py-5 font-bold uppercase tracking-[0.2em] flex items-center justify-center gap-3 text-zinc-400 hover:text-white transition-all hover:-translate-y-1 text-sm group">
            <Terminal className="w-5 h-5 group-hover:text-emerald-400 transition-colors" />
            <span>Terminal Core</span>
          </button>
        </div>

        {/* System metrics mini-display */}
        <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8 border-t border-white/5 pt-8">
          {[
            { label: 'Latency', value: '0.4ms' },
            { label: 'Uptime', value: '99.999%' },
            { label: 'Security', value: 'L99 Max' },
            { label: 'Bandwidth', value: 'Unlimited' }
          ].map((metric, i) => (
            <motion.div 
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 + (i * 0.1) }}
              className="flex flex-col gap-1"
            >
              <span className="text-[0.6rem] text-zinc-600 font-mono tracking-[0.2em] uppercase">{metric.label}</span>
              <span className="text-lg font-black text-zinc-200 tracking-wider">{metric.value}</span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
