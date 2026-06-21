import React from 'react';

const ServiceCard = ({ title, desc, icon }: any) => (
  <div className="relative bg-[#06141c]/60 backdrop-blur-md border border-[#00e5ff]/30 p-6 flex flex-col rounded-xl shadow-[inset_0_0_20px_rgba(0,229,255,0.05)] hover:border-[#00e5ff]/80 hover:shadow-[0_0_25px_rgba(0,229,255,0.3)] transition-all duration-300 overflow-hidden group cursor-pointer">
    {/* Animated Corner Brackets */}
    <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-[#00e5ff] opacity-80 rounded-tl-xl transition-all duration-300 group-hover:w-12 group-hover:h-12 group-hover:border-[#10b981] shadow-[0_0_10px_#00e5ff]" />
    <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-[#00e5ff] opacity-80 rounded-br-xl transition-all duration-300 group-hover:w-12 group-hover:h-12 group-hover:border-[#10b981] shadow-[0_0_10px_#00e5ff]" />
    
    {/* Hexagon Background Pattern */}
    <div className="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_center,#00e5ff_1px,transparent_1px)] [background-size:20px_20px] group-hover:opacity-30 transition-opacity duration-500" />
    
    {/* Icon Area */}
    <div className="mb-4 mt-2 text-[#00e5ff] text-4xl group-hover:text-[#10b981] group-hover:scale-110 transition-all duration-300 drop-shadow-[0_0_10px_#00e5ff]">
      {icon}
    </div>
    
    {/* Content */}
    <h3 className="text-[#ffffff] font-mono text-lg font-bold tracking-[0.2em] mb-2 uppercase drop-shadow-[0_0_5px_#ffffff]">{title}</h3>
    <div className="w-12 h-[2px] bg-[#00e5ff] mb-4 group-hover:w-full group-hover:bg-[#10b981] transition-all duration-500 shadow-[0_0_8px_#00e5ff]" />
    <p className="text-[#00e5ff]/80 text-sm font-mono leading-relaxed">{desc}</p>
    
    {/* Status indicator */}
    <div className="absolute top-4 right-4 flex items-center gap-2">
      <span className="text-[10px] font-mono font-bold text-[#10b981] animate-pulse">ONLINE</span>
      <div className="w-2 h-2 rounded-full bg-[#10b981] shadow-[0_0_8px_#10b981] animate-pulse" />
    </div>
  </div>
);

export default function Services() {
  const services = [
    {
      title: "Desarrollo Web Full-Stack",
      desc: "Arquitectura escalable en React/Node. Interfaces inmersivas (HUDs), backend de alto rendimiento y despliegues en contenedores Docker sobre clústeres bare-metal.",
      icon: "🌐"
    },
    {
      title: "Inteligencia Artificial",
      desc: "Integración de Modelos de Lenguaje (LLMs) multimodales, agentes autónomos y redes neuronales para automatización cognitiva de extremo a extremo.",
      icon: "🧠"
    },
    {
      title: "Automatización & Bots",
      desc: "Pipelines autónomos, Bots de Telegram ultra-rápidos, scraping de mercado y orquestación de procesos (RPA) con Python.",
      icon: "🤖"
    },
    {
      title: "Seguridad Zero-Trust",
      desc: "Sistemas encriptados, bases de datos vectoriales privadas y monitoreo autónomo de intrusiones con auto-corrección de fallos en tiempo real.",
      icon: "🛡️"
    }
  ];

  return (
    <div className="w-full flex flex-col gap-6 p-2">
      <div className="flex items-center gap-4 mb-2 border-b border-[#00e5ff]/30 pb-4">
        <h2 className="text-[#00e5ff] text-xl md:text-2xl font-mono font-bold tracking-[0.4em] drop-shadow-[0_0_10px_#00e5ff] uppercase">Axyntrax Services</h2>
        <div className="flex-1 h-[1px] bg-gradient-to-r from-[#00e5ff]/80 to-transparent shadow-[0_0_10px_#00e5ff]" />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {services.map((srv, idx) => (
          <ServiceCard key={idx} {...srv} />
        ))}
      </div>
    </div>
  );
}
