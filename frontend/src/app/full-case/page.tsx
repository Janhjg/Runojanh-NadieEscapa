'use client';

import { useState, useEffect, Suspense } from 'react';
import { fetchFullCaseById } from '@/services/api';
import ResultsDashboard from '@/components/ResultsDashboard';
import TypewriterChronicle from '@/components/TypewriterChronicle';
import { Archive, Activity, Search, AlertTriangle, FileSearch, Volume2, Square, Download } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSearchParams } from 'next/navigation';

function FullCaseContent() {
  const searchParams = useSearchParams();
  const [id, setId] = useState(searchParams.get('id') || '');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [audioLoading, setAudioLoading] = useState(false);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);
  
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

  useEffect(() => {
    const qid = searchParams.get('id');
    if (qid) {
      setId(qid);
      handleFetch(qid);
    }
  }, [searchParams]);

  const handleFetch = async (targetId: string) => {
    if (!targetId) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await fetchFullCaseById(parseInt(targetId, 10));
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleFetch(id);
  };

  useEffect(() => {
    return () => {
      if (audio) {
        audio.pause();
        audio.src = '';
      }
    };
  }, [audio]);

  const handleListen = async () => {
    if (!result?.cronica) return;
    
    if (isPlaying && audio) {
      audio.pause();
      setIsPlaying(false);
      return;
    }

    setAudioLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/tts/narrate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: result.cronica })
      });
      
      if (!res.ok) throw new Error('Error al generar audio');
      
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const newAudio = new Audio(url);
      
      newAudio.onended = () => setIsPlaying(false);
      setAudio(newAudio);
      newAudio.play();
      setIsPlaying(true);
    } catch (err: any) {
      console.error(err);
      if (err.message.includes('quota')) {
        setError("Límite de voz (ElevenLabs) agotado para este mes.");
      } else if (err.message.includes('paid_plan')) {
        setError("Esta voz requiere un plan de pago. Contacte al administrador.");
      } else {
        setError("Error al conectar con el servicio de voz. Verifique su conexión.");
      }
    } finally {
      setAudioLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!result) return;
    const caseId = result.id || result.registro_id;
    setPdfLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/export/pdf/${caseId}`);
      if (!res.ok) throw new Error('Error al generar PDF');
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Expediente_LAPD_${caseId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      console.error(err);
      setError("No se pudo descargar el expediente.");
    } finally {
      setPdfLoading(false);
    }
  };

  return (
    <main className="container mx-auto px-4 py-8 flex-grow max-w-7xl">
      <header className="mb-10 border-b border-green-900 pb-6">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 flex items-center justify-center bg-green-950/30 border-2 border-green-600 rounded-lg shadow-[0_0_15px_rgba(34,197,94,0.5)]">
            <Archive size={28} className="text-green-500" />
          </div>
          <div>
            <h1 className="glitch-text-frequent text-3xl font-black uppercase tracking-widest text-white" style={{ fontFamily: 'var(--font-noir)' }}>
              Análisis Full Case
            </h1>
            <p className="text-sm text-green-500 uppercase tracking-widest mt-1">Integración Total: Predicción + Clasificación + Narrativa</p>
          </div>
        </div>
      </header>

      <form onSubmit={onSubmit} className="flex gap-4 mb-12 max-w-4xl mx-auto">
        <div className="relative flex-grow">
          <input
            type="number"
            placeholder="DR_NO Caso Histórico (Ej: 10304468)"
            value={id}
            onChange={(e) => setId(e.target.value)}
            className="w-full bg-[#05100a] border px-6 py-4 text-xl font-mono text-white placeholder-green-900/50 outline-none transition-all border-green-900 focus:border-green-600 rounded-lg"
          />
          <FileSearch className="absolute right-4 top-1/2 -translate-y-1/2 text-green-800" size={24} />
        </div>
        <button
          type="submit"
          disabled={loading || !id}
          className="bg-green-800 hover:bg-green-600 text-white px-8 md:px-12 rounded-lg flex items-center justify-center gap-3 transition-colors disabled:opacity-50 text-base font-bold uppercase tracking-widest"
        >
          {loading ? <Activity size={24} className="animate-spin" /> : <Search size={24} />}
          Investigar
        </button>
      </form>

      {error && (
        <div className="flex items-center gap-4 border-2 border-red-900/80 bg-red-950/40 p-6 rounded-lg text-red-400 text-lg mx-auto max-w-4xl mb-8">
          <AlertTriangle size={28} /> <p>{error}</p>
        </div>
      )}

      {loading && (
        <div className="flex flex-col items-center justify-center py-24 gap-6">
          <Archive size={64} className="text-green-500 animate-pulse" />
          <div className="flex flex-col items-center gap-2">
            <p className="text-lg uppercase tracking-[0.3em] font-bold text-green-400">Reconstruyendo Expediente...</p>
            <span className="text-sm text-green-700 animate-pulse font-mono tracking-widest">Iniciando RandomForest & BART-Large...</span>
          </div>
        </div>
      )}

      <AnimatePresence mode="wait">
        {result && (
          <motion.div 
            key={result.id || result.registro_id || 'case'} 
            initial={{ opacity: 0, y: 20 }} 
            animate={{ opacity: 1, y: 0 }} 
            exit={{ opacity: 0 }}
            className="space-y-12"
          >
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-green-500 uppercase tracking-widest">Panel de Evidencias</h2>
              <button
                onClick={handleDownloadPDF}
                disabled={pdfLoading}
                className="flex items-center gap-2 bg-green-900/30 hover:bg-green-600 border border-green-600 text-white px-4 py-2 rounded-lg transition-all disabled:opacity-50 text-xs font-bold tracking-tighter"
              >
                {pdfLoading ? <Activity size={16} className="animate-spin" /> : <Download size={16} />}
                DESCARGAR EXPEDIENTE (PDF)
              </button>
            </div>
             <ResultsDashboard data={result} />
             
             <div className="space-y-6 pt-10 border-t-4 border-gray-800 border-dashed">
               <div className="flex items-center gap-6">
                 <div className="h-0.5 bg-green-900 flex-grow" />
                 <h4 className="text-2xl font-black text-green-500 uppercase tracking-widest font-serif">Narrativa Confidencial</h4>
                 <div className="h-0.5 bg-green-900 flex-grow" />
               </div>
               
               <div className="bg-[#050a0a] border border-green-900/30 rounded-xl p-8 shadow-2xl relative group">
                  <button
                    onClick={handleListen}
                    disabled={audioLoading}
                    className="absolute top-4 right-4 z-10 p-3 bg-green-900/20 border border-green-700/50 text-green-500 rounded-lg hover:bg-green-600 hover:text-white transition-all shadow-[0_0_15px_rgba(34,197,94,0.2)] disabled:opacity-50"
                    title={isPlaying ? "Detener narración" : "Escuchar informe (ElevenLabs)"}
                  >
                    {audioLoading ? (
                      <Activity size={20} className="animate-spin" />
                    ) : isPlaying ? (
                      <Square size={20} fill="currentColor" />
                    ) : (
                      <Volume2 size={20} />
                    )}
                  </button>
                  <TypewriterChronicle text={result.cronica} speed={30} />
                </div>
             </div>

             <footer className="pt-8 flex flex-col md:flex-row items-center justify-between gap-6 opacity-60">
               <div className="flex items-center gap-4 text-sm uppercase tracking-widest text-gray-400">
                 <span>Caso: #{result.id || result.registro_id}</span>
                 <span className="w-2 h-2 rounded-full bg-gray-500" />
                 <span>Verificado por IA</span>
               </div>
               <div className="flex gap-2">
                  {[...Array(5)].map((_, i) => (
                    <div key={i} className="w-8 h-1.5 bg-green-900/50 rounded-full" />
                  ))}
               </div>
             </footer>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}

export default function FullCasePage() {
  return (
    <Suspense fallback={<div className="p-24 text-center text-green-600 text-2xl font-bold animate-pulse">Iniciando Protocolo de Análisis...</div>}>
      <FullCaseContent />
    </Suspense>
  );
}
