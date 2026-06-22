'use client';

import { motion } from 'framer-motion';
import { ReactNode } from 'react';

interface NeoCardProps {
  title: string;
  description: string;
  icon: ReactNode;
  index: number;
  highlightColor?: string;
}

export function NeoCard({ title, description, icon, index, highlightColor = '#00f3ff' }: NeoCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ 
        duration: 0.7, 
        delay: index * 0.15,
        type: 'spring',
        damping: 25,
        stiffness: 120
      }}
      className="group relative neo-card p-10 overflow-hidden flex flex-col justify-between min-h-[320px] transition-all duration-500 hover:-translate-y-2 cursor-crosshair"
    >
      {/* Background glow injected from prop */}
      <div 
        className="absolute -top-16 -right-16 w-48 h-48 rounded-full blur-[80px] opacity-10 group-hover:opacity-30 transition-opacity duration-700"
        style={{ backgroundColor: highlightColor }} 
      />

      <div>
        <div className="w-16 h-16 neo-btn rounded-2xl flex items-center justify-center mb-8 relative [&>svg]:w-8 [&>svg]:h-8 [&>svg]:transition-transform [&>svg]:duration-500 group-hover:[&>svg]:scale-110" style={{ color: highlightColor }}>
          {icon}
          <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" style={{ boxShadow: `0 0 15px ${highlightColor}40` }} />
        </div>
        
        <h3 className="text-2xl font-black uppercase tracking-wider mb-4 text-white font-mono">{title}</h3>
        <p className="text-zinc-400 text-sm leading-relaxed tracking-wide">
          {description}
        </p>
      </div>

      <div className="mt-8 flex items-center justify-between border-t border-white/5 pt-4">
        <span className="text-[0.65rem] font-mono tracking-[0.3em] uppercase text-zinc-600">
          Module_0{index + 1}
        </span>
        <div className="w-2 h-2 rounded-full opacity-50 group-hover:opacity-100 animate-pulse" style={{ backgroundColor: highlightColor }} />
      </div>
    </motion.div>
  );
}
