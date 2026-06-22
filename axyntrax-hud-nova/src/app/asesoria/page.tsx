"use client";

import { motion } from "framer-motion";
import { Building2, Cpu, Globe, Shield, Rocket, Check, ArrowRight } from "lucide-react";
import { useState } from "react";

export default function AsesoriaB2BPage() {
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null);
  const [infrastructure, setInfrastructure] = useState(50);
  const [aiAgents, setAiAgents] = useState(1);

  const calculatePrice = () => {
    let base = selectedPlan === "enterprise" ? 5000 : selectedPlan === "scale" ? 2500 : 0;
    let infraCost = infrastructure * 10;
    let agentCost = aiAgents * 500;
    return base === 0 ? "Seleccione Plan" : `$${(base + infraCost + agentCost).toLocaleString()} / mes`;
  };

  return (
    <div className="min-h-screen bg-[#020202] text-[#e0e0e0] font-sans p-6 sm:p-12 selection:bg-[#00ffcc] selection:text-black">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-20"
        >
          <div className="inline-block px-4 py-1 bg-[#111] text-[#00ffcc] text-sm font-bold tracking-[0.2em] uppercase mb-6 border border-[#00ffcc]/30 rounded-full">
            División Corporativa
          </div>
          <h1 className="text-5xl md:text-8xl font-black uppercase tracking-tighter text-white mb-6">
            Asesoría <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#00ffcc] to-[#0088ff]">B2B</span>
          </h1>
          <p className="text-[#888] text-lg md:text-2xl max-w-3xl mx-auto font-light">
            Transforme su infraestructura operativa con ecosistemas de Inteligencia Artificial Autónoma diseñados por Axyntrax.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          {/* Calculadora de Infraestructura */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-[#0a0a0a] border border-[#222] p-8 md:p-12 rounded-2xl relative overflow-hidden group hover:border-[#333] transition-colors"
          >
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-[#00ffcc] to-transparent opacity-50"></div>
            <h3 className="text-3xl font-black text-white uppercase tracking-tight mb-10 flex items-center gap-4">
              <Cpu className="text-[#00ffcc]" size={32} /> Arquitectura IA
            </h3>

            <div className="space-y-10">
              {/* Slider 1 */}
              <div>
                <div className="flex justify-between text-sm font-bold tracking-widest text-[#888] uppercase mb-4">
                  <span>Capacidad de Cómputo (TB/s)</span>
                  <span className="text-[#00ffcc]">{infrastructure} TB/s</span>
                </div>
                <input 
                  type="range" 
                  min="10" max="500" step="10"
                  value={infrastructure}
                  onChange={(e) => setInfrastructure(Number(e.target.value))}
                  className="w-full accent-[#00ffcc] h-2 bg-[#222] rounded-lg appearance-none cursor-pointer"
                />
              </div>

              {/* Slider 2 */}
              <div>
                <div className="flex justify-between text-sm font-bold tracking-widest text-[#888] uppercase mb-4">
                  <span>Agentes Autónomos</span>
                  <span className="text-[#00ffcc]">{aiAgents} Swarm Nodes</span>
                </div>
                <input 
                  type="range" 
                  min="1" max="20"
                  value={aiAgents}
                  onChange={(e) => setAiAgents(Number(e.target.value))}
                  className="w-full accent-[#00ffcc] h-2 bg-[#222] rounded-lg appearance-none cursor-pointer"
                />
              </div>

              {/* Selector de Plan */}
              <div className="grid grid-cols-2 gap-4 pt-6">
                <button 
                  onClick={() => setSelectedPlan("scale")}
                  className={`p-6 border text-left rounded-xl transition-all ${selectedPlan === "scale" ? 'border-[#00ffcc] bg-[#00ffcc]/10' : 'border-[#333] bg-[#111] hover:border-[#555]'}`}
                >
                  <Rocket className={selectedPlan === "scale" ? "text-[#00ffcc] mb-4" : "text-[#555] mb-4"} size={28} />
                  <div className="font-bold text-white text-xl">AXYNTRAX SCALE</div>
                  <div className="text-[#888] text-sm mt-2">Para MYPEs en crecimiento</div>
                </button>
                <button 
                  onClick={() => setSelectedPlan("enterprise")}
                  className={`p-6 border text-left rounded-xl transition-all ${selectedPlan === "enterprise" ? 'border-[#0088ff] bg-[#0088ff]/10' : 'border-[#333] bg-[#111] hover:border-[#555]'}`}
                >
                  <Building2 className={selectedPlan === "enterprise" ? "text-[#0088ff] mb-4" : "text-[#555] mb-4"} size={28} />
                  <div className="font-bold text-white text-xl">AXYNTRAX ELITE</div>
                  <div className="text-[#888] text-sm mt-2">Para corporaciones</div>
                </button>
              </div>

              {/* Precio Total */}
              <div className="mt-12 pt-8 border-t border-[#222] flex flex-col md:flex-row md:items-end justify-between gap-6">
                <div>
                  <div className="text-[#555] text-xs font-bold tracking-[0.2em] uppercase mb-2">Inversión Estimada</div>
                  <div className="text-4xl md:text-5xl font-black text-white">{calculatePrice()}</div>
                </div>
                <button className="bg-white hover:bg-[#00ffcc] text-black px-8 py-4 rounded-full font-bold uppercase tracking-wider transition-colors flex items-center justify-center gap-3">
                  Agendar <ArrowRight size={18} />
                </button>
              </div>
            </div>
          </motion.div>

          {/* Propuesta de Valor */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="space-y-8"
          >
            <div className="bg-[#111] p-8 rounded-2xl border border-[#222]">
              <div className="w-12 h-12 bg-[#00ffcc]/10 rounded-full flex items-center justify-center mb-6">
                <Globe className="text-[#00ffcc]" size={24} />
              </div>
              <h4 className="text-2xl font-bold text-white mb-4">Alcance Global, ADN Local</h4>
              <p className="text-[#888] leading-relaxed">
                Nuestros sistemas están entrenados para entender el contexto empresarial peruano e internacional, optimizando la facturación y la experiencia de usuario (SUNAT-ready).
              </p>
            </div>

            <div className="bg-[#111] p-8 rounded-2xl border border-[#222]">
              <div className="w-12 h-12 bg-[#0088ff]/10 rounded-full flex items-center justify-center mb-6">
                <Shield className="text-[#0088ff]" size={24} />
              </div>
              <h4 className="text-2xl font-bold text-white mb-4">Seguridad de Grado Militar</h4>
              <p className="text-[#888] leading-relaxed">
                Cada nodo de IA opera bajo un modelo de gobernanza estricto (Fase 6). Aislamiento de datos, tolerancia a fallos y auditorías automáticas continuas.
              </p>
            </div>

            <ul className="space-y-4 pt-6">
              {["Implementación en 48 horas", "Soporte Técnico 24/7 Nivel 3", "Integración con ERPs Legacy", "Orquestación LangGraph nativa"].map((item, i) => (
                <li key={i} className="flex items-center gap-4 text-[#aaa] font-medium">
                  <div className="w-6 h-6 rounded-full bg-[#222] flex items-center justify-center flex-shrink-0">
                    <Check className="text-[#00ffcc]" size={14} />
                  </div>
                  {item}
                </li>
              ))}
            </ul>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
