import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Mail, MessageSquare, Zap, Shield, Cpu, Send, Mic } from 'lucide-react';
import axios from 'axios';

interface ChatMessage {
  id: string;
  sender: 'jarvis' | 'user';
  text: string;
  timestamp: string;
  audio?: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([{
    id: 'init',
    sender: 'jarvis',
    text: 'Sistemas en línea, señor. Cuartel General conectado y estabilizado a la red neural AXYNTRAX. ¿Cuáles son sus órdenes?',
    timestamp: new Date().toLocaleTimeString()
  }]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: input,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsThinking(true);

    try {
      // Connect to the actual backend via localtunnel or direct localhost if cors allows
      // Currently assuming localtunnel is working and CORS is okay or we hit local directly.
      // For local testing, we might want to hit http://localhost:8000/api/chat directly
      // but CORS needs to be handled on backend. Using the localtunnel.
      const response = await axios.post(`${API_BASE_URL}/chat`, { message: userMsg.text }, {
        headers: {
          'Authorization': 'Bearer axyntrax-secret-change-me',
          'Bypass-Tunnel-Reminder': 'true'
        }
      });
      
      const jarvisMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'jarvis',
        text: response.data.reply || 'Fallo de conexión en el clúster neural.',
        timestamp: new Date().toLocaleTimeString(),
        audio: response.data.audio
      };
      
      setMessages(prev => [...prev, jarvisMsg]);
      
      if (jarvisMsg.audio) {
        const snd = new Audio(`data:audio/mp3;base64,${jarvisMsg.audio}`);
        snd.play();
      }
      
    } catch (error) {
      console.error(error);
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'jarvis',
        text: 'Señor, no puedo alcanzar el puerto de enlace de la API. ¿Ha inicializado el servidor orchestrator principal?',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsThinking(false);
    }
  };

  return (
    <div className="dashboard-container">
      {/* LEFT SIDEBAR - VITALS & INBOX */}
      <div className="flex flex-col gap-6">
        
        {/* Status Panel */}
        <div className="glass-panel">
          <div className="flex items-center gap-3 mb-6">
            <Cpu className="w-6 h-6 text-accent-blue" />
            <h2 className="text-xl m-0">AXYNTRAX Core</h2>
          </div>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-text-muted flex items-center">
                <span className={`status-dot ${isThinking ? 'thinking' : 'active'}`}></span>
                J.A.R.V.I.S. Status
              </span>
              <span className={isThinking ? 'text-accent-purple font-medium' : 'text-accent-green font-medium'}>
                {isThinking ? 'PROCESANDO...' : 'EN LÍNEA'}
              </span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-text-muted flex items-center">
                <Shield className="w-4 h-4 mr-2" />
                Seguridad MCP
              </span>
              <span className="text-accent-blue font-medium">MAX CLEARANCE</span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-text-muted flex items-center">
                <Zap className="w-4 h-4 mr-2" />
                Consumo IA (Mensual)
              </span>
              <span className="text-white font-mono">S/ 45.20</span>
            </div>
          </div>
        </div>

        {/* Inbox Panel */}
        <div className="glass-panel flex-1 overflow-hidden flex flex-col">
          <div className="flex items-center gap-3 mb-4">
            <Mail className="w-6 h-6 text-accent-purple" />
            <h2 className="text-xl m-0">Gmail Intercept</h2>
          </div>
          <p className="subtitle mb-4">Esperando credenciales OAuth2 para sincronización...</p>
          
          <div className="flex-1 overflow-y-auto hide-scrollbar space-y-3">
             <div className="p-3 bg-white/5 rounded-lg border border-white/10 opacity-50">
               <h4 className="font-medium text-sm text-white mb-1">Autorización Pendiente</h4>
               <p className="text-xs text-text-muted">J.A.R.V.I.S. requiere archivo credentials.json en el backend.</p>
             </div>
          </div>
        </div>
        
      </div>

      {/* RIGHT SIDE - C&C CHAT */}
      <div className="glass-panel flex flex-col h-full overflow-hidden">
        <div className="flex items-center gap-3 mb-6 pb-4 border-b border-white/10">
          <MessageSquare className="w-6 h-6 text-accent-blue" />
          <div>
            <h2 className="text-xl m-0">Canal de Comando Central</h2>
            <p className="subtitle m-0">Enlace encriptado a red neural profunda</p>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto hide-scrollbar pr-2 mb-4 space-y-4">
          {messages.map((msg) => (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              key={msg.id} 
              className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
            >
              <span className="text-xs text-text-muted mb-1 ml-1 mr-1">
                {msg.sender === 'user' ? 'Señor' : 'J.A.R.V.I.S.'} • {msg.timestamp}
              </span>
              <div 
                className={`p-3.5 max-w-[80%] rounded-2xl ${
                  msg.sender === 'user' 
                    ? 'bg-blue-600/20 border border-blue-500/30 text-white rounded-br-none' 
                    : 'bg-white/5 border border-white/10 text-gray-200 rounded-bl-none'
                }`}
              >
                {msg.text}
              </div>
            </motion.div>
          ))}
          {isThinking && (
             <motion.div 
             initial={{ opacity: 0 }}
             animate={{ opacity: 1 }}
             className="flex flex-col items-start"
           >
             <span className="text-xs text-text-muted mb-1 ml-1">J.A.R.V.I.S. • Calculando...</span>
             <div className="p-3.5 bg-white/5 border border-white/10 rounded-2xl rounded-bl-none flex gap-1">
               <span className="w-2 h-2 bg-accent-purple rounded-full animate-bounce"></span>
               <span className="w-2 h-2 bg-accent-purple rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></span>
               <span className="w-2 h-2 bg-accent-purple rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></span>
             </div>
           </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form onSubmit={handleSendMessage} className="relative mt-auto">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isThinking}
            placeholder="Ingrese comando, señor..." 
            className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-4 pr-24 text-white focus:outline-none focus:border-accent-blue/50 transition-colors"
          />
          <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
            <button type="button" className="p-2 text-text-muted hover:text-white transition-colors">
              <Mic className="w-5 h-5" />
            </button>
            <button 
              type="submit" 
              disabled={!input.trim() || isThinking}
              className="p-2 bg-accent-blue/20 text-accent-blue rounded-lg hover:bg-accent-blue/30 transition-colors disabled:opacity-50"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
