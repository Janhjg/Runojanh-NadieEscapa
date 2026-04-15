'use client';

import { motion } from 'framer-motion';
import { Target, Fingerprint, Info, ShieldCheck, ShieldAlert } from 'lucide-react';

interface ResultsDashboardProps {
  data: any;
}

export default function ResultsDashboard({ data }: ResultsDashboardProps) {
  const { prediccion_ml, clasificacion_hf } = data;
  
  const categories = [
    { key: 'labels_genericas', title: 'Percepción Estética', accent: '#6b0000' },
    { key: 'labels_motivo_crimen', title: 'Móvil del Crimen', accent: '#8a8a8a' },
    { key: 'labels_escena_caracteristicas', title: 'Evidencia Física', accent: '#991b1b' },
    { key: 'labels_contexto_clasificacion', title: 'Contexto Social', accent: '#4a4a4a' },
  ];

  const arrested = prediccion_ml.clase_predicha === 'arrestado';

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      
      {/* ── SECCIÓN ML: PREDICCIÓN ────────────────────────────────────── */}
      <div className="bg-[#050505] border-2 border-gray-800 rounded-xl p-8 flex flex-col items-center justify-between shadow-2xl relative overflow-hidden">
        
        <div className="absolute top-0 left-0 w-full h-1 bg-blue-600 shadow-[0_0_15px_rgba(37,99,235,0.8)]" />
        
        <div className="flex items-center justify-between w-full border-b border-gray-800 pb-4 mb-8">
          <div className="flex items-center gap-3">
            <Target className="text-blue-500" size={24} />
            <h3 className="text-lg font-black uppercase tracking-widest text-white">Análisis Predictivo ML</h3>
          </div>
          <span className="text-sm font-mono text-gray-500 tracking-widest bg-gray-900 px-3 py-1 rounded">EXP-CORE-01</span>
        </div>
        
        <div className="relative flex items-center justify-center mb-8">
          <div className="absolute inset-0 rounded-full border border-blue-900/30 animate-ping opacity-20" />
          <div className="absolute inset-0 rounded-full border-2 border-blue-600/10 scale-150" />
          
          <svg className="w-56 h-56 transform -rotate-90">
            <circle
              cx="112" cy="112" r="100"
              fill="none"
              stroke="rgba(37,99,235,0.1)"
              strokeWidth="16"
            />
            <motion.circle
              cx="112" cy="112" r="100"
              fill="none"
              stroke={arrested ? "#dc2626" : "#4ade80"}
              strokeWidth="16"
              strokeDasharray="628"
              initial={{ strokeDashoffset: 628 }}
              animate={{ strokeDashoffset: 628 - (628 * prediccion_ml.confianza) }}
              transition={{ duration: 1.8, ease: "circOut" }}
              strokeLinecap="round"
            />
          </svg>
          
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-5xl font-black text-white" style={{ fontFamily: 'var(--font-noir)' }}>
              {(prediccion_ml.confianza * 100).toFixed(0)}%
            </span>
            <span className="text-xs uppercase tracking-[0.3em] font-bold text-gray-500 mt-2">Certidumbre</span>
          </div>
        </div>
        
        <div className="w-full bg-[#0a0a0a] border border-gray-800 rounded-lg p-6 text-center shadow-inner">
          <p className="text-xs uppercase tracking-[0.3em] font-bold text-gray-500 mb-2">Estatus Predicho</p>
          <div className="flex items-center justify-center gap-4">
            {arrested ? <ShieldAlert size={28} className="text-red-500" /> : <ShieldCheck size={28} className="text-green-500" />}
            <p className={`text-2xl md:text-3xl font-black uppercase tracking-widest ${arrested ? 'text-red-500' : 'text-green-500'}`} style={{ fontFamily: 'var(--font-noir)' }}>
              {prediccion_ml.clase_predicha}
            </p>
          </div>
        </div>
      </div>

      {/* ── SECCIÓN HF: CLASIFICACIÓN ─────────────────────────────────── */}
      <div className="bg-[#050510] border-2 border-purple-900/40 rounded-xl p-8 space-y-8 shadow-2xl relative overflow-hidden">
        
        <div className="absolute top-0 left-0 w-full h-1 bg-purple-600 shadow-[0_0_15px_rgba(147,51,234,0.8)]" />

        <div className="flex items-center justify-between border-b border-purple-900/50 pb-4">
          <div className="flex items-center gap-3">
            <Fingerprint className="text-purple-400" size={24} />
            <h3 className="text-lg font-black uppercase tracking-widest text-white">Perfilación Neural HF</h3>
          </div>
          <span className="text-sm font-mono text-purple-600 tracking-widest bg-purple-950/30 px-3 py-1 rounded">D-NEURAL-X</span>
        </div>

        <div className="space-y-6">
          {categories.map((cat) => (
            <div key={cat.key} className="relative pl-4 border-l-2 border-purple-900/50">
              <span className="text-xs font-bold uppercase text-purple-400 tracking-[0.2em] block mb-3">
                {cat.title}
              </span>
              <div className="flex flex-wrap gap-2">
                {clasificacion_hf.todas_etiquetas[cat.key]?.map((item: any, i: number) => (
                  <span 
                    key={i} 
                    className="text-xs uppercase tracking-widest font-bold border rounded-md py-2 px-3 transition-all hover:bg-purple-900/30"
                    style={{ 
                      borderColor: i === 0 ? 'rgba(168, 85, 247, 0.6)' : 'rgba(107, 33, 168, 0.4)',
                      color: i === 0 ? 'white' : 'rgba(156, 163, 175, 0.8)',
                      background: i === 0 ? 'rgba(147, 51, 234, 0.2)' : 'transparent'
                    }}
                  >
                    {item.label}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
        
        <div className="pt-6 flex items-center justify-between border-t border-purple-900/30">
          <div className="flex items-center gap-2">
            <Info size={16} className="text-purple-500" />
            <span className="text-xs uppercase font-mono tracking-widest text-purple-400 font-bold">Engine: {clasificacion_hf.modelo}</span>
          </div>
          <div className="flex gap-2">
            <div className="w-2 h-2 rounded-full bg-purple-600" />
            <div className="w-2 h-2 rounded-full bg-purple-600 opacity-50" />
            <div className="w-2 h-2 rounded-full bg-purple-600 opacity-25" />
          </div>
        </div>
      </div>
    </div>
  );
}
