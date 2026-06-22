import React from "react";

export default function PrivateLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-black text-cyan-400 font-mono selection:bg-cyan-500/30 overflow-hidden">
      {/* Arc Reactor Glow Background */}
      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-cyan-500/5 rounded-full blur-[150px] pointer-events-none z-0"></div>
      
      {/* Scanlines Overlay */}
      <div className="fixed inset-0 pointer-events-none z-50 opacity-10" style={{ backgroundImage: "repeating-linear-gradient(0deg, transparent, transparent 2px, #000 2px, #000 4px)" }}></div>
      
      <main className="relative z-10 w-full h-screen overflow-y-auto">
        {children}
      </main>
    </div>
  );
}
