import React from "react";
import { motion } from "framer-motion";
import { ExternalLink, ShieldCheck } from "lucide-react";

/**
 * Sub-component for individual source links
 * with a hover animation and consistent styling.
 */
const CitationItem = ({ citation }) => (
  <motion.a
    href={citation.url}
    target="_blank"
    rel="noopener noreferrer"
    whileHover={{ x: 5 }}
    className="group flex items-start gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors border border-transparent hover:border-white/10"
  >
    <span className="text-[10px] font-bold bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded border border-blue-500/30 mt-0.5">
      {citation.id}
    </span>
    <div className="flex flex-col overflow-hidden">
      <span className="text-sm text-slate-300 group-hover:text-white truncate font-medium">
        {citation.title || "View Source"}
      </span>
      <span className="text-[10px] text-slate-500 truncate">
        {citation.url}
      </span>
    </div>
    <ExternalLink size={12} className="ml-auto text-slate-500 group-hover:text-blue-400 shrink-0 mt-1" />
  </motion.a>
);

export default function SectionCard({ title, data }) {
  // Graceful handling if data hasn't loaded yet
  if (!data) return null;

  const confidencePercentage = Math.round((data.confidence || 0) * 100);

  return (
    <div className="bg-slate-900/50 border border-white/10 rounded-2xl overflow-hidden backdrop-blur-sm mb-6">
      {/* Header Area */}
      <div className="px-6 py-4 border-b border-white/5 bg-white/5 flex justify-between items-center">
        <h3 className="text-lg font-semibold text-white tracking-tight">
          {title}
        </h3>
        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 border border-white/10">
          <ShieldCheck size={14} className={confidencePercentage > 80 ? "text-emerald-400" : "text-amber-400"} />
          <span className="text-xs font-medium text-slate-300">
            {confidencePercentage}% Confidence
          </span>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-6">
        <div className="prose prose-invert max-w-none text-slate-300 leading-relaxed text-sm lg:text-base">
          {data.content}
        </div>

        {/* Citations Section */}
        {data.citations && data.citations.length > 0 && (
          <div className="mt-8 pt-6 border-t border-white/5">
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4 flex items-center gap-2">
              Verified Sources
              <span className="h-px flex-1 bg-white/5"></span>
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {data.citations.map((c, idx) => (
                <CitationItem key={c.id || idx} citation={c} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
