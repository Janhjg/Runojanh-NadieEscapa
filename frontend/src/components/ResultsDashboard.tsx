'use client';

import { motion } from 'framer-motion';
import { Target, Fingerprint, Info } from 'lucide-react';

interface ResultsDashboardProps {
  data: any;
}

export default function ResultsDashboard({ data }: ResultsDashboardProps) {
  const { prediccion_ml, clasificacion_hf } = data;
  
  const categories = [
    { key: 'labels_genericas', title: 'Tonos Generales' },
    { key: 'labels_motivo_crimen', title: 'Motivo' },
    { key: 'labels_escena_caracteristicas', title: 'Escena' },
    { key: 'labels_contexto_clasificacion', title: 'Contexto' },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* ML Prediction Card */}
      <div className="noir-card flex flex-col items-center justify-center space-y-4">
        <div className="flex items-center gap-2 self-start border-b border-noir-border w-full pb-2">
          <Target className="text-noir-accent" size={18} />
          <h3 className="text-sm font-bold uppercase tracking-widest">Predicción Policial</h3>
        </div>
        
        <div className="relative flex items-center justify-center">
          <svg className="w-32 h-32">
            <circle
              cx="64"
              cy="64"
              r="58"
              fill="transparent"
              stroke="#262626"
              strokeWidth="8"
            />
            <motion.circle
              cx="64"
              cy="64"
              r="58"
              fill="transparent"
              stroke="#b91c1c"
              strokeWidth="8"
              strokeDasharray="364.4"
              initial={{ strokeDashoffset: 364.4 }}
              animate={{ strokeDashoffset: 364.4 - (364.4 * prediccion_ml.confianza) }}
              transition={{ duration: 1.5, ease: "easeOut" }}
              strokeLinecap="round"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-2xl font-bold">{(prediccion_ml.confianza * 100).toFixed(0)}%</span>
            <span className="text-[10px] uppercase text-noir-muted">Confianza</span>
          </div>
        </div>
        
        <div className="text-center">
          <p className="text-xs uppercase text-noir-muted mb-1">Resultado Probable</p>
          <p className="text-xl font-bold uppercase text-noir-accent tracking-tighter">
            {prediccion_ml.clase_predicha}
          </p>
        </div>
      </div>

      {/* HuggingFace Labels Card */}
      <div className="noir-card space-y-4">
        <div className="flex items-center gap-2 border-b border-noir-border pb-2">
          <Fingerprint className="text-noir-accent" size={18} />
          <h3 className="text-sm font-bold uppercase tracking-widest">Clasificación HF</h3>
        </div>

        <div className="space-y-3">
          {categories.map((cat) => (
            <div key={cat.key} className="space-y-1">
              <span className="text-[10px] uppercase text-noir-muted block">{cat.title}</span>
              <div className="flex flex-wrap gap-1">
                {clasificacion_hf.todas_etiquetas[cat.key]?.map((item: any, i: number) => (
                  <span 
                    key={i} 
                    className="text-[11px] bg-black border border-noir-border px-2 py-0.5 rounded-full text-noir-fore"
                  >
                    {item.label}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
        
        <div className="pt-2 mt-2 border-t border-noir-border flex items-center gap-1">
          <Info size={12} className="text-noir-muted" />
          <span className="text-[10px] text-noir-muted italic">Modelo: {clasificacion_hf.modelo}</span>
        </div>
      </div>
    </div>
  );
}
