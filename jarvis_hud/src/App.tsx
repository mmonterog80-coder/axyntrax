import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mail, MessageSquare, Send, Mic, Activity, Database, Server, Hexagon } from 'lucide-react';
import axios from 'axios';

interface ChatMessage {
  id: string;
  sender: 'jarvis' | 'user';
  text: string;
  timestamp: string;
  audio?: string;
}

interface SwarmAgent {
  id: string;
  name: string;
  role: string;
  status: string;
  mem: string;
  sub_agents?: SwarmAgent[];
}

interface MailMessage {
  id: string;
  subject: string;
  snippet: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([{
    id: 'init',
    sender: 'jarvis',
    text: 'Sistemas en línea, señor. Cuartel General V6.0 conectado a la matriz cuántica. ¿Cuáles son sus órdenes?',
    timestamp: new Date().toLocaleTimeString()
  }]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [swarm, setSwarm] = useState<SwarmAgent[]>([]);
  const [inbox, setInbox] = useState<MailMessage[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Fetch Swarm Status
    axios.get(`${API_BASE_URL}/swarm/status`, {
      headers: { 'Authorization': 'Bearer axyntrax-secret-change-me' }
    }).then(res => setSwarm(res.data.swarm || []))
      .catch(err => console.error("Error fetching swarm", err));

    // Fetch Gmail Inbox
    axios.get(`${API_BASE_URL}/gmail/inbox`, {
      headers: { 'Authorization': 'Bearer axyntrax-secret-change-me' }
    }).then(res => setInbox(res.data.inbox || []))
      .catch(err => console.error("Error fetching inbox", err));
  }, []);

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
      const response = await axios.post(`${API_BASE_URL}/chat`, { message: userMsg.text }, {
        headers: {
          'Authorization': 'Bearer axyntrax-secret-change-me'
        }
      });
      
      const jarvisMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'jarvis',
        text: response.data.reply || 'Anomalía detectada en el núcleo principal.',
        timestamp: new Date().toLocaleTimeString(),
        audio: response.data.audio
      };
      
      setMessages(prev => [...prev, jarvisMsg]);
      
      if (jarvisMsg.audio) {
        const snd = new Audio(`data:audio/mp3;base64,${jarvisMsg.audio}`);
        snd.play();
      }
    } catch (error) {
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        sender: 'jarvis',
        text: 'Señor, no puedo conectar con el servidor principal.',
        timestamp: new Date().toLocaleTimeString()
      }]);
    } finally {
      setIsThinking(false);
    }
  };

  const calculateTotalCost = () => {
    // Dummy calculo para demostrar moneda en Soles
    return "S/ 124.50";
  };

  return (
    <div className="min-h-screen w-full relative overflow-hidden flex flex-col p-6 gap-6">
      {/* Background Blurs for God Eye effect */}
      <div className="blur-node bg-blue-500/30 w-[600px] h-[600px] top-[-200px] left-[-200px]" />
      <div className="blur-node bg-cyan-400/20 w-[800px] h-[800px] bottom-[-300px] right-[-300px]" />
      <div className="blur-node bg-white/10 w-[500px] h-[500px] top-[20%] left-[40%]" />

      {/* GOD EYE WIREFRAME CENTER */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none opacity-40 mix-blend-screen z-0">
        <div className="wireframe-sphere">
          <div className="wireframe-core"></div>
        </div>
      </div>

      {/* HEADER */}
      <header className="z-10 flex justify-between items-start">
        <div>
          <h1 className="holographic-text text-3xl font-syncopate tracking-widest m-0 flex items-center gap-3">
            <Hexagon className="text-cyan-300 w-8 h-8" />
            AXYNTRAX <span className="text-white/50 font-light">V6.0</span>
          </h1>
          <p className="text-cyan-200/60 font-mono text-sm tracking-widest mt-1">SISTEMA CIBERNÉTICO CENTRAL</p>
        </div>
        <div className="glass-panel px-6 py-3 flex items-center gap-6">
          <div className="flex flex-col items-end">
            <span className="text-xs text-white/50 font-mono">CONSUMO NÚCLEO</span>
            <span className="text-cyan-300 font-bold font-mono text-lg">{calculateTotalCost()}</span>
          </div>
          <div className="w-[1px] h-8 bg-white/20"></div>
          <div className="flex flex-col items-end">
            <span className="text-xs text-white/50 font-mono">STATUS</span>
            <span className="text-emerald-400 font-bold tracking-widest flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              SECURE
            </span>
          </div>
        </div>
      </header>

      {/* MAIN LAYOUT */}
      <div className="z-10 flex-1 grid grid-cols-12 gap-6 h-[calc(100vh-140px)]">
        
        {/* LEFT PANEL - GMAIL & VITALS */}
        <div className="col-span-3 flex flex-col gap-6">
          <div className="glass-panel flex-1 p-5 flex flex-col overflow-hidden relative">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-cyan-400 to-transparent"></div>
            <div className="flex items-center gap-3 mb-4">
              <Mail className="w-5 h-5 text-cyan-300" />
              <h2 className="text-lg font-syncopate text-white/90 m-0">Intercept</h2>
              <span className="ml-auto bg-cyan-500/20 text-cyan-300 text-xs px-2 py-1 rounded">GMAIL</span>
            </div>
            
            <div className="flex-1 overflow-y-auto hide-scrollbar space-y-3">
              {inbox.length > 0 ? inbox.map(mail => (
                <div key={mail.id} className="p-3 bg-white/5 hover:bg-white/10 transition rounded-lg border border-white/10 cursor-pointer">
                  <h4 className="font-medium text-sm text-white mb-1 truncate">{mail.subject}</h4>
                  <p className="text-xs text-white/60 line-clamp-2">{mail.snippet}</p>
                </div>
              )) : (
                <div className="flex flex-col items-center justify-center h-full text-white/30 gap-2">
                  <Mail className="w-8 h-8" />
                  <p className="text-xs text-center">Bandeja despejada o credenciales pendientes</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* CENTER PANEL - SWARM AI STATUS */}
        <div className="col-span-4 flex flex-col gap-6">
          <div className="glass-panel flex-1 p-5 overflow-hidden flex flex-col relative">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-400 to-transparent"></div>
            <div className="flex items-center gap-3 mb-4">
              <Database className="w-5 h-5 text-blue-300" />
              <h2 className="text-lg font-syncopate text-white/90 m-0">Swarm IAs</h2>
            </div>

            <div className="flex-1 overflow-y-auto hide-scrollbar pr-2 space-y-4">
              {swarm.map(dept => (
                <div key={dept.id} className="mb-4">
                  <div className="flex justify-between items-center mb-2 bg-white/5 p-2 rounded border border-white/5">
                    <span className="font-bold text-sm text-white flex items-center gap-2">
                      <Server className="w-3 h-3 text-cyan-400" />
                      {dept.name} <span className="text-[10px] text-white/40 uppercase">{dept.role}</span>
                    </span>
                    <span className={`text-xs ${dept.status === 'ONLINE' ? 'text-emerald-400' : 'text-amber-400'}`}>{dept.status}</span>
                  </div>
                  {dept.sub_agents && dept.sub_agents.length > 0 && (
                    <div className="pl-4 border-l border-white/10 space-y-2 ml-2">
                      {dept.sub_agents.map(sub => (
                        <div key={sub.id} className="flex justify-between items-center text-xs">
                          <span className="text-white/70 flex items-center gap-2">
                            <Activity className="w-3 h-3 text-blue-400" /> {sub.name}
                          </span>
                          <span className={sub.status === 'ONLINE' ? 'text-emerald-400/70' : 'text-amber-400/70'}>{sub.status}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
              {swarm.length === 0 && (
                <div className="text-center text-white/30 text-xs mt-10">Conectando a la matriz...</div>
              )}
            </div>
          </div>
        </div>

        {/* RIGHT PANEL - CHAT TERMINAL */}
        <div className="col-span-5 flex flex-col h-full">
          <div className="glass-panel flex-1 p-5 flex flex-col relative">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-400 to-transparent"></div>
            <div className="flex items-center gap-3 mb-4 pb-4 border-b border-white/10">
              <MessageSquare className="w-5 h-5 text-purple-300" />
              <div>
                <h2 className="text-lg font-syncopate text-white/90 m-0">Terminal Neural</h2>
                <p className="text-[10px] text-white/40 uppercase tracking-widest mt-1">Conexión directa: JARVIS CORE</p>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto hide-scrollbar pr-2 mb-4 space-y-4">
              <AnimatePresence>
                {messages.map((msg) => (
                  <motion.div 
                    initial={{ opacity: 0, x: msg.sender === 'user' ? 20 : -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    key={msg.id} 
                    className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
                  >
                    <span className="text-[10px] text-white/40 uppercase tracking-widest mb-1 ml-1 mr-1">
                      {msg.sender === 'user' ? 'Director' : 'J.A.R.V.I.S.'} • {msg.timestamp}
                    </span>
                    <div 
                      className={`p-3 max-w-[85%] rounded-xl text-sm leading-relaxed backdrop-blur-md ${
                        msg.sender === 'user' 
                          ? 'bg-blue-500/20 border border-blue-400/30 text-white rounded-tr-sm' 
                          : 'bg-white/5 border border-white/10 text-cyan-50 rounded-tl-sm'
                      }`}
                    >
                      {msg.text}
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
              
              {isThinking && (
                 <motion.div 
                 initial={{ opacity: 0 }}
                 animate={{ opacity: 1 }}
                 className="flex flex-col items-start"
               >
                 <span className="text-[10px] text-white/40 uppercase tracking-widest mb-1 ml-1">J.A.R.V.I.S. • Procesando...</span>
                 <div className="p-3 bg-white/5 border border-white/10 rounded-xl rounded-tl-sm flex gap-1.5">
                   <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce"></span>
                   <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></span>
                   <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></span>
                 </div>
               </motion.div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSendMessage} className="relative mt-auto">
              <input 
                type="text" 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={isThinking}
                placeholder="Introduzca su directiva..." 
                className="w-full bg-black/30 border border-white/10 rounded-lg px-4 py-3 pr-24 text-sm text-white focus:outline-none focus:border-cyan-400/50 transition-colors placeholder:text-white/20 font-mono"
              />
              <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                <button type="button" className="p-2 text-white/30 hover:text-cyan-300 transition-colors">
                  <Mic className="w-4 h-4" />
                </button>
                <button 
                  type="submit" 
                  disabled={!input.trim() || isThinking}
                  className="p-2 bg-cyan-500/20 text-cyan-300 rounded hover:bg-cyan-500/40 transition-colors disabled:opacity-50"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </form>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;
