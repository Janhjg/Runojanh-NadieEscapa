'use client';

import { useState, useEffect, Suspense } from 'react';
import { Brain, Activity, Search, AlertTriangle, CheckCircle2, XCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSearchParams } from 'next/navigation';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

function PredictContent() {
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
      const res = await fetch(`${API_BASE_URL}/predict/${targetId}`);
      if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.detail || 'Error'); }
      setResult(await res.json());
    } catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  };

  const arrested = result?.prediccion?.clase_predicha === 'arrestado';

  return (
    <main className="container mx-auto px-4 py-8 flex-grow max-w-7xl">
      <header className="mb-10 border-b border-blue-900 pb-6">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 flex items-center justify-center bg-blue-950/30 border-2 border-blue-600 rounded-lg shadow-[0_0_15px_rgba(37,99,235,0.5)]">
            <Brain size={28} className="text-blue-400" />
          </div>
          <div>
            <h1 className="glitch-text-frequent text-3xl font-black uppercase tracking-widest text-white" style={{ fontFamily: 'var(--font-noir)' }}>
              Módulo Predictivo ML
            </h1>
            <p className="text-sm text-blue-400 uppercase tracking-widest mt-1">Motor RandomForest · Riesgo de Arresto</p>
          </div>
        </div>
      </header>

      <form onSubmit={e => { e.preventDefault(); handleFetch(id); }} className="flex gap-4 mb-12 max-w-4xl mx-auto">
        <input
          type="number"
          placeholder="Número de Expediente Histórico (DR_NO)"
          value={id}
          onChange={e => setId(e.target.value)}
          className="flex-grow bg-[#050510] border px-6 py-4 text-xl font-mono text-white placeholder-blue-900/50 outline-none transition-all border-blue-900 focus:border-blue-500 rounded-lg"
        />
        <button
          type="submit"
          disabled={loading || !id}
          className="bg-blue-900 hover:bg-blue-700 text-white px-8 md:px-12 rounded-lg flex items-center justify-center gap-3 transition-colors disabled:opacity-50 text-base font-bold uppercase tracking-widest"
        >
          {loading ? <Activity size={24} className="animate-spin" /> : <Search size={24} />}
          Analizar
        </button>
      </form>

      {error && (
        <div className="flex items-center gap-4 border-2 border-red-900/80 bg-red-950/40 p-6 rounded-lg text-red-400 text-lg mx-auto max-w-4xl mb-8">
          <AlertTriangle size={28} /> <p>{error}</p>
        </div>
      )}

      {loading && (
        <div className="flex flex-col items-center justify-center py-20 gap-6">
          <Activity size={64} className="animate-pulse text-blue-500" />
          <p className="text-lg uppercase tracking-[0.3em] font-bold text-blue-300">Consultando RandomForest...</p>
        </div>
      )}

      <AnimatePresence>
        {result && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-8 max-w-5xl mx-auto">
            
            <div className={`border-4 rounded-xl p-8 flex items-center gap-8 ${arrested ? 'border-red-600 bg-red-900/20' : 'border-blue-500 bg-blue-900/20'} shadow-2xl`}>
              {arrested
                ? <XCircle size={64} className="text-red-500 shrink-0" />
                : <CheckCircle2 size={64} className="text-blue-400 shrink-0" />
              }
              <div>
                <p className="text-sm uppercase tracking-widest text-gray-400 font-bold mb-2">Veredicto del Sistema</p>
                <p className="text-4xl font-black uppercase tracking-wider" style={{ fontFamily: 'var(--font-noir)', color: arrested ? '#f87171' : '#60a5fa' }}>
                  {arrested ? 'Arresto Efectuado' : 'Sin Arresto Registrado'}
                </p>
                <div className="mt-4 flex items-center gap-4">
                  <div className="w-48 h-3 bg-black rounded-full overflow-hidden border border-gray-700">
                    <div 
                      className={`h-full ${arrested ? 'bg-red-500' : 'bg-blue-500'}`} 
                      style={{ width: `${(result.prediccion?.confianza || 0) * 100}%` }}
                    />
                  </div>
                  <span className="text-lg text-white font-mono font-bold">{(result.prediccion?.confianza * 100).toFixed(1)}% Confianza</span>
                </div>
              </div>
            </div>

            {result.datos_caso && (
              <div className="bg-[#050510] border-2 border-blue-900/50 rounded-xl p-8">
                <h3 className="text-xl font-bold uppercase tracking-widest text-blue-300 mb-6 border-b border-blue-900/50 pb-4">
                  Datos del Expediente #{result.id}
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {[
                    ['Área Policial', result.datos_caso.AREA_NAME || result.datos_caso['AREA NAME']],
                    ['Crimen', result.datos_caso.Crm_Cd_Desc || result.datos_caso['Crm Cd Desc']],
                    ['Arma', result.datos_caso.Weapon_Desc || result.datos_caso['Weapon Desc'] || 'N/A'],
                    ['Víctima', `${result.datos_caso.Vict_Age || result.datos_caso['Vict Age']} años · ${result.datos_caso.Vict_Sex || result.datos_caso['Vict Sex']}`],
                    ['Lugar / Premisa', result.datos_caso.Premis_Desc || result.datos_caso['Premis Desc']],
                    ['Fecha Registrada', result.datos_caso.DATE_OCC || result.datos_caso['DATE OCC']],
                  ].map(([k, v]) => (
                    <div key={k}>
                      <p className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-1">{k}</p>
                      <p className="text-lg text-white break-words">{v}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}

export default function PredictPage() {
  return (
    <Suspense fallback={<div className="p-24 text-center text-blue-500 text-2xl font-bold animate-pulse">Cargando Motor Predictivo...</div>}>
      <PredictContent />
    </Suspense>
  );
}
