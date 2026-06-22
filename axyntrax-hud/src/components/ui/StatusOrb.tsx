'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface StatusOrbProps {
  status: 'ONLINE' | 'OFFLINE' | 'WARNING' | 'SYNCING';
  className?: string;
}

export function StatusOrb({ status, className }: StatusOrbProps) {
  const getOrbColor = () => {
    switch (status) {
      case 'ONLINE': return 'bg-emerald-400 shadow-[0_0_10px_#10b981]';
      case 'OFFLINE': return 'bg-red-500 shadow-[0_0_10px_#ef4444]';
      case 'WARNING': return 'bg-amber-400 shadow-[0_0_10px_#fbbf24]';
      case 'SYNCING': return 'bg-cyan-400 shadow-[0_0_10px_#22d3ee]';
    }
  };

  const getPulseColor = () => {
    switch (status) {
      case 'ONLINE': return 'bg-emerald-400/40';
      case 'OFFLINE': return 'bg-red-500/40';
      case 'WARNING': return 'bg-amber-400/40';
      case 'SYNCING': return 'bg-cyan-400/40';
    }
  };

  return (
    <div className={cn("relative flex items-center justify-center w-3 h-3", className)}>
      {status !== 'OFFLINE' && (
        <motion.div
          className={cn("absolute inset-0 rounded-full", getPulseColor())}
          animate={{ scale: [1, 2], opacity: [0.8, 0] }}
          transition={{ duration: status === 'SYNCING' ? 1 : 2, repeat: Infinity, ease: "easeOut" }}
        />
      )}
      <div className={cn("relative w-2 h-2 rounded-full z-10", getOrbColor())} />
    </div>
  );
}
