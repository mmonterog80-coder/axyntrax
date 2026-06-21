import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
// import Services from './components/Services';
// import Portfolio from './components/Portfolio';
// import CalendarWidget from './components/CalendarWidget';
// import EmailInbox from './components/EmailInbox';

const ArcReactor = () => (
  <div className="relative flex items-center justify-center w-64 h-64 md:w-80 md:h-80">
    {/* Glow base */}
    <div className="absolute inset-0 rounded-full bg-[#00e5ff]/10 blur-3xl animate-pulse" />
    
    {/* Outer rotating dashed ring */}
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
      className="absolute w-full h-full border-[2px] border-[#00e5ff] rounded-full opacity-60"
      style={{ borderStyle: 'dashed', boxShadow: '0 0 20px #00e5ff, inset 0 0 20px #00e5ff' }}
    />
    
    {/* Inner fast rotating dotted ring */}
    <motion.div
      animate={{ rotate: -360 }}
      transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
      className="absolute w-5/6 h-5/6 border-[4px] border-[#00ffff] rounded-full opacity-80"
      style={{ borderStyle: 'dotted', boxShadow: '0 0 15px #00ffff' }}
    />

    {/* Solid glowing middle ring */}
    <motion.div
      animate={{ scale: [1, 1.02, 1] }}
      transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
      className="absolute w-2/3 h-2/3 border-[3px] border-white rounded-full shadow-[0_0_30px_#ffffff,inset_0_0_20px_#ffffff]"
    />

    {/* Inner core pulse */}
    <div className="absolute w-1/2 h-1/2 rounded-full border-[8px] border-[#00e5ff] shadow-[0_0_40px_#00e5ff,inset_0_0_40px_#00e5ff] flex items-center justify-center overflow-hidden">
      <motion.div
        animate={{ opacity: [0.7, 1, 0.7], scale: [0.9, 1.1, 0.9] }}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        className="w-full h-full rounded-full bg-[radial-gradient(circle,#ffffff_10%,#00ffff_50%,transparent_100%)]"
      />
    </div>

    {/* Central blinding light */}
    <motion.div
      animate={{ scale: [0.8, 1.2, 0.8], opacity: [0.8, 1, 0.8] }}
      transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
      className="absolute w-1/4 h-1/4 bg-white rounded-full shadow-[0_0_60px_30px_#ffffff,0_0_100px_40px_#00e5ff]"
    />

    {/* Triangles detail */}
    {[0, 1, 2].map((i) => (
      <motion.div
        key={i}
        animate={{ rotate: 360 }}
        transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
        className="absolute w-full h-full"
        style={{ transform: `rotate(${i * 120}deg)` }}
      >
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3 h-6 bg-[#00ffff] shadow-[0_0_15px_#00ffff]" style={{ clipPath: 'polygon(50% 100%, 0 0, 100% 0)' }} />
      </motion.div>
    ))}
  </div>
);

const Panel = ({ title, children, className = "" }: any) => (
  <motion.div 
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.8 }}
    className={`relative bg-[#000d14]/60 backdrop-blur-2xl border border-[#00e5ff]/40 p-5 flex flex-col shadow-[inset_0_0_30px_rgba(0,229,255,0.05),0_8px_32px_rgba(0,229,255,0.1)] hover:border-[#00e5ff]/80 hover:shadow-[0_0_30px_rgba(0,229,255,0.2)] transition-all duration-500 overflow-hidden group rounded-lg ${className}`}
  >
    {/* Futuristic Corners */}
    <div className="absolute top-0 left-0 w-8 h-8 border-t-[3px] border-l-[3px] border-[#00ffff] opacity-90 transition-all group-hover:w-12 group-hover:h-12 shadow-[0_0_10px_#00ffff]" />
    <div className="absolute top-0 right-0 w-8 h-8 border-t-[3px] border-r-[3px] border-[#00ffff] opacity-90 transition-all group-hover:w-12 group-hover:h-12 shadow-[0_0_10px_#00ffff]" />
    <div className="absolute bottom-0 left-0 w-8 h-8 border-b-[3px] border-l-[3px] border-[#00ffff] opacity-90 transition-all group-hover:w-12 group-hover:h-12 shadow-[0_0_10px_#00ffff]" />
    <div className="absolute bottom-0 right-0 w-8 h-8 border-b-[3px] border-r-[3px] border-[#00ffff] opacity-90 transition-all group-hover:w-12 group-hover:h-12 shadow-[0_0_10px_#00ffff]" />
    
    {/* Scanline */}
    <div className="absolute inset-0 bg-[linear-gradient(transparent_50%,rgba(0,229,255,0.03)_50%)] bg-[length:100%_4px] pointer-events-none" />

    {title && (
      <div className="mb-4 flex items-center justify-between border-b border-[#00e5ff]/30 pb-2 relative z-10">
        <h3 className="text-[#00ffff] font-mono text-[12px] md:text-[14px] font-black uppercase tracking-[0.3em] drop-shadow-[0_0_8px_rgba(0,229,255,1)]">{title}</h3>
        <motion.div 
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="w-16 h-[2px] bg-[#00ffff] shadow-[0_0_10px_#00ffff]" 
        />
      </div>
    )}
    <div className="flex-1 relative z-10">
      {children}
    </div>
  </motion.div>
);

const ProgressBar = ({ label, value }: { label: string, value: number }) => (
  <div className="mb-3">
    <div className="flex justify-between text-[10px] md:text-[11px] font-mono text-[#00e5ff] mb-1.5 uppercase tracking-widest font-bold">
      <span>{label}</span>
      <span className="drop-shadow-[0_0_5px_#00e5ff]">{value.toFixed(1)}%</span>
    </div>
    <div className="h-2 w-full bg-[#00e5ff]/10 rounded-full overflow-hidden border border-[#00e5ff]/20">
      <motion.div 
        initial={{ width: 0 }}
        animate={{ width: `${value}%` }}
        transition={{ duration: 1, ease: "easeOut" }}
        className="h-full bg-gradient-to-r from-[#00e5ff]/40 to-[#00ffff] relative shadow-[0_0_10px_#00ffff]"
      >
        <motion.div 
          animate={{ x: ["-100%", "200%"] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
          className="absolute top-0 bottom-0 w-8 bg-white/50 blur-[2px] skew-x-[-20deg]" 
        />
      </motion.div>
    </div>
  </div>
);

export default function App() {
  const [time, setTime] = useState(new Date());
  const [telemetry, setTelemetry] = useState<any>({
    server_stats: { cpu: 15, ram: 55, disk: 42, temp: 48 },
    active_agents: []
  });
  const [logs, setLogs] = useState<string[]>(['> KERNEL INIT', '> SECURE LINK PENDING...']);
  const [bars1, setBars1] = useState(Array.from({length: 20}, () => Math.random() * 100));

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    const animTimer = setInterval(() => {
      setBars1(prev => prev.map(v => Math.max(10, Math.min(100, v + (Math.random() * 40 - 20)))));
    }, 500);

    const connectWebSocket = () => {
      const ws = new WebSocket('ws://178.156.140.78:8080/ws/hud');
      ws.onopen = () => setLogs(prev => [...prev.slice(-9), `[${new Date().toLocaleTimeString()}] > WEBSOCKET LINK ESTABLISHED`]);
      ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.type === 'SWARM_TELEMETRY') setTelemetry(payload.data);
          else if (payload.type === 'NEW_COMMAND') setLogs(prev => [...prev.slice(-9), `[${new Date().toLocaleTimeString()}] > ${payload.data}`]);
        } catch (err) {}
      };
      ws.onclose = () => {
        setLogs(prev => [...prev.slice(-9), `[${new Date().toLocaleTimeString()}] > CONNECTION LOST. RECONNECTING...`]);
        setTimeout(connectWebSocket, 3000);
      };
      return ws;
    };

    const wsInstance = connectWebSocket();
    return () => { clearInterval(timer); clearInterval(animTimer); wsInstance.close(); };
  }, []);

  return (
    <div className="min-h-screen w-full bg-[#01060a] text-[#00e5ff] font-sans flex flex-col p-4 md:p-8 select-none relative overflow-y-auto overflow-x-hidden scrollbar-hide">
      
      {/* Deep Cyber Background */}
      <div className="fixed inset-0 z-0 pointer-events-none opacity-20 bg-[linear-gradient(rgba(0,229,255,0.15)_1px,transparent_1px),linear-gradient(90deg,rgba(0,229,255,0.15)_1px,transparent_1px)] bg-[size:50px_50px]" />
      <div className="fixed inset-0 z-0 bg-[radial-gradient(circle_at_center,transparent_0%,#01060a_100%)] pointer-events-none" />

      {/* Main Grid */}
      <div className="relative z-10 w-full flex flex-col lg:grid lg:grid-cols-12 lg:grid-rows-12 gap-6 min-h-screen">

        {/* TOP LEFT */}
        <div className="lg:col-span-3 lg:row-span-5 flex flex-col gap-6">
          <div className="flex justify-between items-center text-[11px] font-mono text-[#00ffff] font-black uppercase tracking-[0.4em] drop-shadow-[0_0_8px_#00ffff]">
            <span>STARK INDUSTRIES</span>
            <span>{time.getFullYear()}</span>
          </div>
          
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-[#00e5ff]/5 p-5 rounded-2xl border border-[#00e5ff]/30 backdrop-blur-xl shadow-[0_0_30px_rgba(0,229,255,0.1)] flex flex-col items-center justify-center"
          >
            <div className="text-5xl md:text-6xl font-light font-mono tracking-widest text-[#ffffff] drop-shadow-[0_0_20px_#00ffff]">
              {time.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' })}
              <span className="text-3xl ml-2 text-[#00ffff]/80 animate-pulse">{time.getSeconds().toString().padStart(2, '0')}</span>
            </div>
            <div className="text-[12px] font-mono font-black uppercase tracking-[0.6em] text-[#00ffff] mt-4 opacity-80">
              AXYNTRAX TIME
            </div>
          </motion.div>

          <Panel title="TELEMETRÍA GLOBAL">
            <div className="space-y-4 pt-2">
              <ProgressBar label="CARGA CPU CORE" value={telemetry.server_stats.cpu || 12} />
              <ProgressBar label="MEMORIA CUÁNTICA" value={telemetry.server_stats.ram || 45} />
              <ProgressBar label="ALMACENAMIENTO" value={telemetry.server_stats.disk || 30} />
            </div>
          </Panel>
        </div>

        {/* TOP CENTER: ARC REACTOR */}
        <div className="flex lg:col-span-6 lg:row-span-6 flex-col items-center justify-center relative">
          <motion.div 
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="text-3xl md:text-4xl font-mono font-black tracking-[1em] text-[#ffffff] drop-shadow-[0_0_20px_#00ffff] uppercase absolute top-0 text-center w-full"
          >
            AXYNTRAX HUD
          </motion.div>
          
          <div className="mt-16 mb-8 transform scale-[0.8] md:scale-100 transition-transform">
            <ArcReactor />
          </div>
        </div>

        {/* TOP RIGHT */}
        <div className="lg:col-span-3 lg:row-span-5 flex flex-col gap-6">
          <div className="flex justify-end items-center text-[11px] font-mono text-[#00ffff] font-black uppercase tracking-[0.4em] drop-shadow-[0_0_8px_#00ffff]">
            <span>J.A.R.V.I.S. MK-VII</span>
          </div>

          <Panel title="FRECUENCIA NEURAL" className="h-[180px]">
            <div className="flex items-end justify-between h-full gap-1.5 mt-2">
              {bars1.map((val, i) => (
                <div key={i} className="flex-1 bg-[#00e5ff]/10 relative group h-full rounded-t-sm overflow-hidden">
                  <motion.div 
                    animate={{ height: `${val}%` }}
                    transition={{ type: "spring", stiffness: 300, damping: 20 }}
                    className="absolute bottom-0 w-full bg-gradient-to-t from-[#00e5ff] to-[#00ffff] rounded-t-sm shadow-[0_0_8px_#00ffff]" 
                  />
                </div>
              ))}
            </div>
            <div className="flex justify-between text-[9px] font-bold text-[#00ffff]/70 font-mono mt-3 border-t border-[#00e5ff]/30 pt-2 tracking-widest">
              <span>0Hz</span><span>1GHz</span><span>2GHz</span><span>MAX</span>
            </div>
          </Panel>

          <Panel title="SISTEMA AMBIENTAL">
            <div className="flex justify-between items-center h-full text-[#ffffff] font-mono px-2 py-4">
              <div className="text-center">
                <div className="text-[10px] font-black text-[#00ffff] mb-2 tracking-[0.2em]">NÚCLEO</div>
                <div className="text-4xl font-light drop-shadow-[0_0_15px_#00ffff]">{telemetry.server_stats.temp || 45}<span className="text-xl ml-1">°C</span></div>
              </div>
              <div className="text-center border-l border-r border-[#00e5ff]/30 px-6">
                <div className="text-[10px] font-black text-[#00ffff] mb-2 tracking-[0.2em]">ESTADO</div>
                <div className="text-xl font-bold text-[#10b981] drop-shadow-[0_0_15px_#10b981] animate-pulse">ÓPTIMO</div>
              </div>
              <div className="text-center">
                <div className="text-[10px] font-black text-[#00ffff] mb-2 tracking-[0.2em]">ENERGÍA</div>
                <div className="text-4xl font-light drop-shadow-[0_0_15px_#00ffff]">98<span className="text-xl ml-1">%</span></div>
              </div>
            </div>
          </Panel>
        </div>

        {/* BOTTOM LEFT */}
        <div className="lg:col-span-3 lg:row-span-7 flex flex-col gap-6">
          <Panel title="RED NEURAL (CHROMADB)" className="flex-1">
             <div className="space-y-5 pt-4">
              <ProgressBar label="CORTEX NLP" value={Math.min(100, (telemetry.server_stats.ram * 1.5) || 75)} />
              <ProgressBar label="SINAPSIS" value={92.4} />
              <ProgressBar label="VECTORES" value={100} />
            </div>
          </Panel>
        </div>

        {/* BOTTOM CENTER: TERMINAL LOGS */}
        <div className="lg:col-span-6 lg:row-span-6 flex flex-col">
          <Panel title="TERMINAL KERNEL JARVIS" className="flex-1">
            <div className="h-full flex flex-col justify-end gap-2 font-mono text-[10px] md:text-[12px] font-bold text-[#00ffff] overflow-y-auto scrollbar-hide p-2">
              {logs.map((log, i) => (
                <motion.div 
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  key={i} 
                  className="whitespace-pre-wrap break-words border-l-2 border-[#00ffff]/80 pl-3 py-1 bg-[#00ffff]/5"
                >
                  <span className="text-white drop-shadow-[0_0_5px_#ffffff] mr-3">[{time.toISOString().split('T')[1].slice(0,8)}]</span>
                  <span className="drop-shadow-[0_0_5px_#00ffff]">{log}</span>
                </motion.div>
              ))}
            </div>
          </Panel>
        </div>

        {/* BOTTOM RIGHT */}
        <div className="lg:col-span-3 lg:row-span-7 flex flex-col gap-6">
          <Panel title="AXYNTRAX SWARM ROSTER" className="flex-1">
            <div className="flex flex-col gap-3 overflow-y-auto h-full pr-2 scrollbar-hide">
              {telemetry.active_agents && telemetry.active_agents.length > 0 ? telemetry.active_agents.map((ia: any, index: number) => {
                return (
                  <div key={index} className="border border-[#00ffff]/30 bg-[#00ffff]/10 p-3 rounded-md">
                    <div className="flex justify-between items-center text-[12px] font-mono font-black text-white drop-shadow-[0_0_8px_#00ffff]">
                      <span className="uppercase">{ia.nombre}</span>
                      <span className="text-[#10b981] animate-pulse drop-shadow-[0_0_5px_#10b981]">{ia.status}</span>
                    </div>
                    <div className="text-[10px] font-mono font-bold text-[#00ffff] mt-2 truncate">
                      {ia.task ? `> Ejecutando: ${ia.task}` : '> WAITING FOR PROTOCOL'}
                    </div>
                  </div>
                )
              }) : (
                ['JARVIS', 'MERCURY', 'STITCH', 'GHOST', 'FRIDAY'].map((name, idx) => (
                  <motion.div 
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    key={idx} 
                    className="border border-[#00ffff]/30 bg-[#00ffff]/5 p-3 rounded-md hover:bg-[#00ffff]/20 transition-all cursor-crosshair group"
                  >
                    <div className="flex justify-between items-center text-[12px] font-mono font-black text-white drop-shadow-[0_0_8px_#00ffff]">
                      <span className="uppercase">{name}</span>
                      <span className="text-[#10b981] drop-shadow-[0_0_5px_#10b981] group-hover:animate-pulse">ONLINE</span>
                    </div>
                    <div className="text-[10px] font-mono font-bold text-[#00ffff]/80 mt-2">
                      {'> CONECTADO A LA MATRIZ'}
                    </div>
                  </motion.div>
                ))
              )}
            </div>
          </Panel>
        </div>

      </div>

      {/* BOTTOM WIDGETS (DESACTIVADOS TEMPORALMENTE PARA ESTABILIDAD) */}
      <div className="mt-8 grid grid-cols-1 xl:grid-cols-2 gap-8 z-10 relative">
        {/* <Services />
        <Portfolio />
        <CalendarWidget />
        <EmailInbox /> */}
      </div>

    </div>
  );
}
