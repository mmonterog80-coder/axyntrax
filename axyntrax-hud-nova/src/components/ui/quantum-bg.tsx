'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export function QuantumBackground() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      // Small easing for smooth follow
      requestAnimationFrame(() => {
        setMousePosition({
          x: e.clientX,
          y: e.clientY,
        });
      });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <>
      {/* Vantablack Base layer */}
      <div className="fixed inset-0 bg-[#020202] -z-50" />
      
      {/* Dynamic Cyan L99 Spotlight */}
      <motion.div 
        className="fixed inset-0 pointer-events-none -z-40"
        animate={{
          background: `radial-gradient(1000px circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(0, 243, 255, 0.05), transparent 40%)`
        }}
        transition={{ type: 'tween', ease: 'linear', duration: 0 }}
      />

      {/* Spatial Grid Overlay */}
      <div 
        className="fixed inset-0 pointer-events-none bg-grid-pattern -z-30 opacity-60" 
      />

      {/* Ambient Orbs */}
      <div className="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-cyan-l99/5 blur-[120px] pointer-events-none -z-30" />
      <div className="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-indigo-500/5 blur-[120px] pointer-events-none -z-30" />
    </>
  );
}
