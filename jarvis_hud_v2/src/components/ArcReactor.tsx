import React from 'react';
import { motion } from 'framer-motion';

export const ArcReactor: React.FC = () => {
  return (
    <div className="relative flex items-center justify-center w-64 h-64 md:w-80 md:h-80 mx-auto">
      {/* Outer Ring */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        className="absolute w-full h-full border-[3px] border-[#00e5ff] rounded-full shadow-[0_0_20px_#00e5ff,inset_0_0_20px_#00e5ff] opacity-80"
        style={{ borderStyle: 'dashed' }}
      />
      
      {/* Middle Ring 1 */}
      <motion.div
        animate={{ rotate: -360 }}
        transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
        className="absolute w-5/6 h-5/6 border-[4px] border-[#00aaff] rounded-full shadow-[0_0_15px_#00aaff] opacity-70"
        style={{ borderStyle: 'dotted' }}
      />

      {/* Middle Ring 2 */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
        className="absolute w-2/3 h-2/3 border-[2px] border-[#00ffff] rounded-full shadow-[0_0_25px_#00ffff,inset_0_0_15px_#00ffff]"
      />

      {/* Inner Core Rings */}
      <div className="absolute w-1/2 h-1/2 rounded-full border-[5px] border-[#ffffff] shadow-[0_0_30px_#ffffff,inset_0_0_20px_#ffffff] flex items-center justify-center opacity-90 overflow-hidden">
        <motion.div
          animate={{ scale: [1, 1.05, 1], opacity: [0.8, 1, 0.8] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
          className="w-full h-full rounded-full"
          style={{ background: 'radial-gradient(circle, #ffffff 10%, #00e5ff 60%, transparent 100%)' }}
        />
      </div>

      {/* Center Bright Spot */}
      <motion.div
        animate={{ scale: [0.9, 1.2, 0.9], opacity: [0.9, 1, 0.9] }}
        transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
        className="absolute w-1/4 h-1/4 bg-[#ffffff] rounded-full shadow-[0_0_40px_20px_#ffffff,0_0_80px_30px_#00e5ff]"
      />
      
      {/* Detail elements: Triangles or specific shapes */}
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          animate={{ rotate: 360 }}
          transition={{ duration: 12, repeat: Infinity, ease: "linear" }}
          className="absolute w-full h-full"
          style={{ transform: `rotate(${i * 120}deg)` }}
        >
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-2 h-4 bg-[#00ffff] shadow-[0_0_10px_#00ffff]" />
          <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-2 h-4 bg-[#00ffff] shadow-[0_0_10px_#00ffff]" />
        </motion.div>
      ))}
      
      {/* Radial lines */}
      {Array.from({ length: 12 }).map((_, i) => (
        <div 
          key={`radial-${i}`}
          className="absolute w-[80%] h-[2px] bg-[#00e5ff] opacity-40 shadow-[0_0_5px_#00e5ff]"
          style={{ transform: `rotate(${i * 30}deg)` }}
        />
      ))}
    </div>
  );
};

export default ArcReactor;
