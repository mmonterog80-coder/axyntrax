"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Send, Building2, Calendar, User, Mail, DollarSign, Package, Server, Code, Zap, CheckCircle2, ChevronRight } from "lucide-react";
import { useState } from "react";

const PRODUCTS = [
  {
    id: "p1",
    title: "Axyntrax CRM Local",
    category: "Gestión MYPE",
    price: 1500,
    icon: <Server size={32} />,
    features: ["Control de Inventario SUNAT", "Reportes IA", "Sin pago mensual"],
    color: "from-[#00ffcc] to-[#0088ff]"
  },
  {
    id: "p2",
    title: "AI Helpdesk Module",
    category: "Atención al Cliente",
    price: 2500,
    icon: <Zap size={32} />,
    features: ["Ollama/DeepSeek Local", "Tickets automáticos", "Cero latencia nube"],
    color: "from-[#ff00cc] to-[#3300ff]"
  },
  {
    id: "p3",
    title: "Web Corporativa Next.js",
    category: "Presencia Digital",
    price: 3500,
    icon: <Code size={32} />,
    features: ["Diseño Dark Premium", "SEO Técnico", "Dashboard Integrado"],
    color: "from-[#00ffcc] to-transparent"
  }
];

export default function VentasCatálogoPage() {
  const [selectedProduct, setSelectedProduct] = useState<string | null>(null);
  const [cart, setCart] = useState<string[]>([]);
  const [step, setStep] = useState(1);

  const toggleCart = (id: string) => {
    setCart(prev => prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]);
  };

  const total = cart.reduce((acc, id) => {
    const prod = PRODUCTS.find(p => p.id === id);
    return acc + (prod ? prod.price : 0);
  }, 0);

  return (
    <div className="min-h-screen bg-[#020202] text-[#e0e0e0] font-sans p-6 sm:p-12 selection:bg-[#00ffcc] selection:text-black relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-[#00ffcc] opacity-5 blur-[150px] rounded-full pointer-events-none"></div>

      <div className="max-w-7xl mx-auto relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-16 flex flex-col md:flex-row justify-between items-end border-b border-[#222] pb-8 gap-6"
        >
          <div>
            <div className="inline-block px-3 py-1 bg-[#111] text-[#00ffcc] text-xs font-bold tracking-widest uppercase mb-4 border border-[#00ffcc]/30 rounded-full">
              Catálogo Modular MYPE
            </div>
            <h1 className="text-4xl sm:text-7xl font-black uppercase tracking-tighter text-white">
              Marketplace
            </h1>
          </div>
          <div className="text-right">
            <div className="text-[#888] text-sm uppercase tracking-widest font-bold mb-2">Total Estimado</div>
            <div className="text-4xl font-black text-[#00ffcc]">S/ {total.toLocaleString()}</div>
          </div>
        </motion.div>

        {step === 1 && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
          >
            <AnimatePresence>
              {PRODUCTS.map((prod, i) => {
                const isSelected = cart.includes(prod.id);
                return (
                  <motion.div
                    key={prod.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                    onClick={() => toggleCart(prod.id)}
                    className={`relative p-8 rounded-2xl border cursor-pointer overflow-hidden transition-all duration-300 ${isSelected ? 'border-[#00ffcc] bg-[#00ffcc]/5 shadow-[0_0_30px_rgba(0,255,204,0.1)]' : 'border-[#222] bg-[#0a0a0a] hover:border-[#444]'}`}
                  >
                    {isSelected && (
                      <div className="absolute top-4 right-4 text-[#00ffcc]">
                        <CheckCircle2 size={24} />
                      </div>
                    )}
                    
                    <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${prod.color} flex items-center justify-center text-white mb-8`}>
                      {prod.icon}
                    </div>
                    
                    <div className="text-[#888] text-xs font-bold uppercase tracking-widest mb-2">{prod.category}</div>
                    <h3 className="text-2xl font-bold text-white mb-6">{prod.title}</h3>
                    
                    <ul className="space-y-3 mb-8">
                      {prod.features.map((feat, j) => (
                        <li key={j} className="flex items-center gap-3 text-sm text-[#aaa]">
                          <div className="w-1.5 h-1.5 rounded-full bg-[#00ffcc]"></div>
                          {feat}
                        </li>
                      ))}
                    </ul>

                    <div className="pt-6 border-t border-[#222] flex justify-between items-end">
                      <span className="text-xl font-black text-white">S/ {prod.price.toLocaleString()}</span>
                      <span className="text-xs uppercase tracking-widest text-[#555] font-bold">Uníco Pago</span>
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </motion.div>
        )}

        {step === 2 && (
          <motion.div 
            initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
            className="max-w-3xl mx-auto bg-[#0a0a0a] border border-[#222] p-8 md:p-12 rounded-2xl"
          >
            <h3 className="text-3xl font-black text-white uppercase tracking-tight mb-8">Confirmación Operativa</h3>
            
            <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-xs font-bold uppercase text-[#888] tracking-widest mb-2">RUC / Razón Social</label>
                  <input type="text" className="w-full bg-[#111] border border-[#333] p-4 text-white rounded-lg focus:outline-none focus:border-[#00ffcc]" />
                </div>
                <div>
                  <label className="block text-xs font-bold uppercase text-[#888] tracking-widest mb-2">Correo Corporativo</label>
                  <input type="email" className="w-full bg-[#111] border border-[#333] p-4 text-white rounded-lg focus:outline-none focus:border-[#00ffcc]" />
                </div>
              </div>
              <div>
                <label className="block text-xs font-bold uppercase text-[#888] tracking-widest mb-2">Requerimientos Específicos</label>
                <textarea className="w-full bg-[#111] border border-[#333] p-4 text-white rounded-lg focus:outline-none focus:border-[#00ffcc] min-h-[120px]"></textarea>
              </div>

              <div className="bg-[#111] p-6 rounded-xl border border-[#333] flex justify-between items-center mt-8">
                <div>
                  <div className="text-[#888] text-xs font-bold tracking-widest uppercase mb-1">Inversión Tecnológica</div>
                  <div className="text-3xl font-black text-[#00ffcc]">S/ {total.toLocaleString()}</div>
                </div>
                <button className="bg-[#00ffcc] hover:bg-white text-black font-black uppercase px-8 py-4 rounded-xl flex items-center gap-2 transition-colors shadow-[0_0_20px_rgba(0,255,204,0.3)]">
                  Procesar <ChevronRight size={20} />
                </button>
              </div>
            </form>
          </motion.div>
        )}

        {/* Footer Navigation */}
        <div className="mt-16 flex justify-center">
          {step === 1 && cart.length > 0 && (
            <motion.button 
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              onClick={() => setStep(2)}
              className="bg-white text-black hover:bg-[#00ffcc] font-black uppercase px-10 py-5 rounded-full flex items-center gap-3 shadow-xl transition-all"
            >
              <Package size={20} /> Configurar Instalación ({cart.length})
            </motion.button>
          )}
          {step === 2 && (
            <button 
              onClick={() => setStep(1)}
              className="text-[#888] hover:text-white uppercase tracking-widest text-sm font-bold flex items-center gap-2 transition-colors"
            >
              ← Volver al Catálogo
            </button>
          )}
        </div>

      </div>
    </div>
  );
}
