'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldAlert, Activity, BookOpen, PlusCircle, Brain, Tag, ChevronRight, LayoutDashboard, ListChecks } from 'lucide-react';
import CaseForm from '@/components/CaseForm';
import ResultsDashboard from '@/components/ResultsDashboard';
import TypewriterChronicle from '@/components/TypewriterChronicle';
import { predictCrime, classifyCrime, narrateCrime } from '@/services/api';

export default function NewCasePage() {
  const [isLoading, setIsLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  
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
      setIsLoading('predict');
      const predictData = await predictCrime(formData);
      setPrediction(predictData);
      
      setIsLoading('classify');
      const classifyData = await classifyCrime(formData, predictData);
      setClassification(classifyData);
      
      setIsLoading('narrate');
      const narrateData = await narrateCrime(formData, predictData, classifyData.todas_etiquetas);
      setChronicle(narrateData.cronica);
      
    } catch (err: any) {
      setError(err.message || 'Error en la investigación');
    } finally {
      setIsLoading(null);
    }
  };

  return (
    <main className="container mx-auto px-4 py-8 flex-grow max-w-7xl">
      <header className="mb-8 border-b border-red-900 pb-6">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 flex items-center justify-center bg-red-950/30 border-2 border-red-600 rounded-lg shadow-[0_0_15px_rgba(220,38,38,0.5)]">
            <PlusCircle size={28} className="text-red-500" />
          </div>
          <div>
            <h1 className="glitch-text-frequent text-3xl font-black uppercase tracking-widest text-white" style={{ fontFamily: 'var(--font-noir)' }}>
              Nuevo Caso
            </h1>
            <p className="text-sm text-red-500 uppercase tracking-widest mt-1">Creación de Expediente e Investigación Neural</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
        
        {/* COLUMNA IZQUIERDA: FORMULARIO */}
        <div className="lg:col-span-12 xl:col-span-5 space-y-6">
          <CaseForm onSubmit={handleFullProcess} isLoading={!!isLoading} />
          
          {error && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-center gap-4 border-2 border-red-900/80 bg-red-950/40 p-6 rounded-lg text-red-400 text-lg">
              <ShieldAlert size={28} /> {error}
            </motion.div>
          )}
        </div>

        {/* COLUMNA DERECHA: RESULTADOS */}
        <div className="lg:col-span-12 xl:col-span-7">
          <div className="flex items-center justify-between mb-6 border-b border-gray-800 pb-4">
            <div className="flex gap-6">
              <button 
                onClick={() => setActiveTab('full')}
                className={`flex items-center gap-2 text-base font-bold uppercase tracking-widest pb-3 transition-all border-b-4 ${activeTab === 'full' ? 'text-white border-red-600' : 'text-gray-500 border-transparent hover:text-gray-300'}`}
              >
                <LayoutDashboard size={20} /> Dashboard
              </button>
              <button 
                onClick={() => setActiveTab('steps')}
                className={`flex items-center gap-2 text-base font-bold uppercase tracking-widest pb-3 transition-all border-b-4 ${activeTab === 'steps' ? 'text-white border-red-600' : 'text-gray-500 border-transparent hover:text-gray-300'}`}
              >
                <ListChecks size={20} /> Log Neural
              </button>
            </div>
          </div>

          <div className="min-h-[600px]">
            {isLoading && (
              <div className="flex flex-col items-center justify-center py-32 gap-8">
                <div className="relative">
                  <Activity size={80} className="text-red-500 animate-pulse" />
                  <div className="absolute inset-0 bg-red-500/20 blur-xl rounded-full" />
                </div>
                <div className="text-center space-y-3">
                  <p className="text-xl md:text-2xl uppercase tracking-[0.3em] font-black text-white">
                    {isLoading === 'predict' && 'Prediciendo Arresto...'}
                    {isLoading === 'classify' && 'Construyendo Perfil...'}
                    {isLoading === 'narrate' && 'Escribiendo Crónica...'}
                  </p>
                  <p className="text-sm text-red-500 animate-pulse font-mono font-bold tracking-widest">Ejecución en Progreso</p>
                </div>
              </div>
            )}

            {!isLoading && !prediction && !classification && !chronicle && (
               <div className="flex flex-col items-center justify-center h-full opacity-30 py-32 grayscale">
                 <ShieldAlert size={100} className="mb-6 mx-auto text-gray-500" />
                 <p className="text-2xl uppercase tracking-[0.3em] font-bold text-gray-300">Esperando Ficha</p>
               </div>
            )}

            <AnimatePresence mode="wait">
              {activeTab === 'full' && !isLoading && (prediction || classification) ? (
                <motion.div key="full" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-10">
                  <ResultsDashboard 
                    data={{ 
                      prediccion_ml: prediction || { clase_predicha: 'Calculando...', confianza: 0 },
                      clasificacion_hf: classification || { todas_etiquetas: {}, modelo: 'BART' }
                    }} 
                  />
                  {chronicle && (
                    <div className="space-y-6 pt-8 border-t border-gray-800">
                      <div className="flex items-center gap-6">
                        <div className="h-0.5 bg-red-900 flex-grow" />
                        <span className="text-xl font-black text-white uppercase tracking-widest font-serif">CRÓNICA DEL CASO</span>
                        <div className="h-0.5 bg-red-900 flex-grow" />
                      </div>
                      <div className="bg-[#050505] p-8 border border-gray-800 rounded-xl">
                        <TypewriterChronicle text={chronicle} />
                      </div>
                    </div>
                  )}
                </motion.div>
              ) : null}

              {activeTab === 'steps' && (isLoading || prediction || classification) ? (
                <motion.div key="steps" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                  <LogEntry icon={Brain} label="Inferencia RandomForest (Arresto)" status={prediction ? 'done' : isLoading === 'predict' ? 'loading' : 'pending'} />
                  <LogEntry icon={Tag} label="Clasificación BART-Large (Perfil)" status={classification ? 'done' : isLoading === 'classify' ? 'loading' : 'pending'} />
                  <LogEntry icon={BookOpen} label="Generación Narrativa (Ollama)" status={chronicle ? 'done' : isLoading === 'narrate' ? 'loading' : 'pending'} />
                </motion.div>
              ) : null}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </main>
  );
}

function LogEntry({ icon: Icon, label, status }: { icon: any, label: string, status: 'done' | 'loading' | 'pending' }) {
  return (
    <div className={`p-6 border-2 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4 transition-all ${status === 'done' ? 'border-red-900 bg-red-950/20' : status === 'loading' ? 'border-red-600 bg-red-900/10 shadow-[0_0_15px_rgba(220,38,38,0.2)]' : 'border-gray-800 bg-black'}`}>
      <div className="flex items-center gap-4">
        <Icon size={28} className={status === 'done' ? 'text-red-500' : status === 'loading' ? 'text-red-400' : 'text-gray-600'} />
        <span className={`text-base md:text-lg uppercase tracking-widest font-bold ${status === 'done' ? 'text-white' : status === 'loading' ? 'text-red-100' : 'text-gray-500'}`}>
          {label}
        </span>
      </div>
      <div className="flex items-center gap-3">
        {status === 'loading' && <Activity size={20} className="text-red-500 animate-spin" />}
        <span className={`text-sm tracking-[0.2em] font-mono font-bold ${status === 'done' ? 'text-red-500' : status === 'loading' ? 'text-red-400' : 'text-gray-600'}`}>
          {status === 'done' ? '[COMPLETADO]' : status === 'loading' ? '[PROCESANDO]' : '[ESPERA]'}
        </span>
      </div>
    </div>
  );
}
