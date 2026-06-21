import React, { useState, useEffect } from 'react';

interface CalendarEvent {
  id: number;
  title: string;
  description: string;
  start_time: string;
  end_time: string;
}

const CalendarWidget: React.FC = () => {
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ title: '', desc: '', time: '' });

  const fetchEvents = async () => {
    try {
      const res = await fetch('http://178.156.140.78:8080/api/calendar');
      if (res.ok) {
        const data = await res.json();
        setEvents(data.events);
      }
    } catch (error) {
      console.error("Error fetching calendar:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 60000); // Polling cada minuto
    return () => clearInterval(interval);
  }, []);

  const handleAddEvent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title || !formData.time) return;
    
    const start = new Date(formData.time);
    const end = new Date(start.getTime() + 60*60*1000); // 1 hr
    
    try {
      await fetch('http://178.156.140.78:8080/api/calendar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: formData.title,
          description: formData.desc,
          start_time: start.toISOString(),
          end_time: end.toISOString()
        })
      });
      setShowForm(false);
      setFormData({ title: '', desc: '', time: '' });
      fetchEvents();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="relative p-6 rounded-2xl bg-black/40 backdrop-blur-xl border border-cyan-500/20 shadow-[0_0_30px_rgba(0,255,255,0.1)] overflow-hidden group h-[600px] flex flex-col">
      {/* Glow Effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
      
      <div className="flex items-center justify-between mb-6 flex-shrink-0">
        <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-600 tracking-widest uppercase">
          [ CORE SYNC ] AGENDA CORPORATIVA
        </h2>
        <div className="flex items-center space-x-2">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
          </span>
          <span className="text-cyan-400 text-xs tracking-widest font-mono uppercase">Enlace Activo</span>
        </div>
      </div>

      <div className="mb-4 flex-shrink-0">
        <button onClick={() => setShowForm(!showForm)} className="px-4 py-2 bg-cyan-600/30 hover:bg-cyan-500/50 text-cyan-300 text-xs font-bold uppercase tracking-widest rounded border border-cyan-500/50 transition-colors">
          {showForm ? 'Cancelar' : '+ Agregar Evento'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleAddEvent} className="mb-6 bg-black/50 p-4 rounded border border-cyan-500/30 space-y-3 flex-shrink-0">
          <input type="text" placeholder="Título del evento" value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})} className="w-full bg-transparent border-b border-gray-600 text-white p-2 focus:outline-none focus:border-cyan-500 text-sm" required />
          <input type="text" placeholder="Descripción" value={formData.desc} onChange={e => setFormData({...formData, desc: e.target.value})} className="w-full bg-transparent border-b border-gray-600 text-white p-2 focus:outline-none focus:border-cyan-500 text-sm" />
          <input type="datetime-local" value={formData.time} onChange={e => setFormData({...formData, time: e.target.value})} className="w-full bg-transparent border-b border-gray-600 text-white p-2 focus:outline-none focus:border-cyan-500 text-sm" required />
          <button type="submit" className="w-full py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs tracking-widest uppercase rounded">Guardar</button>
        </form>
      )}

      <div className="space-y-4 overflow-y-auto flex-1 pr-2 custom-scrollbar">
        {loading ? (
          <div className="text-cyan-500/50 text-sm font-mono animate-pulse uppercase">Extrayendo datos de la red neuronal...</div>
        ) : events.length === 0 ? (
          <div className="text-gray-400 text-sm font-mono border border-dashed border-gray-600/50 p-4 rounded-lg text-center">
            No hay eventos agendados para las próximas 24 horas.
          </div>
        ) : (
          events.map((ev) => {
            const date = new Date(ev.start_time);
            return (
              <div key={ev.id} className="group/item relative overflow-hidden p-4 rounded-lg bg-gray-900/50 border border-gray-700/50 hover:border-cyan-500/50 transition-all duration-300">
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-cyan-500 to-blue-600 group-hover/item:w-2 transition-all duration-300"></div>
                <div className="pl-4">
                  <div className="flex justify-between items-start">
                    <h3 className="text-lg font-semibold text-white tracking-wide">{ev.title}</h3>
                    <div className="text-right">
                      <span className="block text-cyan-400 font-mono text-sm">
                        {date.toLocaleDateString()}
                      </span>
                      <span className="block text-gray-400 font-mono text-xs">
                        {date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                  </div>
                  <p className="mt-2 text-sm text-gray-400 font-mono border-t border-gray-800 pt-2">
                    {ev.description}
                  </p>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default CalendarWidget;
