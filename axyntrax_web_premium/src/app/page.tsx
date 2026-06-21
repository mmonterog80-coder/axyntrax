"use client";
import { motion, useScroll, useTransform } from "framer-motion";
import { useEffect, useState, useRef } from "react";

export default function Home() {
  const [mounted, setMounted] = useState(false);
  const { scrollYProgress } = useScroll();
  const yBg = useTransform(scrollYProgress, [0, 1], ["0%", "50%"]);
  const opacityText = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <main className="relative min-h-screen bg-[#01060a] text-[#ffffff] font-sans overflow-x-hidden selection:bg-[#00e5ff]/30">
      
      {/* GLOBAL BACKGROUND ELEMENTS */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(0,229,255,0.05)_0%,#01060a_100%)]" />
        <div className="absolute inset-0 opacity-20 bg-[linear-gradient(rgba(0,229,255,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(0,229,255,0.1)_1px,transparent_1px)] bg-[size:60px_60px]" style={{ filter: "drop-shadow(0 0 10px #00e5ff)" }} />
      </div>

      {/* FLOATING PARTICLES */}
      <div className="fixed inset-0 z-[1] pointer-events-none overflow-hidden">
        {Array.from({ length: 40 }).map((_, i) => (
          <motion.div
            key={`particle-${i}`}
            initial={{ y: "110vh", x: `${Math.random() * 100}vw`, scale: Math.random() * 0.5 + 0.5, opacity: 0 }}
            animate={{ y: "-10vh", opacity: [0, 0.8, 0], x: `${(Math.random() * 100)}vw` }}
            transition={{ duration: Math.random() * 8 + 7, repeat: Infinity, ease: "linear", delay: Math.random() * 10 }}
            className="absolute w-2 h-2 rounded-full bg-[#00e5ff] shadow-[0_0_15px_#00ffff]"
          />
        ))}
      </div>

      {/* HERO SECTION */}
      <section className="relative z-10 min-h-screen flex flex-col items-center justify-center px-6 pt-20">
        <motion.div style={{ y: yBg, opacity: opacityText }} className="flex flex-col items-center justify-center w-full">
          
          {/* EPIC 3D HOLOGRAPHIC LOGO ANIMATION */}
          <div className="relative w-[300px] h-[300px] md:w-[500px] md:h-[500px] flex items-center justify-center mb-16 perspective-[2000px]">
            {/* Outer Rings */}
            <motion.div 
              animate={{ rotateZ: 360, rotateX: 20 }}
              transition={{ duration: 40, repeat: Infinity, ease: "linear" }}
              className="absolute inset-0 border-[3px] border-dashed border-[#00e5ff] rounded-full opacity-30 drop-shadow-[0_0_15px_#00e5ff]"
            />
            <motion.div 
              animate={{ rotateZ: -360, rotateY: 20 }}
              transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
              className="absolute inset-[30px] md:inset-[50px] border-[4px] border-dotted border-[#00ffff] rounded-full opacity-60 drop-shadow-[0_0_20px_#00ffff]"
            />
            
            {/* Core Glow */}
            <motion.div 
              animate={{ scale: [1, 1.1, 1], opacity: [0.6, 1, 0.6] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
              className="absolute inset-[60px] md:inset-[100px] bg-gradient-to-tr from-[#00e5ff]/20 to-[#00ffff]/40 rounded-full blur-[40px]"
            />

            {/* Central 3D Text */}
            <motion.div
              initial={{ scale: 0.5, opacity: 0, rotateY: 90 }}
              animate={{ scale: 1, opacity: 1, rotateY: 0 }}
              transition={{ duration: 2, type: "spring", bounce: 0.5 }}
              className="relative z-10"
            >
              <h1 className="text-8xl md:text-[160px] font-black uppercase tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white via-[#00ffff] to-[#004455] drop-shadow-[0_0_40px_rgba(0,229,255,0.8)]" style={{ fontFamily: "'Montserrat', sans-serif", WebkitTextStroke: "2px rgba(0,229,255,0.5)" }}>
                AXY
              </h1>
            </motion.div>
          </div>

          {/* MAIN HEADLINE */}
          <motion.div
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 1, duration: 1 }}
            className="text-center max-w-5xl relative"
          >
            <h2 className="text-4xl md:text-7xl font-black uppercase tracking-widest mb-6 text-white drop-shadow-[0_0_15px_#00e5ff]">
              Corporación <span className="text-[#00ffff]">Axyntrax</span>
            </h2>
            <div className="w-full h-[2px] bg-gradient-to-r from-transparent via-[#00ffff] to-transparent mb-8 shadow-[0_0_15px_#00ffff]" />
            <p className="text-lg md:text-2xl font-mono text-[#00e5ff]/90 mb-12 max-w-3xl mx-auto leading-relaxed">
              Forjando el futuro a través de Inteligencia Artificial Autónoma.
              Infraestructura Cuántica. Protocolo MARK VII en línea.
            </p>

            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
              <motion.button
                whileHover={{ scale: 1.05, boxShadow: "0 0 40px rgba(0,255,255,0.6)" }}
                whileTap={{ scale: 0.95 }}
                className="px-12 py-5 bg-[#00ffff]/10 border-[3px] border-[#00ffff] text-[#00ffff] font-mono font-black uppercase tracking-[0.3em] rounded-sm transition-all hover:bg-[#00ffff]/20 relative overflow-hidden group"
              >
                <div className="absolute inset-0 bg-[linear-gradient(45deg,transparent_25%,rgba(255,255,255,0.2)_50%,transparent_75%)] w-[300%] -translate-x-[100%] group-hover:animate-[shimmer_1.5s_infinite]" />
                Ingresar al HUB
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-12 py-5 text-[#ffffff] font-mono font-bold uppercase tracking-[0.2em] relative group"
              >
                <span className="relative z-10 group-hover:drop-shadow-[0_0_10px_#ffffff]">Ver Protocolos</span>
                <div className="absolute bottom-0 left-0 w-0 h-[2px] bg-white group-hover:w-full transition-all duration-300 shadow-[0_0_10px_#ffffff]" />
              </motion.button>
            </div>
          </motion.div>
        </motion.div>

        {/* SCROLL DOWN INDICATOR */}
        <motion.div 
          animate={{ y: [0, 15, 0], opacity: [0.3, 1, 0.3] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center"
        >
          <span className="text-[10px] font-mono font-bold uppercase tracking-[0.3em] text-[#00ffff] mb-4">INICIAR CONEXIÓN</span>
          <div className="w-[2px] h-16 bg-gradient-to-b from-[#00ffff] to-transparent shadow-[0_0_10px_#00ffff]" />
        </motion.div>
      </section>

      {/* CORE FEATURES SECTION */}
      <section className="relative z-10 min-h-screen py-32 px-6 bg-[#000408]">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h3 className="text-3xl md:text-5xl font-black uppercase tracking-widest text-white drop-shadow-[0_0_15px_#00ffff] mb-4">Sistemas Integrados</h3>
            <div className="w-24 h-1 bg-[#00ffff] mx-auto shadow-[0_0_15px_#00ffff]" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { title: "MATRIZ NEURAL", desc: "Orquestador IA Central con procesamiento cognitivo distribuido.", delay: 0 },
              { title: "SEGURIDAD QUÁNTICA", desc: "Encriptación de grado militar para la protección total de datos corporativos.", delay: 0.2 },
              { title: "TELEMETRÍA GLOBAL", desc: "Vigilancia algorítmica en tiempo real del enjambre de sub-agentes.", delay: 0.4 }
            ].map((feature, idx) => (
              <motion.div 
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: feature.delay }}
                key={idx}
                className="bg-[#001420]/50 backdrop-blur-lg border border-[#00e5ff]/30 p-10 rounded-xl relative overflow-hidden group hover:border-[#00ffff] transition-colors duration-500 hover:shadow-[0_0_40px_rgba(0,255,255,0.15)] cursor-pointer"
              >
                {/* Tech Corners */}
                <div className="absolute top-0 left-0 w-8 h-8 border-t-[3px] border-l-[3px] border-[#00ffff] opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="absolute bottom-0 right-0 w-8 h-8 border-b-[3px] border-r-[3px] border-[#00ffff] opacity-0 group-hover:opacity-100 transition-opacity" />
                
                <h4 className="text-2xl font-black font-mono uppercase text-[#00ffff] mb-6 tracking-wider">{feature.title}</h4>
                <p className="text-[#a0d8e0] font-sans text-lg leading-relaxed">{feature.desc}</p>
                <div className="mt-8 text-sm font-mono font-bold text-white/50 group-hover:text-[#00ffff] transition-colors uppercase tracking-widest">
                  {`> Acceder_Modulo_0${idx+1}`}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CUSTOM ANIMATIONS */}
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes shimmer {
          100% { transform: translateX(100%); }
        }
      `}} />
    </main>
  );
}
