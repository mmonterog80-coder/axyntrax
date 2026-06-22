'use client';

import { motion } from 'framer-motion';

export function GridOverlay() {
  return (
    <>
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 2 }}
        className="fixed inset-0 z-0 pointer-events-none hud-grid opacity-30" 
      />
      <div className="fixed inset-0 z-0 pointer-events-none bg-[radial-gradient(ellipse_at_center,_transparent_0%,_#050505_80%)]" />
    </>
  );
}
