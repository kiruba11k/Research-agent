import { Canvas } from '@react-three/fiber';
import { Points, PointMaterial } from '@react-three/drei';
import { motion } from 'framer-motion';
import { Cpu, Search, Download } from 'lucide-react';

export default function App() {
  // Use state to track targetCompany and report
  // Use axios to POST to your Render backend URL
  return (
    <div className="h-screen bg-black text-white relative">
      <div className="absolute inset-0 opacity-30">
        <Canvas><Points>{/* 3D Stars Logic Here */}</Points></Canvas>
      </div>
      <div className="relative z-10 flex items-center justify-center h-full">
        <motion.div className="bg-white/5 backdrop-blur-xl border border-white/10 p-10 rounded-3xl">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-6">DEEP RESEARCH AGENT</h1>
          <input className="w-full bg-transparent border-b border-white/20 p-2 mb-6 outline-none" placeholder="Target Company..." />
          <button className="w-full bg-cyan-600 py-3 rounded-xl font-bold flex items-center justify-center gap-2">
            <Cpu size={20} /> RUN ANALYSIS
          </button>
        </motion.div>
      </div>
    </div>
  );
}
