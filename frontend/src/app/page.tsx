'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Skull, AlertTriangle, ChevronRight, Activity, Tag, BookOpen } from 'lucide-react';
import CaseForm from '@/components/CaseForm';
import ResultsDashboard from '@/components/ResultsDashboard';
import TypewriterChronicle from '@/components/TypewriterChronicle';
import { submitFullCase, predictCrime, classifyCrime, narrateCrime } from '@/services/api';

export default function Home() {
  const [isLoading, setIsLoading] = useState<string | null>(null); // 'full', 'predict', 'classify', 'narrate'
  const [error, setError] = useState<string | null>(null);
  
  // States for partial results
  const [currentCrime, setCurrentCrime] = useState<any>(null);
  const [prediction, setPrediction] = useState<any>(null);
  const [classification, setClassification] = useState<any>(null);
  const [chronicle, setChronicle] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'full' | 'steps'>('full');

  const resetAll = () => {
    setPrediction(null);
    setClassification(null);
    setChronicle(null);
    setError(null);
  };

  const handleFullProcess = async (formData: any) => {
    resetAll();
    setCurrentCrime(formData);
    
    try {
      // 1. Fase Predict (Instantánea)
      setIsLoading('predict');
      const predictData = await predictCrime(formData);
      setPrediction(predictData);
      
      // 2. Fase Classify (Lenta - BART Large)
      setIsLoading('classify');
      const classifyData = await classifyCrime(formData, predictData);
      setClassification(classifyData);
      
      // 3. Fase Narrate (Media - Ollama)
      setIsLoading('narrate');
      const narrateData = await narrateCrime(formData, predictData, classifyData.todas_etiquetas);
      setChronicle(narrateData.cronica);
      
    } catch (err: any) {
      setError(err.message || 'Error en la investigación');
    } finally {
      setIsLoading(null);
    }
  };

  const handlePredict = async (formData: any) => {
    setIsLoading('predict');
    resetAll();
    setCurrentCrime(formData);
    try {
      const data = await predictCrime(formData);
      setPrediction(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(null);
    }
  };

  const handleClassify = async () => {
    if (!currentCrime || !prediction) return;
    setIsLoading('classify');
    try {
      const data = await classifyCrime(currentCrime, prediction);
      setClassification(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(null);
    }
  };

  const handleNarrate = async () => {
    if (!currentCrime || !prediction || !classification) return;
    setIsLoading('narrate');
    try {
      const data = await narrateCrime(currentCrime, prediction, classification.todas_etiquetas);
      setChronicle(data.cronica);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(null);
    }
  };

  return (
    <main className="container mx-auto px-4 py-8 flex-grow max-w-6xl">
      {/* Header */}
      <header className="flex flex-col md:flex-row items-center justify-between mb-12 border-b border-noir-border pb-6">
        <div className="flex items-center gap-4 mb-4 md:mb-0">
          <div className="bg-noir-accent p-3 rounded-full shadow-[0_0_15px_rgba(185,28,28,0.5)]">
            <Skull className="text-white" size={32} />
          </div>
          <div>
            <h1 className="text-3xl font-black tracking-tighter uppercase leading-none">
              Runojanh <span className="text-noir-accent font-noir">Detective</span>
            </h1>
            <p className="text-[10px] uppercase tracking-[0.3em] text-noir-muted">Crime Analysis Terminal v2.0</p>
          </div>
        </div>
        
        <div className="flex bg-black border border-noir-border p-1 rounded-sm">
          <button 
            onClick={() => setActiveTab('full')}
            className={`px-4 py-1 text-[10px] uppercase font-bold transition-colors ${activeTab === 'full' ? 'bg-noir-accent text-white' : 'text-noir-muted hover:text-noir-fore'}`}
          >
            Proceso Automático
          </button>
          <button 
            onClick={() => setActiveTab('steps')}
            className={`px-4 py-1 text-[10px] uppercase font-bold transition-colors ${activeTab === 'steps' ? 'bg-noir-accent text-white' : 'text-noir-muted hover:text-noir-fore'}`}
          >
            Análisis Manual
          </button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Input Form */}
        <div className="lg:col-span-4 space-y-6">
          <CaseForm 
            onSubmit={activeTab === 'full' ? handleFullProcess : handlePredict} 
            isLoading={!!isLoading} 
          />
          
          <AnimatePresence>
            {activeTab === 'steps' && prediction && (
              <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="space-y-4">
                <button 
                  onClick={handleClassify}
                  disabled={!!isLoading || !!classification}
                  className="w-full noir-card flex items-center justify-between hover:border-noir-accent transition-colors disabled:opacity-50"
                >
                  <div className="flex items-center gap-3">
                    <Tag size={16} className={classification ? "text-green-500" : "text-noir-accent"} />
                    <span className="text-xs uppercase font-bold">Clasificar con HuggingFace</span>
                  </div>
                  {isLoading === 'classify' && <Activity size={14} className="animate-pulse text-noir-accent" />}
                  {classification && <span className="text-[10px] text-green-500 font-bold">OK</span>}
                </button>

                <button 
                  onClick={handleNarrate}
                  disabled={!!isLoading || !classification || !!chronicle}
                  className="w-full noir-card flex items-center justify-between hover:border-noir-accent transition-colors disabled:opacity-50"
                >
                  <div className="flex items-center gap-3">
                    <BookOpen size={16} className={chronicle ? "text-green-500" : "text-noir-accent"} />
                    <span className="text-xs uppercase font-bold">Generar Crónica (Ollama)</span>
                  </div>
                  {isLoading === 'narrate' && <Activity size={14} className="animate-pulse text-noir-accent" />}
                  {chronicle && <span className="text-[10px] text-green-500 font-bold">OK</span>}
                </button>
              </motion.div>
            )}
          </AnimatePresence>
          
          {error && (
            <div className="bg-red-950/30 border border-red-900 p-4 text-red-500 text-xs flex items-start gap-3">
              <AlertTriangle size={16} className="shrink-0" />
              <p>{error}</p>
            </div>
          )}
        </div>

        {/* Right Column: Results */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          <AnimatePresence mode="wait">
            {!prediction && !isLoading && (
              <motion.div key="empty" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex-grow noir-card flex flex-col items-center justify-center text-center py-24 opacity-30 border-dashed">
                <ChevronRight size={48} className="mb-4" />
                <p className="text-sm uppercase tracking-widest font-noir">Terminal lista para recibir datos</p>
              </motion.div>
            )}

            {(isLoading === 'predict' || isLoading === 'classify' || isLoading === 'narrate') && (
              <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex-grow noir-card flex flex-col items-center justify-center text-center py-20 space-y-6">
                <Activity size={48} className="animate-pulse text-noir-accent" />
                <div className="space-y-2">
                  <p className="text-sm uppercase tracking-widest font-bold">Investigación en Curso</p>
                  <div className="flex flex-col gap-2 items-start text-[10px] uppercase tracking-tighter">
                    <div className="flex items-center gap-2">
                      <div className={`w-2 h-2 rounded-full ${isLoading === 'predict' ? 'bg-noir-accent animate-ping' : prediction ? 'bg-green-500' : 'bg-noir-muted'}`} />
                      <span className={prediction ? 'text-green-500' : 'text-noir-muted'}>Paso 1: Análisis de Probabilidades (ML)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className={`w-2 h-2 rounded-full ${isLoading === 'classify' ? 'bg-noir-accent animate-ping' : classification ? 'bg-green-500' : 'bg-noir-muted'}`} />
                      <span className={classification ? 'text-green-500' : 'text-noir-muted'}>Paso 2: Perfilado del Escenario (BART)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className={`w-2 h-2 rounded-full ${isLoading === 'narrate' ? 'bg-noir-accent animate-ping' : chronicle ? 'bg-green-500' : 'bg-noir-muted'}`} />
                      <span className={chronicle ? 'text-green-500' : 'text-noir-muted'}>Paso 3: Generación de la Crónica (Ollama)</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {prediction && (
              <motion.div key="result" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-6">
                <ResultsDashboard data={{ 
                  prediccion_ml: prediction, 
                  clasificacion_hf: classification || { todas_etiquetas: {}, modelo: "Esperando..." }
                }} />

                {chronicle && (
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 border-b border-noir-border pb-2">
                      <span className="text-xs font-bold uppercase tracking-widest">Crónica Narrativa</span>
                      <span className="text-[10px] text-noir-muted uppercase">(Ollama: gemma2:2b)</span>
                    </div>
                    <TypewriterChronicle text={chronicle} />
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      <footer className="mt-12 pt-6 border-t border-noir-border text-[9px] uppercase tracking-[0.5em] text-center text-noir-muted">
        Runojanh Police AI Division &copy; 2026 - L.A. Precinct
      </footer>
    </main>
  );
}
