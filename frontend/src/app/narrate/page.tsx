'use client';

import { useState, useEffect, Suspense } from 'react';
import TypewriterChronicle from '@/components/TypewriterChronicle';
import { BookOpen, Activity, Search, AlertTriangle, Volume2, Square, Download } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSearchParams } from 'next/navigation';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

function NarrateContent() {
  const searchParams = useSearchParams();
  const [id, setId] = useState(searchParams.get('id') || '');
  const [loading, setLoading] = useState(false);
  const [audioLoading, setAudioLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [diagnostic, setDiagnostic] = useState<string | null>(null);

  useEffect(() => {
    const qid = searchParams.get('id');
    if (qid) { setId(qid); handleFetch(qid); }
  }, [searchParams]);

  useEffect(() => {
    return () => {
      if (audio) {
        audio.pause();
        audio.src = '';
      }
    };
  }, [audio]);

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
      
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Error al generar audio');
      }
      
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
      } else if (err.message.includes('E11_ERROR')) {
        const parts = err.message.split(' - ');
        const details = parts.slice(1).join(' - ');
        setError(`Error del Servidor de Voz (ElevenLabs).`);
        setDiagnostic(details);
      } else {
        setError("Error al conectar con el servicio de voz. Verifique su conexión.");
      }
    } finally {
      setAudioLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!result) return;
    const caseId = result.registro_id || id;
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
    <main className="container mx-auto px-4 py-8 flex-grow max-w-5xl">
      <header className="mb-10 border-b border-amber-900/50 pb-6">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 flex items-center justify-center bg-amber-950/30 border-2 border-amber-600 rounded-lg shadow-[0_0_15px_rgba(217,119,6,0.5)]">
            <BookOpen size={28} className="text-amber-500" />
          </div>
          <div>
            <h1 className="glitch-text-frequent text-3xl font-black uppercase tracking-widest text-white" style={{ fontFamily: 'var(--font-noir)' }}>
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
        <div className="mx-auto max-w-4xl mb-8 space-y-2">
          <div className="flex items-center gap-4 border-2 border-red-900/80 bg-red-950/40 p-6 rounded-lg text-red-400 text-lg">
            <AlertTriangle size={28} /> <p>{error}</p>
          </div>
          {diagnostic && (
            <div className="bg-black/80 border border-red-900/40 p-4 rounded-lg">
              <p className="text-[10px] text-red-500 font-black uppercase tracking-widest mb-1">Diagnóstico Técnico ElevenLabs:</p>
              <p className="text-xs font-mono text-red-800 break-words">{diagnostic}</p>
              <p className="text-[9px] text-red-900 mt-2 italic">Si el error dice "Paid plan required", ElevenLabs bloquea esta voz para uso de API en cuentas gratuitas, aunque funcione en su web.</p>
            </div>
          )}
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
            <div className="flex justify-between items-center px-4">
              <span className="text-xl font-black text-amber-600 tracking-[0.2em] uppercase font-serif">EXPEDIENTE #{result.registro_id}</span>
              <button
                onClick={handleDownloadPDF}
                disabled={pdfLoading}
                className="flex items-center gap-2 bg-amber-950/20 hover:bg-amber-600 border border-amber-600 text-white px-4 py-2 rounded-lg transition-all disabled:opacity-50 text-xs font-bold tracking-tighter"
              >
                {pdfLoading ? <Activity size={16} className="animate-spin" /> : <Download size={16} />}
                IMPRIMIR EXPEDIENTE
              </button>
            </div>
            <div className="bg-[#050400] border-2 border-amber-900/50 rounded-xl p-8 shadow-2xl relative group">
              <button
                onClick={handleListen}
                disabled={audioLoading}
                className="absolute top-4 right-4 z-10 p-3 bg-amber-900/20 border border-amber-700/50 text-amber-500 rounded-lg hover:bg-amber-600 hover:text-white transition-all shadow-[0_0_15px_rgba(217,119,6,0.2)] disabled:opacity-50"
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
