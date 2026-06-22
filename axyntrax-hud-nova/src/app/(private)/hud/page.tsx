"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import { Activity, Database, Mail, MessageSquare, Terminal, Cpu } from "lucide-react";

export default function HudPage() {
  const [models, setModels] = useState<any[]>([]);
  const [ollamaStatus, setOllamaStatus] = useState<"connecting" | "online" | "offline">("connecting");
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const fetchOllama = async () => {
      try {
        const res = await fetch("http://localhost:11434/api/tags");
        if (res.ok) {
          const data = await res.json();
          setModels(data.models || []);
          setOllamaStatus("online");
        } else {
          setOllamaStatus("offline");
        }
      } catch (err) {
        setOllamaStatus("offline");
      }
    };
    fetchOllama();
    const interval = setInterval(fetchOllama, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 h-full flex flex-col">
      {/* Top Bar */}
      <header className="flex justify-between items-center border-b border-cyan-500/30 pb-4 mb-6">
        <div className="flex items-center gap-4">
          <motion.div 
            animate={{ rotate: 360 }}
            transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
            className="w-10 h-10 border-2 border-cyan-500 rounded-full flex items-center justify-center shadow-[0_0_15px_rgba(6,182,212,0.6)]"
          >
            <div className="w-6 h-6 border border-cyan-400 rounded-full flex items-center justify-center">
              <div className="w-2 h-2 bg-cyan-300 rounded-full"></div>
            </div>
          </motion.div>
          <div>
            <h1 className="text-2xl font-bold tracking-widest text-white uppercase">JARVIS Core</h1>
            <p className="text-xs text-cyan-500 tracking-widest">AXYNTRAX NEURAL LINK ACTIVE</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-xl font-bold text-white tracking-widest">{time.toLocaleTimeString()}</div>
          <div className="text-xs text-cyan-500 tracking-widest">{time.toLocaleDateString()}</div>
        </div>
      </header>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1 min-h-0">
        
        {/* Left Column: Ollama Status */}
        <div className="flex flex-col gap-6">
          <div className="bg-black/50 border border-cyan-900/50 rounded-lg p-4 backdrop-blur-md flex-1 overflow-hidden flex flex-col">
            <div className="flex items-center gap-2 mb-4 border-b border-cyan-900/50 pb-2">
              <Cpu className="w-5 h-5 text-cyan-400" />
              <h2 className="text-sm font-bold text-white uppercase tracking-widest">Ollama Node</h2>
              <span className={`ml-auto text-xs px-2 py-0.5 rounded border ${ollamaStatus === 'online' ? 'bg-cyan-900/30 border-cyan-500 text-cyan-400' : 'bg-red-900/30 border-red-500 text-red-400'} uppercase`}>
                {ollamaStatus}
              </span>
            </div>
            <div className="flex-1 overflow-y-auto pr-2 space-y-2">
              {ollamaStatus === 'online' && models.length === 0 && (
                <p className="text-xs text-slate-500">No models loaded.</p>
              )}
              {models.map((m: any, i: number) => (
                <div key={i} className="bg-cyan-950/20 border border-cyan-900/50 p-2 rounded flex justify-between items-center">
                  <span className="text-sm font-medium text-cyan-300">{m.name}</span>
                  <span className="text-xs text-slate-500">{(m.size / 1024 / 1024 / 1024).toFixed(1)} GB</span>
                </div>
              ))}
              {ollamaStatus === 'offline' && (
                <p className="text-xs text-red-400 animate-pulse">Connection refused. Ensure Ollama is running on port 11434.</p>
              )}
            </div>
          </div>

          <div className="bg-black/50 border border-cyan-900/50 rounded-lg p-4 backdrop-blur-md flex-1">
            <div className="flex items-center gap-2 mb-4 border-b border-cyan-900/50 pb-2">
              <Activity className="w-5 h-5 text-cyan-400" />
              <h2 className="text-sm font-bold text-white uppercase tracking-widest">System Load</h2>
            </div>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-xs mb-1"><span>CPU</span><span className="text-cyan-300">45%</span></div>
                <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden"><div className="bg-cyan-500 w-[45%] h-full"></div></div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1"><span>RAM</span><span className="text-cyan-300">12.4 GB</span></div>
                <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden"><div className="bg-cyan-500 w-[70%] h-full"></div></div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1"><span>GPU VRAM</span><span className="text-cyan-300">8.1 GB</span></div>
                <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden"><div className="bg-cyan-500 w-[65%] h-full"></div></div>
              </div>
            </div>
          </div>
        </div>

        {/* Center Column: JARVIS Terminal */}
        <div className="bg-black/50 border border-cyan-900/50 rounded-lg p-4 backdrop-blur-md flex flex-col lg:col-span-1">
          <div className="flex items-center gap-2 mb-4 border-b border-cyan-900/50 pb-2">
            <Terminal className="w-5 h-5 text-cyan-400" />
            <h2 className="text-sm font-bold text-white uppercase tracking-widest">Jarvis Logs</h2>
            <div className="ml-auto flex gap-1">
              <div className="w-2 h-2 rounded-full bg-red-500"></div>
              <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
              <div className="w-2 h-2 rounded-full bg-green-500"></div>
            </div>
          </div>
          <div className="flex-1 overflow-y-auto font-mono text-xs space-y-2 p-2 bg-[#020617] rounded border border-slate-800">
            <p className="text-cyan-600">[{time.toISOString()}] SYSTEM INITIALIZED</p>
            <p className="text-cyan-600">[{time.toISOString()}] ESTABLISHING NEURAL UPLINK...</p>
            <p className="text-green-500">[{time.toISOString()}] CONNECTION SECURE</p>
            <p className="text-slate-400">[{time.toISOString()}] Monitoring incoming threats...</p>
            <p className="text-slate-400">[{time.toISOString()}] Running diagnostics...</p>
            <p className="text-cyan-400">[{time.toISOString()}] All systems nominal.</p>
            <motion.div animate={{ opacity: [0, 1, 0] }} transition={{ repeat: Infinity, duration: 1 }} className="w-2 h-4 bg-cyan-500 inline-block mt-2"></motion.div>
          </div>
        </div>

        {/* Right Column: Comms */}
        <div className="flex flex-col gap-6">
          <div className="bg-black/50 border border-cyan-900/50 rounded-lg p-4 backdrop-blur-md flex-1 flex flex-col">
            <div className="flex items-center gap-2 mb-4 border-b border-cyan-900/50 pb-2">
              <Mail className="w-5 h-5 text-cyan-400" />
              <h2 className="text-sm font-bold text-white uppercase tracking-widest">Encrypted Comm</h2>
            </div>
            <div className="flex-1 overflow-y-auto space-y-3">
              {[
                { from: "DIRECTOR", sub: "Alpha Protocol", time: "10:42 AM" },
                { from: "STITCH", sub: "Patch deployed", time: "09:15 AM" },
                { from: "SYSADMIN", sub: "Server 04 down", time: "08:00 AM" }
              ].map((msg, i) => (
                <div key={i} className="border-l-2 border-cyan-500 pl-3 py-1">
                  <div className="flex justify-between text-xs">
                    <span className="font-bold text-cyan-300">{msg.from}</span>
                    <span className="text-slate-500">{msg.time}</span>
                  </div>
                  <p className="text-xs text-slate-400">{msg.sub}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-black/50 border border-cyan-900/50 rounded-lg p-4 backdrop-blur-md flex-1 flex flex-col">
            <div className="flex items-center gap-2 mb-4 border-b border-cyan-900/50 pb-2">
              <MessageSquare className="w-5 h-5 text-cyan-400" />
              <h2 className="text-sm font-bold text-white uppercase tracking-widest">Live Feed</h2>
            </div>
            <div className="flex-1 flex flex-col justify-end gap-2">
              <div className="bg-cyan-900/20 p-2 rounded text-xs text-slate-300 border border-cyan-900/30">
                <span className="text-cyan-500 font-bold">GHOSTMAN:</span> Initiate sweep.
              </div>
              <div className="bg-black p-2 rounded text-xs text-slate-300 border border-slate-800">
                <span className="text-purple-500 font-bold">JARVIS:</span> Sweeping sector 4. Clean.
              </div>
              <div className="mt-2 flex gap-2">
                <input type="text" className="w-full bg-black border border-cyan-900/50 rounded px-2 py-1 text-xs focus:outline-none focus:border-cyan-500 text-cyan-400" placeholder="Awaiting command..." />
                <button className="bg-cyan-900/50 border border-cyan-500 text-cyan-400 px-3 py-1 rounded text-xs font-bold hover:bg-cyan-500 hover:text-black transition-colors">TX</button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
