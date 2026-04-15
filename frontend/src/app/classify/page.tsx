'use client';

import { useState, useEffect, Suspense } from 'react';
import { Tag, Activity, Search, AlertTriangle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSearchParams } from 'next/navigation';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

const CAT_LABELS: Record<string, string> = {
  labels_genericas:              'Percepción Estética',
  labels_motivo_crimen:          'Móvil del Crimen',
  labels_escena_caracteristicas: 'Evidencia Física',
  labels_contexto_clasificacion: 'Contexto Social',
};

function ClassifyContent() {
  const searchParams = useSearchParams();
  const [id, setId] = useState(searchParams.get('id') || '');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const qid = searchParams.get('id');
    if (qid) { setId(qid); handleFetch(qid); }
  }, [searchParams]);

  const handleFetch = async (targetId: string) => {
    if (!targetId) return;
    setLoading(true); setError(null); setResult(null);
    try {
      const res = await fetch(`${API_BASE_URL}/classify/${targetId}`);
      if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.detail || 'Error'); }
      setResult(await res.json());
    } catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  };

  return (
    <main className="container mx-auto px-4 py-8 flex-grow max-w-7xl">
      <header className="mb-10 border-b border-purple-900 pb-6">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 flex items-center justify-center bg-purple-950/30 border-2 border-purple-600 rounded-lg shadow-[0_0_15px_rgba(147,51,234,0.5)]">
            <Tag size={28} className="text-purple-400" />
          </div>
          <div>
            <h1 className="glitch-text-frequent text-3xl font-black uppercase tracking-widest text-white" style={{ fontFamily: 'var(--font-noir)' }}>
              Perfil Criminal NLP
            </h1>
            <p className="text-sm text-purple-400 uppercase tracking-widest mt-1">Motor BART-Large · Zero-Shot Híbrido</p>
          </div>
        </div>
      </header>

      <form onSubmit={e => { e.preventDefault(); handleFetch(id); }} className="flex gap-4 mb-12 max-w-4xl mx-auto">
        <input
          type="number"
          placeholder="Número de Expediente Histórico (DR_NO)"
          value={id}
          onChange={e => setId(e.target.value)}
          className="flex-grow bg-[#080510] border px-6 py-4 text-xl font-mono text-white placeholder-purple-900/50 outline-none transition-all border-purple-900 focus:border-purple-500 rounded-lg"
        />
        <button
          type="submit"
          disabled={loading || !id}
          className="bg-purple-900 hover:bg-purple-700 text-white px-8 md:px-12 rounded-lg flex items-center justify-center gap-3 transition-colors disabled:opacity-50 text-base font-bold uppercase tracking-widest"
        >
          {loading ? <Activity size={24} className="animate-spin" /> : <Search size={24} />}
          Perfilar
        </button>
      </form>

      {error && (
        <div className="flex items-center gap-4 border-2 border-red-900/80 bg-red-950/40 p-6 rounded-lg text-red-400 text-lg mx-auto max-w-4xl mb-8">
          <AlertTriangle size={28} /> <p>{error}</p>
        </div>
      )}

      {loading && (
        <div className="flex flex-col items-center justify-center py-20 gap-6">
          <Activity size={64} className="animate-pulse text-purple-500" />
          <p className="text-lg uppercase tracking-[0.3em] font-bold text-purple-300">Clasificando con BART-Large...</p>
        </div>
      )}

      <AnimatePresence>
        {result && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-8 max-w-6xl mx-auto">
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {result.todas_etiquetas && Object.entries(result.todas_etiquetas).map(([cat, items]: any) => (
                <div key={cat} className="bg-[#080510] border-2 border-purple-900/50 rounded-xl p-8 shadow-xl">
                  <h3 className="text-lg uppercase tracking-widest text-purple-400 font-bold mb-6 border-b border-purple-900/30 pb-3">
                    {CAT_LABELS[cat] || cat}
                  </h3>
                  <div className="flex flex-wrap gap-3">
                    {items.map((item: any, i: number) => (
                      <span
                        key={i}
                        className="px-4 py-2 text-sm font-bold uppercase tracking-wider rounded-lg border"
                        style={{
                          background: i === 0 ? 'rgba(147, 51, 234, 0.2)' : 'rgba(88, 28, 135, 0.1)',
                          borderColor: `rgba(168, 85, 247, ${0.8 - i * 0.15})`,
                          color: `rgba(216, 180, 254, ${1 - i * 0.2})`,
                        }}
                      >
                        {item.label}
                        <span className="ml-2 opacity-50 font-mono">{(item.score * 100).toFixed(0)}%</span>
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {result.texto_construido && (
              <details className="bg-[#080510] border border-gray-800 rounded-xl p-6 group cursor-pointer">
                <summary className="text-base uppercase tracking-widest text-gray-500 hover:text-purple-400 font-bold transition-colors outline-none list-none flex items-center justify-between">
                  Ver Resumen de Hechos Analizado
                </summary>
                <div className="mt-6 pt-4 border-t border-gray-800">
                  <p className="text-lg text-gray-300 leading-relaxed italic border-l-4 border-purple-900 pl-6">{result.texto_construido}</p>
                </div>
              </details>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}

export default function ClassifyPage() {
  return (
    <Suspense fallback={<div className="p-24 text-center text-purple-500 text-2xl font-bold animate-pulse">Cargando Módulo NLP...</div>}>
      <ClassifyContent />
    </Suspense>
  );
}
