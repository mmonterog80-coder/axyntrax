"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Terminal } from "lucide-react";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);
  const router = useRouter();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (username === "GHOSTMAN" && password === "Mm40675032g@") {
      router.push("/hud");
    } else {
      setError(true);
      setTimeout(() => setError(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center font-mono selection:bg-cyan-500/30">
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md p-8 border border-slate-800 bg-[#0a0a0a] rounded-lg shadow-[0_0_50px_rgba(0,0,0,1)]"
      >
        <div className="flex justify-center mb-8">
          <div className="w-16 h-16 border-2 border-cyan-500 rounded-full flex items-center justify-center shadow-[0_0_15px_rgba(6,182,212,0.5)]">
            <Terminal className="w-8 h-8 text-cyan-400" />
          </div>
        </div>
        <h2 className="text-center text-xl font-bold text-slate-300 mb-8 uppercase tracking-widest">
          Axyntrax Protocol
        </h2>
        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <input 
              type="text" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-black border border-slate-800 text-cyan-400 px-4 py-3 focus:outline-none focus:border-cyan-500 focus:shadow-[0_0_10px_rgba(6,182,212,0.2)] transition-all uppercase"
              placeholder="IDENTIFIER"
              autoComplete="off"
              spellCheck="false"
            />
          </div>
          <div>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-black border border-slate-800 text-cyan-400 px-4 py-3 focus:outline-none focus:border-cyan-500 focus:shadow-[0_0_10px_rgba(6,182,212,0.2)] transition-all"
              placeholder="PASSPHRASE"
            />
          </div>
          {error && <p className="text-red-500 text-sm text-center font-bold animate-pulse">ACCESS DENIED</p>}
          <button type="submit" className="w-full bg-cyan-900/30 border border-cyan-500/50 text-cyan-400 font-bold py-3 hover:bg-cyan-500 hover:text-black transition-colors uppercase tracking-widest">
            Initialize
          </button>
        </form>
      </motion.div>
    </div>
  );
}
