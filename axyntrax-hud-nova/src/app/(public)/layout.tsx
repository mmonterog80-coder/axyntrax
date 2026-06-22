import Link from "next/link";
import { Shield, Brain, Rocket, ChevronRight } from "lucide-react";

export default function PublicLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 font-sans selection:bg-cyan-500/30 flex flex-col">
      <header className="fixed top-0 w-full z-50 bg-[#020617]/80 backdrop-blur-md border-b border-slate-800/50">
        <div className="container mx-auto px-6 h-20 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-8 h-8 bg-cyan-500 rounded-lg flex items-center justify-center group-hover:bg-cyan-400 transition-colors shadow-[0_0_15px_rgba(6,182,212,0.5)]">
              <Shield className="w-5 h-5 text-[#020617]" />
            </div>
            <span className="text-xl font-bold tracking-tight text-white">AXYNTRAX<span className="text-cyan-400">.</span></span>
          </Link>
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium">
            <Link href="/" className="text-slate-300 hover:text-white transition-colors">Inicio</Link>
            <Link href="/soluciones" className="text-slate-300 hover:text-white transition-colors">Soluciones</Link>
            <Link href="/contacto" className="text-slate-300 hover:text-white transition-colors">Contacto</Link>
            <Link href="/login" className="px-5 py-2.5 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20 transition-all text-white flex items-center gap-2">
              Acceso Privado <ChevronRight className="w-4 h-4" />
            </Link>
          </nav>
        </div>
      </header>
      <main className="flex-1 pt-20">
        {children}
      </main>
      <footer className="border-t border-slate-800/50 bg-[#020617] py-12">
        <div className="container mx-auto px-6 text-center text-slate-500 text-sm">
          <p>© {new Date().getFullYear()} Axyntrax Perú. Todos los derechos reservados.</p>
        </div>
      </footer>
    </div>
  );
}
