import React, { useState, useEffect } from 'react';
import { 
  Cpu, Circle, RefreshCw, Bot, Boxes, CircleAlert, TriangleAlert, 
  DollarSign, ScrollText, Crown, Brain, BookOpen, Target, Clock, FileText,
  Sparkles, Power, Flame, Network, CheckCircle2, Lock, Activity, Database
} from 'lucide-react';

// API Configuration
const API_BASE = ''; // En prod, usa rutas relativas al mismo dominio proxy

export default function App() {
  const [activeTab, setActiveTab] = useState('comando');
  const [token, setToken] = useState(localStorage.getItem('jarvis_token') || '');
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('jarvis_token'));
  const [authInput, setAuthInput] = useState('');
  
  // States para data real
  const [telemetry, setTelemetry] = useState<any>({ uptime_human: '--:--:--' });
  const [systemInfo, setSystemInfo] = useState<any>({ cpu_percent: 0, ram_percent: 0 });
  const [iasStatus, setIasStatus] = useState<any>({ total: 0, online: 0, ias: [] });
  const [skills, setSkills] = useState<any[]>([]);
  
  // Uptime local ticker (hasta el prox sync)
  const [localUptime, setLocalUptime] = useState('--:--:--');

  useEffect(() => {
    if (!isAuthenticated) return;

    const fetchData = async () => {
      try {
        const headers = { 'Authorization': `Bearer ${token}` };
        
        // Health (public pero útil para uptime)
        const resHealth = await fetch(`${API_BASE}/health`);
        if (resHealth.ok) {
           const d = await resHealth.json();
           setTelemetry(d);
           setLocalUptime(d.uptime_human);
        }

        // System Telemetry
        const resSys = await fetch(`${API_BASE}/api/telemetry/system`, { headers });
        if (resSys.ok) setSystemInfo(await resSys.json());

        // IAs Status
        const resIas = await fetch(`${API_BASE}/api/ias/status`, { headers });
        if (resIas.ok) setIasStatus(await resIas.json());

        // Skills
        const resSkills = await fetch(`${API_BASE}/api/skills`, { headers });
        if (resSkills.ok) {
           const d = await resSkills.json();
           setSkills(d.skills || []);
        } else if (resSkills.status === 401 || resSkills.status === 403) {
           handleLogout();
        }

      } catch (err) {
        console.error("Fetch error:", err);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, [isAuthenticated, token]);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem('jarvis_token', authInput);
    setToken(authInput);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('jarvis_token');
    setToken('');
    setIsAuthenticated(false);
  };

  const tabs = [
    { id: 'comando', label: 'Comando', icon: Crown },
    { id: 'skills', label: 'Skills', icon: Boxes },
    { id: 'agentes', label: 'Agentes', icon: Bot },
    { id: 'concilio', label: 'Concilio', icon: Brain },
    { id: 'memoria', label: 'Memoria', icon: BookOpen },
    { id: 'objetivos', label: 'Objetivos', icon: Target },
    { id: 'ciclos', label: 'Ciclos', icon: Clock },
    { id: 'reportes', label: 'Reportes', icon: FileText },
    { id: 'constitucion', label: 'Constitución', icon: ScrollText },
  ];

  if (!isAuthenticated) {
    return (
      <div className="jarvis-shell jarvis-grid-bg min-h-screen flex items-center justify-center font-sans">
        <div className="jarvis-panel border border-jarvis-border p-8 rounded-lg max-w-sm w-full backdrop-blur text-center">
          <div className="mx-auto w-16 h-16 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center mb-6">
            <Lock className="h-8 w-8 text-cyan-400" />
          </div>
          <h1 className="font-mono text-xl font-bold mb-2">AUTH REQUIRED</h1>
          <p className="text-xs text-slate-400 mb-6">Conexión cifrada a la red AXYNTRAX</p>
          <form onSubmit={handleLogin} className="space-y-4">
            <input 
              type="password" 
              value={authInput}
              onChange={e => setAuthInput(e.target.value)}
              placeholder="API SECRET"
              className="w-full bg-[#0b1121] border border-jarvis-border rounded-md px-4 py-2 text-sm text-center tracking-[0.2em] focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50"
            />
            <button type="submit" className="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-md text-sm font-medium transition-all bg-cyan-500/15 border border-cyan-500/40 text-cyan-200 hover:bg-cyan-500/25">
              INICIAR CONEXIÓN
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="jarvis-shell jarvis-grid-bg min-h-screen flex flex-col font-sans">
      <header className="border-b border-jarvis-border bg-jarvis-panel/60 backdrop-blur sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3 min-w-0">
            <div className="relative">
              <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-cyan-500/20 to-amber-500/20 border border-cyan-500/40 flex items-center justify-center">
                <Cpu className="h-5 w-5 text-cyan-300" />
              </div>
              <div className="absolute -top-0.5 -right-0.5 h-2.5 w-2.5 rounded-full bg-green-400 jarvis-pulse"></div>
            </div>
            <div className="min-w-0">
              <h1 className="font-mono text-lg font-bold tracking-tight">JARVIS <span className="text-cyan-400">AX</span></h1>
              <p className="text-[10px] text-slate-500 uppercase tracking-widest -mt-0.5">CEO Orquestador · v1.0</p>
            </div>
          </div>
          
          <div className="hidden md:flex items-center gap-2 text-xs font-mono text-slate-400">
            <span className="flex items-center gap-1.5 text-green-400">
              <Circle className="h-2 w-2 fill-current" /> ONLINE {iasStatus.online}/{iasStatus.total}
            </span>
            <div className="h-4 w-px bg-jarvis-border"></div>
            <span>{iasStatus.total} agentes</span>
            <div className="h-4 w-px bg-jarvis-border"></div>
            <span className="text-amber-300">$0</span>
            <div className="h-4 w-px bg-jarvis-border"></div>
            <span>uptime {localUptime}</span>
          </div>
          
          <button onClick={handleLogout} className="h-8 px-3 rounded-md flex items-center gap-1.5 text-sm text-slate-300 hover:text-red-400 hover:bg-red-500/10 transition-all border border-transparent">
            <Power className="h-4 w-4" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6">
        {/* Metric Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          <MetricCard title="Agentes Activos" value={String(iasStatus.online || 0)} icon={Bot} colorClass="text-violet-300" />
          <MetricCard title="Skills Activas" value={String(skills.length || 0)} icon={Boxes} colorClass="text-emerald-300" />
          <MetricCard title="CPU" value={`${systemInfo.cpu_percent || 0}%`} icon={Activity} colorClass="text-amber-300" />
          <MetricCard title="RAM" value={`${systemInfo.ram_percent || 0}%`} icon={Database} colorClass="text-cyan-300" />
          <MetricCard title="Aprobaciones" value="0" icon={CircleAlert} colorClass="text-orange-300" />
          <MetricCard title="Alertas" value="0" icon={TriangleAlert} colorClass="text-red-300" />
        </div>

        {/* Tabs */}
        <div className="flex flex-col gap-2 mt-6">
          <div className="jarvis-panel grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-9 w-full gap-1 p-1 rounded-lg overflow-x-auto jarvis-scroll">
            {tabs.map(tab => {
              const isActive = activeTab === tab.id;
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center justify-center gap-1.5 py-2 text-[11px] font-medium rounded-md transition-all
                    ${isActive ? 'bg-cyan-500/15 text-cyan-300 shadow-sm border border-cyan-500/30' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-300 border border-transparent'}`}
                >
                  <Icon className="h-3.5 w-3.5" />
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              )
            })}
          </div>

          {/* Tab Content */}
          <div className="mt-4 flex-1">
            {activeTab === 'comando' && (
              <div className="grid lg:grid-cols-2 gap-4">
                <div className="space-y-4">
                  {/* Protocolo de Activación */}
                  <div className="jarvis-panel border border-jarvis-border rounded-lg overflow-hidden flex flex-col">
                    <div className="border-b border-jarvis-border p-4 flex items-center justify-between bg-black/20">
                      <div className="flex items-center gap-2">
                        <Crown className="h-4 w-4 text-amber-400" />
                        <h2 className="font-mono text-sm font-semibold">PROTOCOLO DE ACTIVACIÓN</h2>
                      </div>
                      <span className="text-[10px] text-amber-300 border border-amber-500/40 px-2 py-0.5 rounded-md font-medium">v1.0</span>
                    </div>
                    <div className="p-4">
                      <p className="text-xs text-slate-400 mb-3">
                        Dispara el prompt maestro. JARVIS generará 5 entregables en paralelo: presentación, inventario, plan 24h, dashboard y 10 preguntas críticas.
                      </p>
                      <button className="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-md text-sm font-medium transition-all bg-amber-500/15 border border-amber-500/40 text-amber-200 hover:bg-amber-500/25 hover:text-amber-100 shadow-sm">
                        <Sparkles className="h-4 w-4" />
                        Activar JARVIS v1.0
                      </button>
                    </div>
                  </div>

                  {/* Auto-Delegación */}
                  <div className="jarvis-panel border border-jarvis-border rounded-lg overflow-hidden flex flex-col">
                    <div className="border-b border-jarvis-border p-4 flex items-center gap-2 bg-black/20">
                      <Network className="h-4 w-4 text-cyan-400" />
                      <h2 className="font-mono text-sm font-semibold">AUTO-DELEGACIÓN</h2>
                    </div>
                    <div className="p-4">
                      <p className="text-xs text-slate-400 mb-2">
                        Describe una tarea. JARVIS rutea al mejor agente según especialidad + performance + costo.
                      </p>
                      <textarea 
                        className="w-full min-h-[64px] bg-[#0b1121] border border-jarvis-border rounded-md px-3 py-2 text-sm text-slate-100 placeholder:text-slate-600 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 resize-none mb-3"
                        placeholder="ej: Diseñar landing page con hero, form de lead capture y testimonios"
                        rows={2}
                      ></textarea>
                      <button className="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-md text-sm font-medium transition-all bg-cyan-500/15 border border-cyan-500/40 text-cyan-200 hover:bg-cyan-500/25 shadow-sm opacity-50 cursor-not-allowed">
                        <Bot className="h-4 w-4" />
                        Delegar tarea
                      </button>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  {/* Cola de Aprobación */}
                  <div className="jarvis-panel border border-jarvis-border rounded-lg overflow-hidden flex flex-col h-[320px]">
                    <div className="border-b border-jarvis-border p-4 flex items-center justify-between bg-black/20 shrink-0">
                      <div className="flex items-center gap-2">
                        <CircleAlert className="h-4 w-4 text-amber-400" />
                        <h2 className="font-mono text-sm font-semibold">COLA DE APROBACIÓN (LEVEL 3)</h2>
                      </div>
                      <span className="text-[10px] text-amber-300 border border-amber-500/40 px-2 py-0.5 rounded-md font-medium">0 PENDIENTES</span>
                    </div>
                    <div className="flex-1 overflow-y-auto jarvis-scroll flex items-center justify-center">
                      <div className="text-center text-xs text-slate-500">
                        <CheckCircle2 className="h-6 w-6 text-green-500/60 mx-auto mb-2" />
                        Sin solicitudes pendientes
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'skills' && (
              <div className="space-y-4">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-mono font-bold text-slate-200">SKILLS DEL ORQUESTADOR</h2>
                  <div className="text-xs text-slate-400">{skills.length} Habilidades Cargadas</div>
                </div>
                {skills.length === 0 ? (
                   <div className="jarvis-panel border border-jarvis-border rounded-lg p-12 text-center text-slate-500">
                     Cargando skills...
                   </div>
                ) : (
                  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {skills.map(skill => (
                      <div key={skill.id} className="jarvis-panel border border-jarvis-border rounded-lg p-4 flex flex-col hover:border-cyan-500/30 transition-all">
                         <div className="flex justify-between items-start mb-2">
                           <h3 className="font-mono font-bold text-cyan-300">{skill.name}</h3>
                           <span className="text-[10px] uppercase border border-jarvis-border px-1.5 py-0.5 rounded text-slate-400">{skill.tier}</span>
                         </div>
                         <p className="text-xs text-slate-400 flex-1 mb-4">{skill.description}</p>
                         <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono">
                           <span>Agt: {skill.assigned_agent}</span>
                           <span>Pri: {skill.priority}</span>
                         </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'agentes' && (
              <div className="space-y-4">
                <h2 className="text-lg font-mono font-bold text-slate-200">AGENTES ACTIVOS</h2>
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {iasStatus.ias && iasStatus.ias.map((ia: any) => (
                    <div key={ia.id} className="jarvis-panel border border-jarvis-border rounded-lg p-4 flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className={`h-2 w-2 rounded-full ${ia.estado === 'online' ? 'bg-green-400 jarvis-pulse' : 'bg-slate-500'}`}></div>
                        <span className="font-mono text-sm">{ia.nombre}</span>
                      </div>
                      <span className="text-[10px] text-slate-500 uppercase">{ia.estado}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {['concilio','memoria','objetivos','ciclos','reportes','constitucion'].includes(activeTab) && (
              <div className="jarvis-panel border border-jarvis-border rounded-lg p-12 text-center text-slate-500 flex flex-col items-center justify-center">
                <span className="text-xl mb-2">Módulo {activeTab.toUpperCase()}</span>
                <span className="text-sm">Enlace neuronal en establecimiento...</span>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="mt-auto border-t border-jarvis-border bg-jarvis-panel/60 backdrop-blur shrink-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between gap-3 text-[10px] font-mono text-slate-500">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              JARVIS AX v1.0 · CEO Orquestador
            </span>
            <span className="hidden sm:inline">·</span>
            <span className="hidden sm:inline">{iasStatus.online} agentes activos</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="hidden sm:inline">sync: ok</span>
            <span className="text-slate-400 font-semibold tracking-widest">AXYNTRAX</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

interface MetricCardProps {
  title: string;
  value: string;
  icon: React.ElementType;
  colorClass: string;
}

function MetricCard({ title, value, icon: Icon, colorClass }: MetricCardProps) {
  return (
    <div className="bg-jarvis-panel/80 text-white flex flex-col gap-6 border border-jarvis-border shadow-sm p-3 rounded-lg backdrop-blur hover:border-cyan-500/30 transition-colors">
      <div className="flex items-center justify-between">
        <div className="text-[10px] uppercase tracking-wider text-slate-500">{title}</div>
        <span className={colorClass}>
          <Icon className="h-4 w-4" />
        </span>
      </div>
      <div className={`mt-1 text-xl font-bold font-mono ${colorClass}`}>
        {value}
      </div>
    </div>
  );
}
