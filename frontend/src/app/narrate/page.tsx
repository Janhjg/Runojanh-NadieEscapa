'use client';

import { useState, useEffect, Suspense } from 'react';
import TypewriterChronicle from '@/components/TypewriterChronicle';
import { BookOpen, Activity, Search, AlertTriangle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSearchParams } from 'next/navigation';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

function NarrateContent() {
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
      const res = await fetch(`${API_BASE_URL}/narrate/${targetId}`);
      if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.detail || 'Error'); }
      setResult(await res.json());
    } catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  };

  return (
    <main className="container mx-auto px-4 py-8 flex-grow max-w-5xl">
      <header className="mb-10 border-b border-amber-900/50 pb-6">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 flex items-center justify-center bg-amber-950/30 border-2 border-amber-600 rounded-lg shadow-[0_0_15px_rgba(217,119,6,0.5)]">
            <BookOpen size={28} className="text-amber-500" />
          </div>
          <div>
            <h1 className="text-3xl font-black uppercase tracking-widest text-white" style={{ fontFamily: 'var(--font-noir)' }}>
              Crónica de Novela Negra
            </h1>
            <p className="text-sm text-amber-500 uppercase tracking-widest mt-1">Motor Llama / Ollama · Generación Narrativa</p>
          </div>
        </div>
      </header>

      <form onSubmit={e => { e.preventDefault(); handleFetch(id); }} className="flex gap-4 mb-12 max-w-4xl mx-auto">
        <input
          type="number"
          placeholder="Número de Expediente Histórico (DR_NO)"
          value={id}
          onChange={e => setId(e.target.value)}
          className="flex-grow bg-[#0a0800] border px-6 py-4 text-xl font-mono text-white placeholder-amber-900/50 outline-none transition-all border-amber-900 focus:border-amber-600 rounded-lg"
        />
        <button
          type="submit"
          disabled={loading || !id}
          className="bg-amber-800 hover:bg-amber-600 text-white px-8 md:px-12 rounded-lg flex items-center justify-center gap-3 transition-colors disabled:opacity-50 text-base font-bold uppercase tracking-widest"
        >
          {loading ? <Activity size={24} className="animate-spin" /> : <Search size={24} />}
          Relatar
        </button>
      </form>

      {error && (
        <div className="flex items-center gap-4 border-2 border-red-900/80 bg-red-950/40 p-6 rounded-lg text-red-400 text-lg mx-auto max-w-4xl mb-8">
          <AlertTriangle size={28} /> <p>{error}</p>
        </div>
      )}

      {loading && (
        <div className="flex flex-col items-center justify-center py-20 gap-6">
          <div className="relative">
            <Activity size={64} className="text-amber-500 animate-pulse" />
            <div className="absolute inset-0 bg-amber-500/20 blur-xl rounded-full" />
          </div>
          <p className="text-lg uppercase tracking-[0.3em] font-bold text-amber-300">Generando narrativa confidencial...</p>
        </div>
      )}

      <AnimatePresence>
        {result && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
            <div className="flex items-center gap-6 mb-6">
              <div className="h-0.5 bg-amber-900 flex-grow" />
              <span className="text-xl font-black text-amber-600 tracking-[0.2em] uppercase font-serif">CRÓNICA #{result.registro_id}</span>
              <div className="h-0.5 bg-amber-900 flex-grow" />
            </div>
            <div className="bg-[#050400] border-2 border-amber-900/50 rounded-xl p-8 shadow-2xl">
              <TypewriterChronicle text={result.cronica} speed={30} />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}

export default function NarratePage() {
  return (
    <Suspense fallback={<div className="p-24 text-center text-amber-600 text-2xl font-bold animate-pulse">Iniciando máquina de escribir...</div>}>
      <NarrateContent />
    </Suspense>
  );
}
