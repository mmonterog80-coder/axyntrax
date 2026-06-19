import React, { useState, useEffect } from 'react';
import { Bot, MessageSquare, ShieldCheck, Zap, Activity, Users, DollarSign, Calendar, Mail, Server, Eye, CheckCircle2 } from 'lucide-react';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState('chat'); // chat, calendar, mail, swarm

  const [messages, setMessages] = useState([
    { id: 1, type: 'user', text: 'Me interesa la integración de IA para mi e-commerce.', time: '10:01 AM', sender: '+51 987 654 321' },
    { id: 2, type: 'ai', text: '¡Excelente! Nuestro sistema AXYNTRAX se conecta con Shopify y WooCommerce. ¿Qué plataforma utiliza?', time: '10:01 AM', sender: 'SalesBot' }
  ]);

  const swarmStatus = [
    { id: 'zia', name: 'Z.IA', role: 'Lead Gen / Frontend', status: 'active', desc: 'Gestionando interfaz visual y leads B2B.' },
    { id: 'gemini', name: 'Gemini', role: 'Estrategia Cognitiva', status: 'thinking', desc: 'Analizando intención de compra del cliente.' },
    { id: 'deepseek', name: 'DeepSeek', role: 'Lógica / Código', status: 'active', desc: 'Verificando estructura de payload.' },
    { id: 'sentinel', name: 'Sentinel (Ernie)', role: 'Auditoría / Seguridad', status: 'idle', desc: 'Esperando respuesta generada para auditar.' },
    { id: 'qwen', name: 'Qwen', role: 'BD / Despliegue', status: 'idle', desc: 'En espera de nuevas órdenes en Supabase.' },
    { id: 'jarvis', name: 'JARVIS', role: 'Orquestador Core', status: 'active', desc: 'Sincronizando flujos entre agentes.' }
  ];

  const calendarEvents = [
    { id: 1, title: 'Demo AXYNTRAX - Cliente VIP', time: '14:00 - 15:00', type: 'meeting' },
    { id: 2, title: 'Revisión de Seguridad Sentinel', time: '16:00 - 16:30', type: 'internal' },
    { id: 3, title: 'Cierre de Venta (Shopify)', time: '17:00 - 17:45', type: 'meeting' }
  ];

  const emails = [
    { id: 1, sender: 'soporte@axyntrax.com', subject: 'Alerta de Infraestructura', preview: 'El servidor Railway fue parcheado...', time: '10:30 AM', read: false },
    { id: 2, sender: 'leads@axyntrax.com', subject: 'Nuevo Lead Capturado', preview: 'El SalesBot ha agendado una llamada...', time: '09:15 AM', read: true }
  ];

  // Simular conexión real al Backend en Railway
  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await fetch('https://jarvis-ax-cloud-production.up.railway.app/health');
        if (response.ok) {
          console.log('[Z.IA] Enlace seguro establecido con AXYNTRAX Railway Cloud.');
        }
      } catch (error) {
        console.warn('[Z.IA] Intentando reconexión a Railway...', error);
      }
    };
    checkConnection();
    // Poll every 30s to keep it alive
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard-container">
      
      {/* Sidebar: Navigation & Metrics */}
      <aside className="sidebar-grid" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        
        {/* Branding */}
        <div className="glass-panel" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'var(--accent-blue)', padding: '10px', borderRadius: '12px' }}>
            <Zap size={24} color="#000" />
          </div>
          <div>
            <h2 style={{ margin: 0 }} className="text-gradient">AXYNTRAX</h2>
            <div className="subtitle">HUD Universal (Z.IA)</div>
          </div>
        </div>

        {/* Navigation Menu */}
        <div className="glass-panel">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <button className={`nav-btn ${activeTab === 'chat' ? 'active' : ''}`} onClick={() => setActiveTab('chat')}>
              <MessageSquare size={18} /> SalesBot Chat
            </button>
            <button className={`nav-btn ${activeTab === 'calendar' ? 'active' : ''}`} onClick={() => setActiveTab('calendar')}>
              <Calendar size={18} /> Calendario IA
            </button>
            <button className={`nav-btn ${activeTab === 'mail' ? 'active' : ''}`} onClick={() => setActiveTab('mail')}>
              <Mail size={18} /> Correo (Inbox)
            </button>
            <button className={`nav-btn ${activeTab === 'swarm' ? 'active' : ''}`} onClick={() => setActiveTab('swarm')}>
              <Server size={18} /> Enjambre (IAs)
            </button>
          </div>
        </div>

        {/* Metrics */}
        <div className="glass-panel" style={{ flex: 1 }}>
          <h3 style={{ fontSize: '1rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Activity size={18} className="text-gradient" /> Live Metrics
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="subtitle" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Users size={14}/> Active Chats</span>
              <span style={{ fontWeight: '600', fontSize: '1.2rem' }}>14</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="subtitle" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><ShieldCheck size={14}/> Conversion Rate</span>
              <span style={{ fontWeight: '600', fontSize: '1.2rem', color: 'var(--accent-green)' }}>28.5%</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '1rem', borderTop: '1px solid var(--glass-border)' }}>
              <span className="subtitle" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><DollarSign size={14}/> Est. Revenue</span>
              <span style={{ fontWeight: '700', fontSize: '1.5rem', color: 'var(--accent-blue)' }}>$4,250</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        
        <header className="glass-panel" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 2rem' }}>
          <h1 style={{ fontSize: '1.5rem', margin: 0 }}>
            {activeTab === 'chat' && 'Centro de Comunicaciones (SalesBot)'}
            {activeTab === 'calendar' && 'Gestión de Agenda (JARVIS)'}
            {activeTab === 'mail' && 'Bandeja de Entrada Inteligente'}
            {activeTab === 'swarm' && 'Monitor del Enjambre de IAs'}
          </h1>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <div className="status-indicator">
              <span className="status-dot active"></span>
              <span className="subtitle" style={{ color: 'var(--accent-green)' }}>Conectado a: https://jarvis-ax-cloud-production.up.railway.app</span>
            </div>
            <div className="status-indicator">
              <span className="status-dot thinking"></span>
              <span className="subtitle" style={{ color: 'var(--accent-purple)' }}>Z.IA Watchdog Active</span>
            </div>
          </div>
        </header>

        {/* Tab Contents */}
        <div style={{ marginTop: '2rem', flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          
          {/* CHAT TAB */}
          {activeTab === 'chat' && (
            <div className="glass-panel" style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {messages.map((msg) => (
                <div key={msg.id} className={`message-bubble ${msg.type}`}>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '5px', display: 'flex', justifyContent: 'space-between' }}>
                    <span>{msg.sender}</span>
                    <span>{msg.time}</span>
                  </div>
                  <div>{msg.text}</div>
                </div>
              ))}
            </div>
          )}

          {/* CALENDAR TAB */}
          {activeTab === 'calendar' && (
            <div className="glass-panel" style={{ flex: 1, padding: '2rem' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
                {calendarEvents.map(ev => (
                  <div key={ev.id} className="glass-panel" style={{ background: 'rgba(255,255,255,0.02)', borderLeft: `4px solid ${ev.type === 'meeting' ? 'var(--accent-blue)' : 'var(--accent-purple)'}` }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                      <h3 style={{ margin: 0, fontSize: '1.1rem' }}>{ev.title}</h3>
                      <Calendar size={18} color="var(--accent-blue)" />
                    </div>
                    <span className="subtitle" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Activity size={14} /> {ev.time}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* MAIL TAB */}
          {activeTab === 'mail' && (
            <div className="glass-panel" style={{ flex: 1, padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {emails.map(email => (
                <div key={email.id} className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', background: email.read ? 'rgba(255,255,255,0.01)' : 'rgba(0, 212, 255, 0.05)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ fontWeight: email.read ? 'normal' : 'bold', color: 'var(--text-bright)' }}>{email.sender}</span>
                    <span className="subtitle">{email.time}</span>
                  </div>
                  <h4 style={{ margin: 0, color: 'var(--accent-blue)' }}>{email.subject}</h4>
                  <p className="subtitle" style={{ margin: 0 }}>{email.preview}</p>
                </div>
              ))}
            </div>
          )}

          {/* SWARM TAB */}
          {activeTab === 'swarm' && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '1.5rem', overflowY: 'auto' }}>
              {swarmStatus.map(agent => (
                <div key={agent.id} className="glass-panel agent-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <Bot size={24} color={agent.status === 'active' ? 'var(--accent-green)' : agent.status === 'thinking' ? 'var(--accent-purple)' : 'var(--text-dim)'} />
                      <h3 style={{ margin: 0 }}>{agent.name}</h3>
                    </div>
                    <span className={`status-dot ${agent.status}`}></span>
                  </div>
                  <div className="subtitle" style={{ borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.5rem' }}>
                    {agent.role}
                  </div>
                  <div style={{ flex: 1, display: 'flex', alignItems: 'center' }}>
                    <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--text-bright)', lineHeight: '1.5' }}>
                      {agent.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}

        </div>
      </main>

      <style dangerouslySetInnerHTML={{__html: `
        .nav-btn {
          display: flex;
          align-items: center;
          gap: 10px;
          width: 100%;
          background: transparent;
          border: 1px solid transparent;
          color: var(--text-dim);
          padding: 12px 16px;
          border-radius: 8px;
          cursor: pointer;
          text-align: left;
          font-family: inherit;
          font-size: 1rem;
          transition: all 0.3s ease;
        }
        .nav-btn:hover {
          background: rgba(255,255,255,0.05);
          color: var(--text-bright);
        }
        .nav-btn.active {
          background: rgba(0, 212, 255, 0.1);
          border: 1px solid rgba(0, 212, 255, 0.2);
          color: var(--accent-blue);
          box-shadow: 0 0 15px rgba(0, 212, 255, 0.05);
        }
        .agent-card {
          transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .agent-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 10px 30px rgba(0, 212, 255, 0.1);
        }
      `}} />
    </div>
  );
}

export default App;
