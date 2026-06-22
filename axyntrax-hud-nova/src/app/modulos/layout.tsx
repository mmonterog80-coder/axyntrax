import { ReactNode } from 'react';
import Link from 'next/link';
import * as Icons from 'lucide-react';

export default function ModulosLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-[#050505] text-white font-sans flex flex-col">
      <header className="sticky top-0 z-50 bg-[#0A0A0A]/80 backdrop-blur-md border-b border-white/10 px-6 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <Link href="/hud" className="text-gray-400 hover:text-cyan-400 transition-colors">
            <Icons.ArrowLeft className="w-5 h-5" />
          </Link>
          <div className="flex items-center space-x-2">
            <Icons.Hexagon className="w-6 h-6 text-cyan-500 animate-pulse" />
            <span className="font-bold tracking-widest text-lg">AXYNTRAX <span className="text-cyan-500">GLOBAL</span></span>
          </div>
        </div>
        <div className="flex space-x-6 text-sm font-medium">
          <Link href="/modulos" className="text-cyan-400 hover:text-cyan-300">Hub Principal</Link>
          <span className="text-gray-600">|</span>
          <span className="text-green-400 flex items-center"><span className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span> Sistema Operativo</span>
          {/* Indicador de Voz de Jarvis Activo */}
          <span className="text-cyan-400 flex items-center ml-4 border-l border-white/10 pl-4">
            <Icons.Mic className="w-4 h-4 mr-2" />
            Jarvis Voice Core: ONLINE
          </span>
        </div>
      </header>

      <main className="flex-1 overflow-hidden relative">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-cyan-900/20 via-[#050505] to-[#050505] pointer-events-none"></div>
        <div className="relative z-10 h-full overflow-y-auto p-6 md:p-12">
          {children}
        </div>
      </main>

      {/* Jarvis Core Audio Engine */}
      <audio autoPlay preload="auto" src="/jarvis_voice.mp3" className="hidden" />
    </div>
  );
}
