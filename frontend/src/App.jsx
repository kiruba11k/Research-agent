import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial } from '@react-three/drei';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Cpu, Download, Loader2, FileText } from 'lucide-react';
import axios from 'axios';

const API_BASE = "https://research-agent-n30i.onrender.com"; // Change after deployment

export default function App() {
  const [file, setFile] = useState(null);
  const [target, setTarget] = useState('');
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [reportId, setReportId] = useState(null);

const runAnalysis = async () => {

  setLoading(true);

  try {

    const formData = new FormData();

    formData.append("target", target);

    formData.append("mine", "Speridian");

    if(file)
      formData.append("file", file);

    const res = await axios.post(

      `${API_BASE}/generate`,

      formData,

      {

        headers:

        {

          "Content-Type":

          "multipart/form-data"

        }

      }

    );

    setReport(res.data.report);

    setReportId(res.data.id);

  }

  catch(e)

  {

    alert("failed");

  }

  setLoading(false);

};


  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans relative overflow-hidden">
      {/* 3D Background Element */}
      <div className="absolute inset-0 z-0 opacity-30">
        <Canvas>
          <ambientLight intensity={1} />
          <Sphere args={[1, 100, 200]} scale={2.5}>
            <MeshDistortMaterial color="#3b82f6" speed={2} distort={0.4} />
          </Sphere>
        </Canvas>
      </div>

      <div className="relative z-10 max-w-5xl mx-auto px-6 py-12">
        <header className="mb-16 text-center">
          <motion.h1 initial={{y:-20}} animate={{y:0}} className="text-6xl font-black tracking-tighter bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
            DEEP RESEARCH AI
          </motion.h1>
          <p className="text-slate-400 mt-4 uppercase tracking-[0.3em] text-sm">Autonomous Account Orchestrator</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          {/* Controls */}
          <div className="lg:col-span-4">
            <div className="bg-slate-900/50 backdrop-blur-xl border border-white/10 p-8 rounded-3xl shadow-2xl">
              <div className="flex items-center gap-3 mb-8 text-blue-400">
                <Search size={24} />
                <h2 className="text-xl font-bold">Research Portal</h2>
              </div>
              <input 
  value={target}
  onChange={(e)=>setTarget(e.target.value)}
  placeholder="Target Company Name..."
  className="w-full bg-slate-800 border border-white/5 rounded-xl p-4 mb-4"
/>

<input
  type="file"
  accept=".pdf"
  onChange={(e)=>setFile(e.target.files[0])}
  className="w-full bg-slate-800 border border-white/5 rounded-xl p-4 mb-4"
/>

              <button 
                onClick={runAnalysis} disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-500 py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all active:scale-95"
              >
                {loading ? <Loader2 className="animate-spin"/> : <Cpu size={20}/>}
                {loading ? "AGENTS WORKING..." : "START ORCHESTRATION"}
              </button>
            </div>
          </div>

          {/* Results Area */}
          <div className="lg:col-span-8 min-h-[500px]">
            <AnimatePresence>
              {report ? (
                <motion.div initial={{opacity:0, x:20}} animate={{opacity:1, x:0}} className="bg-slate-900/80 backdrop-blur-md border border-white/10 rounded-3xl p-8 h-full">
                  <div className="flex justify-between items-center mb-6 border-b border-white/10 pb-4">
                    <h3 className="text-2xl font-bold flex items-center gap-2"><FileText className="text-emerald-400"/> Generated Report</h3>
                    <button 
                      onClick={()=>window.open(`${API_BASE}/download/${reportId}`)}
                      className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 px-4 py-2 rounded-lg text-sm font-bold transition-all"
                    >
                      <Download size={16}/> DOWNLOAD PDF
                    </button>
                  </div>
                  <div className="prose prose-invert max-w-none overflow-y-auto max-h-[600px] text-slate-300">
                    <pre className="whitespace-pre-wrap font-sans leading-relaxed">{report}</pre>
                  </div>
                </motion.div>
              ) : (
                <div className="border-2 border-dashed border-white/5 rounded-3xl h-full flex items-center justify-center text-slate-600 uppercase tracking-widest">
                  Awaiting Input Data
                </div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}
