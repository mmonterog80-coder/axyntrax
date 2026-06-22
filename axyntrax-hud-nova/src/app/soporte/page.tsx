"use client";

import { motion } from "framer-motion";
import { Ticket, AlertCircle, Clock, CheckCircle2, Search, Send, Bot, User, Loader2 } from "lucide-react";
import { useState, useRef, useEffect } from "react";

export default function SoportePage() {
  const [messages, setMessages] = useState<{role: 'user'|'ai', content: string}[]>([
    { role: 'ai', content: 'Sistema de Soporte IA Axyntrax iniciado. ¿En qué puedo ayudarle hoy?' }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      // Connect to local Ollama instance (Ensure Ollama is running)
      const response = await fetch("http://localhost:11434/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "qwen2.5-coder", // Defaulting to qwen2.5-coder as per fallback matrix
          prompt: `Eres el agente de Soporte Técnico Nivel 1 de Axyntrax. Responde de manera profesional, corporativa y concisa. Usuario: ${userMessage}`,
          stream: false
        })
      });

      if (!response.ok) throw new Error("Ollama connection failed");
      const data = await response.json();
      
      setMessages(prev => [...prev, { role: 'ai', content: data.response }]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: 'ERROR: No se pudo conectar con el núcleo de IA local (Ollama). Por favor, asegúrese de que el servicio está activo.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#050505] text-[#e0e0e0] font-mono p-6 sm:p-12 selection:bg-[#00ffcc] selection:text-black">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-16 border-b border-[#222] pb-12"
        >
          <div>
            <div className="inline-block px-3 py-1 bg-[#222] text-white text-xs font-bold tracking-widest uppercase mb-4 border border-[#333]">
              Soporte IA Autónomo v3.0
            </div>
            <h1 className="text-4xl sm:text-7xl font-black uppercase tracking-tighter text-white">
              Soporte Técnico
            </h1>
          </div>
          <div className="relative w-full md:w-72">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-[#555]" size={20} />
            <input type="text" placeholder="BUSCAR ID TICKET..." className="w-full bg-[#111] border border-[#333] py-3 pl-12 pr-4 text-white uppercase focus:outline-none focus:border-[#00ffcc] transition-colors" />
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Columna Izquierda: Chat IA */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-7 flex flex-col h-[600px]"
          >
            <div className="bg-[#0a0a0a] border border-[#222] p-4 flex items-center justify-between">
              <h3 className="text-xl font-bold uppercase text-white flex items-center gap-3">
                <Bot className="text-[#00ffcc]" /> AI Assistant
              </h3>
              <div className="flex items-center gap-2 text-xs text-[#00ffcc] border border-[#00ffcc]/30 px-2 py-1 bg-[#00ffcc]/10">
                <span className="w-2 h-2 rounded-full bg-[#00ffcc] animate-pulse"></span>
                OLLAMA ONLINE
              </div>
            </div>
            
            <div className="flex-1 bg-[#111] border-x border-[#222] p-6 overflow-y-auto space-y-6">
              {messages.map((msg, i) => (
                <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[80%] p-4 border ${msg.role === 'user' ? 'bg-[#222] border-[#444] text-white' : 'bg-[#0a0a0a] border-[#00ffcc]/30 text-[#00ffcc]'} shadow-lg relative`}>
                    {/* Decorative Corner */}
                    <div className={`absolute top-0 w-2 h-2 border-t border-l ${msg.role === 'user' ? 'left-0 border-[#fff]' : 'left-0 border-[#00ffcc]'}`}></div>
                    
                    <div className="flex items-center gap-2 mb-2 opacity-60 text-xs font-bold tracking-widest uppercase">
                      {msg.role === 'user' ? <User size={14} /> : <Bot size={14} />}
                      {msg.role === 'user' ? 'USER' : 'AXYNTRAX AI'}
                    </div>
                    <div className="text-sm leading-relaxed whitespace-pre-wrap font-sans">
                      {msg.content}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-[#0a0a0a] border border-[#00ffcc]/30 p-4 text-[#00ffcc] flex items-center gap-3">
                    <Loader2 size={16} className="animate-spin" /> Procesando petición...
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className="bg-[#0a0a0a] border border-[#222] p-4">
              <form onSubmit={handleSubmit} className="flex gap-4">
                <input 
                  type="text" 
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Describa su problema..." 
                  disabled={isLoading}
                  className="flex-1 bg-[#111] border border-[#333] p-3 text-white focus:outline-none focus:border-[#00ffcc] transition-colors"
                />
                <button 
                  type="submit" 
                  disabled={isLoading || !input.trim()}
                  className="bg-white hover:bg-[#00ffcc] text-black px-6 font-black uppercase transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  <Send size={18} /> Enviar
                </button>
              </form>
            </div>
          </motion.div>

          {/* Columna Derecha: Tickets */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="lg:col-span-5"
          >
            <h3 className="text-xl font-bold uppercase text-white mb-6">Tickets Recientes</h3>
            <div className="space-y-4">
              {[
                { id: "TKT-8902", title: "Error de conexión en módulo CRM", status: "ESCALADO A IA", time: "Hace 2 horas", color: "text-purple-500", border: "border-purple-500/30" },
                { id: "TKT-8895", title: "Actualización de dashboard gerencial", status: "RESUELTO", time: "Ayer", color: "text-[#00ffcc]", border: "border-[#00ffcc]/30" },
                { id: "TKT-8891", title: "Consulta sobre facturación IA", status: "RESUELTO", time: "Hace 3 días", color: "text-[#00ffcc]", border: "border-[#00ffcc]/30" },
              ].map((ticket, i) => (
                <div key={i} className={`bg-[#0a0a0a] border ${ticket.border} p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-[#111] transition-colors cursor-pointer group`}>
                  <div className="flex items-center gap-4">
                    <div className="p-3 bg-[#111] border border-[#333] group-hover:border-[#555] transition-colors">
                      {ticket.status === "RESUELTO" ? <CheckCircle2 className={ticket.color} size={24} /> : <AlertCircle className={ticket.color} size={24} />}
                    </div>
                    <div>
                      <div className="text-[#555] text-xs font-bold tracking-widest mb-1">{ticket.id}</div>
                      <div className="text-white font-bold text-sm">{ticket.title}</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-6 sm:text-right">
                    <div className="hidden sm:block">
                      <div className={`${ticket.color} font-bold text-xs uppercase tracking-wider`}>{ticket.status}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 bg-[#111] border border-[#222] p-6 text-sm text-[#888] leading-relaxed">
              * El Soporte Autónomo IA intentará resolver su problema. Si no se puede solucionar, el ticket será escalado al Nivel 2 humano de Axyntrax.
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
