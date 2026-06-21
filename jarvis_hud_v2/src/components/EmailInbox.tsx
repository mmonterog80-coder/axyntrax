import React, { useState, useEffect } from 'react';

interface EmailMsg {
  id: number;
  sender: string;
  subject: string;
  body: string;
  ai_draft_reply: string | null;
  status: string;
  received_at: string;
}

const EmailInbox: React.FC = () => {
  const [emails, setEmails] = useState<EmailMsg[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEmails = async () => {
      try {
        const res = await fetch('http://178.156.140.78:8080/api/email/inbox');
        if (res.ok) {
          const data = await res.json();
          setEmails(data.inbox);
        }
      } catch (error) {
        console.error("Error fetching emails:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchEmails();
    const interval = setInterval(fetchEmails, 30000);
    return () => clearInterval(interval);
  }, []);

  const approveReply = async (id: number) => {
    try {
      await fetch(`http://178.156.140.78:8080/api/email/send/${id}`, { method: 'POST' });
      setEmails(emails.map(e => e.id === id ? { ...e, status: 'sent' } : e));
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="relative p-6 rounded-2xl bg-black/40 backdrop-blur-xl border border-violet-500/20 shadow-[0_0_30px_rgba(139,92,246,0.1)] overflow-hidden group h-[600px] flex flex-col">
      <div className="absolute inset-0 bg-gradient-to-br from-violet-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
      
      <div className="flex items-center justify-between mb-6 flex-shrink-0">
        <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-violet-400 to-purple-600 tracking-widest uppercase">
          [ COMMS ] BANDEJA AUTÓNOMA
        </h2>
        <div className="flex items-center space-x-2">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-violet-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-violet-500"></span>
          </span>
          <span className="text-violet-400 text-xs tracking-widest font-mono uppercase">Interceptando...</span>
        </div>
      </div>

      <div className="space-y-4 overflow-y-auto flex-1 pr-2 custom-scrollbar">
        {loading ? (
          <div className="text-violet-500/50 text-sm font-mono animate-pulse uppercase">Sincronizando con nodos SMTP...</div>
        ) : emails.length === 0 ? (
          <div className="text-gray-400 text-sm font-mono border border-dashed border-gray-600/50 p-4 rounded-lg text-center">
            Bandeja limpia. Ninguna amenaza ni solicitud detectada.
          </div>
        ) : (
          emails.map((msg) => (
            <div key={msg.id} className="relative p-4 rounded-lg bg-gray-900/50 border border-gray-700/50 hover:border-violet-500/50 transition-all duration-300">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <span className="text-xs text-violet-400 font-mono tracking-widest uppercase block mb-1">De: {msg.sender}</span>
                  <h3 className="text-white font-bold">{msg.subject}</h3>
                </div>
                <span className={`text-xs px-2 py-1 rounded font-mono ${msg.status === 'sent' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'}`}>
                  {msg.status.toUpperCase()}
                </span>
              </div>
              
              <div className="text-sm text-gray-400 mb-4 line-clamp-2">
                {msg.body}
              </div>

              {msg.ai_draft_reply && msg.status !== 'sent' && (
                <div className="bg-black/50 p-3 rounded border border-violet-500/30">
                  <span className="text-xs text-cyan-400 font-mono block mb-2">🤖 Borrador de Sistema:</span>
                  <p className="text-sm text-gray-300 italic mb-3">{msg.ai_draft_reply}</p>
                  <button onClick={() => approveReply(msg.id)} className="w-full py-2 bg-violet-600 hover:bg-violet-500 text-white font-bold tracking-widest text-xs uppercase rounded transition-colors">
                    Aprobar & Enviar
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default EmailInbox;
