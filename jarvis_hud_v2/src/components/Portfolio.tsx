import React from 'react';

const ProjectCard = ({ title, category, img, delay }: any) => (
  <div className="relative group overflow-hidden rounded-xl bg-[#06141c]/80 border border-[#00e5ff]/30 aspect-video shadow-[0_0_15px_rgba(0,229,255,0.1)] cursor-pointer" style={{ animationDelay: delay }}>
    {/* Placeholder Image (Neon Wireframe style) */}
    <div className="absolute inset-0 bg-[#030b10] flex items-center justify-center opacity-80 group-hover:opacity-40 transition-opacity duration-500">
      <div className="w-[80%] h-[80%] border border-[#00e5ff]/20 flex items-center justify-center relative overflow-hidden">
        <div className="absolute inset-0 bg-[linear-gradient(45deg,transparent_45%,#00e5ff_50%,transparent_55%)] opacity-10 animate-[translate_3s_linear_infinite]" style={{ backgroundSize: '200% 200%' }} />
        <span className="text-4xl opacity-50 drop-shadow-[0_0_10px_#00e5ff]">{img}</span>
      </div>
    </div>
    
    {/* Scanline Effect */}
    <div className="absolute inset-0 bg-[linear-gradient(to_bottom,transparent_50%,rgba(0,229,255,0.05)_50%)] [background-size:100%_4px] pointer-events-none opacity-50" />
    
    {/* Overlay Info */}
    <div className="absolute inset-x-0 bottom-0 p-6 bg-gradient-to-t from-[#030b10] to-transparent transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
      <div className="text-[10px] font-mono text-[#10b981] font-bold tracking-widest mb-1 opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-100 drop-shadow-[0_0_5px_#10b981]">{category}</div>
      <h3 className="text-[#ffffff] font-mono text-xl font-bold tracking-wider drop-shadow-[0_0_8px_#ffffff]">{title}</h3>
      <div className="w-0 h-[2px] bg-[#00e5ff] mt-3 group-hover:w-full transition-all duration-500 shadow-[0_0_10px_#00e5ff]" />
    </div>
    
    {/* Frame corners */}
    <div className="absolute top-2 left-2 w-4 h-4 border-t-2 border-l-2 border-[#00e5ff] opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
    <div className="absolute top-2 right-2 w-4 h-4 border-t-2 border-r-2 border-[#00e5ff] opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
  </div>
);

export default function Portfolio() {
  const projects = [
    { title: "SISTEMA C.O.R.E. (TELEGRAM)", category: "AUTOMATIZACIÓN IA", img: "💬", delay: "0s" },
    { title: "AXYNTRAX HUD V2", category: "FRONTEND REACT", img: "🌐", delay: "0.2s" },
    { title: "MOTOR VECTORIAL DE MEMORIA", category: "DATABASE", img: "🗄️", delay: "0.4s" },
    { title: "RED DE ENJAMBRE MULTI-AGENTE", category: "IA DISTRIBUIDA", img: "⚡", delay: "0.6s" }
  ];

  return (
    <div className="w-full flex flex-col gap-6 p-2 mt-8">
      <div className="flex items-center gap-4 mb-4 border-b border-[#00e5ff]/30 pb-4">
        <h2 className="text-[#ffffff] text-xl md:text-2xl font-mono font-bold tracking-[0.4em] drop-shadow-[0_0_10px_#ffffff] uppercase">Casos de Éxito</h2>
        <div className="flex-1 h-[1px] bg-gradient-to-r from-[#ffffff]/80 to-transparent shadow-[0_0_10px_#ffffff]" />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {projects.map((proj, idx) => (
          <ProjectCard key={idx} {...proj} />
        ))}
      </div>
    </div>
  );
}
