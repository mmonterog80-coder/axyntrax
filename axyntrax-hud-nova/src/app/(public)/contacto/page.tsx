"use client";

import { motion } from "framer-motion";
import { Mail, MapPin, Phone } from "lucide-react";

export default function ContactoPage() {
  return (
    <div className="container mx-auto px-6 py-24">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 max-w-6xl mx-auto">
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
          <h1 className="text-4xl font-bold text-white mb-6">Contacte a nuestro equipo</h1>
          <p className="text-lg text-slate-400 mb-12">Estamos listos para evaluar la infraestructura de su empresa y proponer soluciones de inteligencia corporativa.</p>
          
          <div className="space-y-8">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-slate-900 rounded-full flex items-center justify-center border border-slate-800">
                <MapPin className="w-5 h-5 text-cyan-400" />
              </div>
              <div>
                <h4 className="text-white font-medium">Sede Principal</h4>
                <p className="text-slate-400">Lima, Perú. Distrito Financiero, San Isidro.</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-slate-900 rounded-full flex items-center justify-center border border-slate-800">
                <Mail className="w-5 h-5 text-cyan-400" />
              </div>
              <div>
                <h4 className="text-white font-medium">Correo Electrónico</h4>
                <p className="text-slate-400">contacto@axyntrax.pe</p>
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="bg-slate-900/50 p-8 rounded-2xl border border-slate-800">
          <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Nombre Corporativo</label>
              <input type="text" className="w-full bg-[#020617] border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-cyan-500 transition-colors" placeholder="Empresa S.A.C." />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Correo Corporativo</label>
              <input type="email" className="w-full bg-[#020617] border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-cyan-500 transition-colors" placeholder="ejecutivo@empresa.com" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Requerimiento</label>
              <textarea rows={4} className="w-full bg-[#020617] border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-cyan-500 transition-colors" placeholder="Describa brevemente sus necesidades operativas..."></textarea>
            </div>
            <button className="w-full bg-cyan-500 hover:bg-cyan-400 text-[#020617] font-semibold py-3 rounded-lg transition-colors">
              Enviar Solicitud
            </button>
          </form>
        </motion.div>
      </div>
    </div>
  );
}
