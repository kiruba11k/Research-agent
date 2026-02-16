import { motion } from "framer-motion";

const CitationItem = ({ citation }) => (
  <motion.a
    href={citation.url}
    target="_blank"
    whileHover={{ x: 5 }}
    className="group flex items-start gap-2 p-2 rounded-lg hover:bg-white/5 transition-colors"
  >
    <span className="text-xs bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded border border-blue-500/30">
      [{citation.id}]
    </span>
    <span className="text-sm text-slate-300 group-hover:text-white line-clamp-1">
      {citation.title || citation.url}
    </span>
  </motion.a>
);

export default CitationItem;
