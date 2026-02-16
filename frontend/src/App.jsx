import React, { useState, useRef, useEffect } from "react";
import { Canvas } from "@react-three/fiber";
import { Sphere, MeshDistortMaterial, Float } from "@react-three/drei";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Cpu, Loader2, FileText, Download, CheckCircle2 } from "lucide-react";

// Point to your Render backend
const API_BASE = "https://research-agent-n30i.onrender.com";

export default function App() {
  const [file, setFile] = useState(null);
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");
  const [sections, setSections] = useState([]);
  const [citations, setCitations] = useState([]);
  
  // Ref to automatically scroll to new content
  const scrollRef = useRef(null);
  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollIntoView({ behavior: "smooth" });
  }, [sections, status]);

  const runAnalysis = async () => {
    if (!target) return alert("Please enter a target company");

    setLoading(true);
    setStatus("Initializing Agents...");
    setSections([]);
    setCitations([]);

    const formData = new FormData();
    formData.append("target_company", target);
    if (file) formData.append("annual_report", file);

    try {
      const response = await fetch(`${API_BASE}/research`, {
        method: "POST",
        body: formData,
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop(); // Keep partial line in buffer

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const data = JSON.parse(line);
            if (data.type === "status") setStatus(data.message);
            if (data.type === "section") {
              setSections((prev) => [...prev, data.data]);
            }
            if (data.type === "citations") {
              setCitations((prev) => [...prev, ...data.data]);
            }
            if (data.type === "complete") {
              setStatus("Orchestration Complete");
              setLoading(false);
            }
          } catch (e) {
            console.error("Row parse error", e);
          }
        }
      }
    } catch (err) {
      setStatus("Error connecting to research cluster");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-blue-500/30">
      {/* Dynamic 3D Background */}
      <div className="fixed inset-0 z-0 opacity-40">
        <Canvas camera={{ position: [0, 0, 5] }}>
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          <Float speed={2} rotationIntensity={1} floatIntensity={2}>
            <Sphere args={[1, 100, 200]} scale={2.2}>
              <MeshDistortMaterial color="#3b82f6" speed={3} distort={0.4} />
            </Sphere>
          </Float>
        </Canvas>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-12">
        <header className="mb-16">
          <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
            <h1 className="text-7xl font-black tracking-tighter bg-gradient-to-br from-white via-blue-400 to-emerald-400 bg-clip-text text-transparent">
              DEEP RESEARCH <span className="text-white/20">AI</span>
            </h1>
            <p className="text-slate-500 font-medium tracking-widest uppercase text-sm mt-2 flex items-center gap-2">
              <Cpu size={16} /> Autonomous Account Strategy Orchestrator
            </p>
          </motion.div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
          {/* Left Panel: Controls */}
          <aside className="lg:col-span-4 space-y-6">
            <div className="bg-slate-900/80 border border-white/5 backdrop-blur-xl p-8 rounded-3xl shadow-2xl">
              <div className="flex items-center gap-3 mb-8 text-blue-400 font-bold uppercase tracking-wider text-xs">
                <Search size={18} /> Research Parameters
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="text-[10px] text-slate-500 uppercase font-bold ml-1">Target Account</label>
                  <input 
                    value={target} 
                    onChange={(e) => setTarget(e.target.value)} 
                    placeholder="e.g. First Northern Bank" 
                    className="w-full bg-slate-800/50 border border-white/10 p-4 rounded-2xl focus:ring-2 ring-blue-500 outline-none transition-all mt-1" 
                  />
                </div>

                <div>
                  <label className="text-[10px] text-slate-500 uppercase font-bold ml-1">Internal Documents (PDF)</label>
                  <div className="relative group mt-1">
                    <input 
                      type="file" 
                      accept=".pdf" 
                      onChange={(e) => setFile(e.target.files[0])} 
                      className="absolute inset-0 opacity-0 cursor-pointer z-10" 
                    />
                    <div className="bg-slate-800/50 border-2 border-dashed border-white/10 group-hover:border-blue-500/50 p-6 rounded-2xl flex flex-col items-center gap-2 transition-all">
                      <FileText className={file ? "text-emerald-400" : "text-slate-500"} />
                      <span className="text-xs text-slate-400">{file ? file.name : "Upload Annual Report"}</span>
                    </div>
                  </div>
                </div>

                <button 
                  onClick={runAnalysis} 
                  disabled={loading} 
                  className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 py-5 rounded-2xl flex items-center justify-center gap-3 font-bold text-sm tracking-widest transition-all shadow-lg shadow-blue-500/20"
                >
                  {loading ? <Loader2 className="animate-spin" /> : <Cpu size={20} />}
                  {loading ? "AGENTS ACTIVE" : "START ANALYSIS"}
                </button>
              </div>
            </div>
            
            {status && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-center gap-3 px-6 py-4 bg-blue-500/10 border border-blue-500/20 rounded-2xl text-blue-400 text-xs font-mono">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" />
                {status}
              </motion.div>
            )}
          </aside>

          {/* Right Panel: Output */}
          <main className="lg:col-span-8">
            <AnimatePresence mode="wait">
              {sections.length > 0 ? (
                <motion.div 
                  initial={{ opacity: 0, x: 20 }} 
                  animate={{ opacity: 1, x: 0 }} 
                  className="space-y-8 pb-24"
                >
                  <div className="flex items-center justify-between border-b border-white/5 pb-6">
                    <h2 className="text-2xl font-bold flex items-center gap-3">
                      <CheckCircle2 className="text-emerald-400" /> Account Intel Report
                    </h2>
                    <div className="flex gap-2">
                      <button className="p-2 hover:bg-white/5 rounded-lg text-slate-400 transition-colors"><Download size={20}/></button>
                    </div>
                  </div>

                  {sections.map((s, i) => (
                    <motion.section 
                      key={i} 
                      initial={{ opacity: 0, y: 20 }} 
                      animate={{ opacity: 1, y: 0 }}
                      className="bg-slate-900/40 p-8 rounded-3xl border border-white/5 backdrop-blur-sm"
                    >
                      <h3 className="text-blue-400 text-[10px] uppercase font-black tracking-[0.2em] mb-4">
                        Phase 0{i+1}: {s.section_title || "Analysis Core"}
                      </h3>
                      <div className="prose prose-invert max-w-none prose-p:text-slate-300 prose-p:leading-relaxed">
                        <p>{s.section_content}</p>
                      </div>
                    </motion.section>
                  ))}

                  {citations.length > 0 && (
                    <div className="bg-slate-900/80 p-8 rounded-3xl border border-white/5">
                      <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-6">Verified Sources</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {citations.map((c, i) => (
                          <a 
                            key={i} 
                            href={c.url} 
                            target="_blank" 
                            rel="noreferrer" 
                            className="p-3 bg-white/5 rounded-xl text-[11px] text-slate-400 hover:text-white hover:bg-blue-500/20 transition-all truncate border border-transparent hover:border-blue-500/30"
                          >
                            [{c.id || i+1}] {c.title || c.url}
                          </a>
                        ))}
                      </div>
                    </div>
                  )}
                  <div ref={scrollRef} />
                </motion.div>
              ) : (
                <div className="h-[600px] border-2 border-dashed border-white/5 rounded-[40px] flex flex-col items-center justify-center text-slate-600 gap-4">
                  <div className="p-6 bg-slate-900 rounded-full animate-pulse"><Cpu size={48} /></div>
                  <p className="font-mono text-[10px] uppercase tracking-widest">System Ready for Orchestration</p>
                </div>
              )}
            </AnimatePresence>
          </main>
        </div>
      </div>
    </div>
  );
}
