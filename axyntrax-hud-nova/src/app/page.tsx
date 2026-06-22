import { QuantumBackground } from "@/components/ui/quantum-bg";
import { GlassNav } from "@/components/ui/glass-nav";
import { HeroSection } from "@/components/ui/hero-section";
import { NeoCard } from "@/components/ui/neo-card";
import { Brain, Cpu, ShieldAlert, Workflow } from "lucide-react";

export default function Home() {
  const modules = [
    {
      title: "DeepSeek Core",
      description: "Clasificación de intenciones en microsegundos. Procesamiento multimodal sin latencia estructural, impulsado por L99.",
      icon: <Brain />,
      color: "#00f3ff"
    },
    {
      title: "Omni-Socket",
      description: "Motor WebSocket asíncrono para gestión de estado global, OCR en tiempo real y telemetría predictiva.",
      icon: <Workflow />,
      color: "#8b5cf6" // Purple neon
    },
    {
      title: "Quantum Security",
      description: "Protección nativa contra inyecciones SQL y ataques LLM. Cifrado cuántico de capa 7 por defecto.",
      icon: <ShieldAlert />,
      color: "#f59e0b" // Amber neon
    }
  ];

  return (
    <main className="relative min-h-screen selection:bg-cyan-l99/30 selection:text-white">
      <QuantumBackground />
      <GlassNav />
      
      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <HeroSection />

        <section id="arquitectura" className="py-32 relative">
          {/* Section Header */}
          <div className="mb-16">
            <h2 className="text-sm font-mono text-cyan-l99 tracking-[0.3em] uppercase mb-4 flex items-center gap-4">
              <span className="w-12 h-[1px] bg-cyan-l99" />
              Módulos de Sistema
            </h2>
            <h3 className="text-4xl md:text-5xl font-black uppercase tracking-tighter text-white">
              Arquitectura Base
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {modules.map((mod, i) => (
              <NeoCard 
                key={mod.title}
                title={mod.title}
                description={mod.description}
                icon={mod.icon}
                index={i}
                highlightColor={mod.color}
              />
            ))}
          </div>
        </section>
      </div>

      <footer className="border-t border-white/5 bg-[#020202] mt-20 relative z-10">
        <div className="max-w-7xl mx-auto px-6 py-12 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-4 group cursor-pointer">
            <div className="w-8 h-8 neo-btn rounded-lg flex items-center justify-center">
              <Cpu className="w-4 h-4 text-cyan-l99 group-hover:scale-110 transition-transform" />
            </div>
            <span className="text-xl font-black tracking-widest uppercase font-mono">
              Axyntrax<span className="text-cyan-l99">.AI</span>
            </span>
          </div>
          <div className="text-zinc-600 text-xs font-mono tracking-[0.2em] uppercase">
            &copy; {new Date().getFullYear()} AXYNTRAX CORP. L99 AUTHORIZED.
          </div>
        </div>
      </footer>
    </main>
  );
}
