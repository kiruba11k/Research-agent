import React, { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { Sphere, MeshDistortMaterial } from "@react-three/drei";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Cpu, Loader2, FileText } from "lucide-react";

const API_BASE = "https://research-agent-n30i.onrender.com";

export default function App() {
  const [file, setFile] = useState(null);
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [sections, setSections] = useState([]);
  const [citations, setCitations] = useState([]);

  const runAnalysis = () => {
    if (!target) {
      alert("Enter company");
      return;
    }

    setLoading(true);
    setProgress(0);
    setStatus("");
    setSections([]);
    setCitations([]);

    const formData = new FormData();
    formData.append("target_company", target);
    if (file) formData.append("annual_report", file);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", API_BASE + "/research", true);

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        setProgress(Math.round((event.loaded / event.total) * 100));
      }
    };

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 3) {
        const lines = xhr.responseText.split("\n");
        lines.forEach((line) => {
          if (line) {
            try {
              const data = JSON.parse(line);
              if (data.type === "status") setStatus(data.message);
              if (data.type === "section") setSections((prev) => [...prev, data.data]);
              if (data.type === "citations") setCitations((prev) => [...prev, data.data]);
              if (data.type === "complete") setLoading(false);
            } catch {}
          }
        });
      }
    };

    xhr.onload = () => setLoading(false);
    xhr.send(formData);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 relative overflow-hidden">
      <div className="absolute inset-0 opacity-30">
        <Canvas>
          <ambientLight />
          <Sphere args={[1, 100, 200]} scale={2.5}>
            <MeshDistortMaterial color="#3b82f6" speed={2} distort={0.4} />
          </Sphere>
        </Canvas>
      </div>

      <div className="relative max-w-5xl mx-auto px-6 py-12">
        <header className="text-center mb-16">
          <motion.h1 initial={{ y: -20 }} animate={{ y: 0 }} className="text-6xl font-black bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
            DEEP RESEARCH AI
          </motion.h1>
          <p className="text-slate-400 mt-4">Autonomous Account Orchestrator</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          <div className="lg:col-span-4">
            <div className="bg-slate-900/50 p-8 rounded-3xl">
              <div className="flex gap-3 mb-8 text-blue-400">
                <Search /> <h2>Research Portal</h2>
              </div>
              <input value={target} onChange={(e) => setTarget(e.target.value)} placeholder="Target Company" className="w-full bg-slate-800 p-4 mb-4 rounded-xl" />
              <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} className="w-full bg-slate-800 p-4 mb-4 rounded-xl" />
              <button onClick={runAnalysis} disabled={loading} className="w-full bg-blue-600 py-4 rounded-xl flex justify-center gap-2">
                {loading ? <Loader2 className="animate-spin" /> : <Cpu />}
                {loading ? "AGENTS WORKING" : "START ORCHESTRATION"}
              </button>

              {progress > 0 && (
                <div className="mt-4">
                  <div>Upload Progress: {progress}%</div>
                  <div className="w-full bg-slate-700 rounded">
                    <div className="bg-blue-500 p-1 rounded" style={{ width: progress + "%" }} />
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="lg:col-span-8 min-h-[500px]">
            <AnimatePresence>
              {sections.length > 0 || status ? (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-slate-900 p-8 rounded-3xl">
                  <div className="flex gap-2 mb-4"><FileText /> Generated Report</div>
                  {status && <div className="text-blue-400 mb-4">{status}</div>}
                  {sections.map((s, i) => (
                    <div key={i} className="mb-6">
                      <h3 className="text-xl font-bold">{s.section_title || "Section"}</h3>
                      <p>{s.section_content || JSON.stringify(s)}</p>
                    </div>
                  ))}
                  {citations.length > 0 && (
                    <div className="mt-6">
                      <h3>Sources</h3>
                      {citations.map((c, i) => (
                        <a key={i} href={c.url} target="_blank" rel="noreferrer" className="block text-green-400">{c.title || c.url}</a>
                      ))}
                    </div>
                  )}
                </motion.div>
              ) : (
                <div className="border border-white/10 rounded-3xl h-full flex items-center justify-center">Awaiting Input Data</div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}
