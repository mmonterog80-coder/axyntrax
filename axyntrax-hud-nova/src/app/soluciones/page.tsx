"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const modules = [
  {
    id: "crm",
    title: "CRM Inteligente",
    description: "Gestión de clientes con IA entrenada en tu rubro.",
    icon: "🤝",
    color: "from-blue-600 to-indigo-600",
    price: 49,
  },
  {
    id: "whatsapp",
    title: "WhatsApp Bot IA",
    description: "Atención 24/7 y cierre de ventas automático.",
    icon: "💬",
    color: "from-emerald-500 to-green-600",
    price: 39,
  },
  {
    id: "billing",
    title: "Facturación Electrónica",
    description: "Emite boletas y facturas validadas por SUNAT al instante.",
    icon: "🧾",
    color: "from-amber-500 to-orange-600",
    price: 29,
  },
  {
    id: "inventory",
    title: "Inventario Predictivo",
    description: "Control de stock en tiempo real con proyecciones de IA.",
    icon: "📦",
    color: "from-purple-500 to-violet-600",
    price: 35,
  },
];

export default function ConstructorEcosistema() {
  const [selectedModules, setSelectedModules] = useState<string[]>([]);

  const toggleModule = (id: string) => {
    setSelectedModules((prev) =>
      prev.includes(id) ? prev.filter((m) => m !== id) : [...prev, id]
    );
  };

  const totalPrice = selectedModules.reduce((acc, curr) => {
    const mod = modules.find((m) => m.id === curr);
    return acc + (mod?.price || 0);
  }, 0);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 selection:bg-indigo-500/30 overflow-hidden relative">
      {/* Background gradients */}
      <div className="absolute inset-0 z-0 flex justify-center items-center pointer-events-none opacity-20">
        <div className="w-[800px] h-[800px] bg-indigo-500/30 rounded-full blur-[120px] mix-blend-screen" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-16 md:py-24">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="text-center mb-16"
        >
          <div className="inline-block px-4 py-1.5 mb-6 rounded-full bg-slate-900 border border-slate-800 text-sm font-medium text-indigo-400 tracking-wide uppercase">
            Constructor de Ecosistemas Modulares
          </div>
          <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-slate-100 to-slate-500">
            Arma tu propia armadura digital
          </h1>
          <p className="text-xl md:text-2xl text-slate-400 max-w-3xl mx-auto italic font-light">
            "Axyntrax se acomoda a su empresa, nunca al revés."
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-12 items-start">
          <div className="lg:col-span-2 grid sm:grid-cols-2 gap-6">
            {modules.map((mod, idx) => {
              const isSelected = selectedModules.includes(mod.id);
              return (
                <motion.button
                  key={mod.id}
                  onClick={() => toggleModule(mod.id)}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: idx * 0.1 }}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`relative p-6 rounded-3xl border transition-all duration-300 text-left overflow-hidden h-full ${
                    isSelected
                      ? "border-indigo-500/50 bg-slate-900/80 shadow-[0_0_30px_rgba(99,102,241,0.15)]"
                      : "border-slate-800 bg-slate-900/30 hover:border-slate-700 hover:bg-slate-900/50"
                  }`}
                >
                  <div
                    className={`absolute inset-0 bg-gradient-to-br ${mod.color} opacity-0 transition-opacity duration-300 ${
                      isSelected ? "opacity-10" : ""
                    }`}
                  />
                  
                  {/* Glowing corner if selected */}
                  {isSelected && (
                    <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-indigo-500/20 to-transparent rounded-bl-[100px]" />
                  )}

                  <div className="relative z-10 flex flex-col h-full">
                    <div className="flex justify-between items-start mb-4">
                      <span className="text-4xl drop-shadow-sm">{mod.icon}</span>
                      <div
                        className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                          isSelected
                            ? "border-indigo-400 bg-indigo-500/20"
                            : "border-slate-700 bg-slate-800/50"
                        }`}
                      >
                        {isSelected && (
                          <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            className="w-2.5 h-2.5 bg-indigo-400 rounded-full shadow-[0_0_10px_rgba(129,140,248,0.8)]"
                          />
                        )}
                      </div>
                    </div>
                    <h3 className="text-xl font-semibold mb-2 text-slate-100">
                      {mod.title}
                    </h3>
                    <p className="text-slate-400 text-sm flex-grow mb-4">
                      {mod.description}
                    </p>
                    <div className="mt-auto flex items-end justify-between">
                      <span className="text-sm font-medium text-slate-500 uppercase tracking-wider">
                        Módulo
                      </span>
                      <span className="text-lg font-bold text-slate-200">
                        S/ {mod.price} <span className="text-xs font-normal text-slate-500">/mes</span>
                      </span>
                    </div>
                  </div>
                </motion.button>
              );
            })}
          </div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="sticky top-24 bg-slate-900/60 border border-slate-800 rounded-3xl p-8 backdrop-blur-xl shadow-2xl"
          >
            <h2 className="text-2xl font-bold mb-6 text-slate-100 flex items-center gap-3">
              <span className="text-indigo-400">⚡</span> Tu Ecosistema
            </h2>
            
            <div className="min-h-[160px] mb-8">
              <AnimatePresence mode="popLayout">
                {selectedModules.length === 0 ? (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="text-slate-500 text-center py-8 border-2 border-dashed border-slate-800 rounded-2xl flex flex-col items-center gap-3"
                  >
                    <span className="text-3xl opacity-50">🧩</span>
                    <p className="text-sm">Selecciona módulos para armar tu solución</p>
                  </motion.div>
                ) : (
                  <div className="space-y-3">
                    {selectedModules.map((id) => {
                      const mod = modules.find((m) => m.id === id)!;
                      return (
                        <motion.div
                          key={id}
                          layout
                          initial={{ opacity: 0, scale: 0.9, x: -20 }}
                          animate={{ opacity: 1, scale: 1, x: 0 }}
                          exit={{ opacity: 0, scale: 0.9, x: 20 }}
                          className="flex items-center justify-between p-3 rounded-xl bg-slate-800/50 border border-slate-700/50"
                        >
                          <div className="flex items-center gap-3">
                            <span>{mod.icon}</span>
                            <span className="font-medium text-sm text-slate-200">{mod.title}</span>
                          </div>
                          <span className="text-sm font-semibold text-indigo-300">
                            S/ {mod.price}
                          </span>
                        </motion.div>
                      );
                    })}
                  </div>
                )}
              </AnimatePresence>
            </div>

            <div className="pt-6 border-t border-slate-800">
              <div className="flex justify-between items-end mb-6">
                <div>
                  <p className="text-slate-400 text-sm mb-1">Inversión Mensual</p>
                  <p className="text-3xl font-bold text-white">
                    S/ {totalPrice}
                  </p>
                </div>
                {selectedModules.length > 0 && (
                  <span className="text-xs text-indigo-400 bg-indigo-500/10 px-2 py-1 rounded-md border border-indigo-500/20">
                    IA Integrada
                  </span>
                )}
              </div>
              
              <button
                disabled={selectedModules.length === 0}
                className={`w-full py-4 rounded-xl font-semibold tracking-wide transition-all duration-300 ${
                  selectedModules.length > 0
                    ? "bg-indigo-600 hover:bg-indigo-500 text-white shadow-[0_0_20px_rgba(79,70,229,0.3)] hover:shadow-[0_0_30px_rgba(79,70,229,0.5)]"
                    : "bg-slate-800 text-slate-500 cursor-not-allowed"
                }`}
              >
                {selectedModules.length > 0 ? "Desplegar Sistema" : "Configura tu plan"}
              </button>
            </div>
            
            {/* Added detail */}
            <p className="text-xs text-center text-slate-500 mt-4">
              Cada módulo incluye una IA especializada en el rubro de tu empresa.
            </p>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
