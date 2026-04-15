'use client';

import { useState, useEffect } from 'react';
import { fetchAllCrimes, fetchUserCases, fetchCrimesMeta } from '@/services/api';
import {
  Database, Activity, ChevronRight, ChevronLeft,
  Brain, Tag, BookOpen, Archive, User, Filter, Search, RefreshCw, Layers
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';

const SEXO_OPTIONS = [
  { value: '', label: 'Cualquiera' },
  { value: 'F', label: 'Femenino' },
  { value: 'M', label: 'Masculino' },
];

const DESCENT_MAP: Record<string, string> = {
  A: 'Asiática', B: 'Negra', C: 'China', D: 'Camboyana',
  F: 'Filipina', G: 'Guameña', H: 'Hispana', I: 'Indígena',
  J: 'Japonesa', K: 'Coreana', O: 'Otros', P: 'Isleña Pacífico',
  S: 'Samoana', U: 'Hawaiana', V: 'Vietnamita', W: 'Blanca',
  X: 'Desconocida', Z: 'Asiático indio',
};

export default function CrimesPage() {
  const [crimes, setCrimes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [source, setSource] = useState<'LAPD' | 'USER'>('LAPD');
  const [offset, setOffset] = useState(0);
  const limit = 50;

  // Meta dropdown data
  const [metaAreas, setMetaAreas] = useState<{ id: number; name: string }[]>([]);
  const [metaDescents, setMetaDescents] = useState<{ code: string; label: string }[]>([]);

  // Filters
  const [filterSex, setFilterSex] = useState('');
  const [filterArea, setFilterArea] = useState('');
  const [filterPart12, setFilterPart12] = useState('');
  const [filterDescent, setFilterDescent] = useState('');
  const [filterCrmCd, setFilterCrmCd] = useState('');

  const [expandedId, setExpandedId] = useState<string | number | null>(null);

  useEffect(() => {
    fetchCrimesMeta().then((meta: any) => {
      setMetaAreas(meta.areas || []);
      setMetaDescents(meta.descents || []);
    }).catch(() => {});
  }, []);

  const fetchCases = async () => {
    setLoading(true);
    try {
      if (source === 'LAPD') {
        let params = '';
        if (filterSex)    params += `&vict_sex=${filterSex}`;
        if (filterArea)   params += `&area=${filterArea}`;
        if (filterPart12) params += `&part_1_2=${filterPart12}`;
        if (filterDescent) params += `&vict_descent=${filterDescent}`;
        if (filterCrmCd)  params += `&crm_cd=${filterCrmCd}`;
        const data = await fetchAllCrimes(limit, offset, params);
        setCrimes(data.crimes || []);
        setTotal(data.total || 0);
      } else {
        const data = await fetchUserCases(limit, offset);
        setCrimes(data.cases || []);
        setTotal(data.total || 0);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCases();
  }, [offset, source, filterSex, filterArea, filterPart12, filterDescent, filterCrmCd]);

  const resetFilters = () => {
    setFilterSex(''); setFilterArea(''); setFilterPart12('');
    setFilterDescent(''); setFilterCrmCd(''); setOffset(0);
  };

  return (
    <main className="container mx-auto px-4 py-8 flex-grow w-full max-w-7xl">
      <header className="mb-8 border-b border-noir-border pb-6 flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="flex items-center gap-4">
          <Database size={40} className="text-gray-400" />
          <div>
            <h1 className="glitch-text-frequent text-3xl md:text-4xl font-black uppercase tracking-widest text-white" style={{ fontFamily: 'var(--font-noir)' }}>
              Archivo Policial
            </h1>
            <p className="text-sm text-noir-muted uppercase tracking-widest">{total.toLocaleString()} Expedientes</p>
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => { setSource('LAPD'); setOffset(0); }}
            className={`px-6 py-2 text-sm uppercase tracking-widest font-bold transition-all border ${source === 'LAPD' ? 'bg-gray-800 border-gray-600 text-white' : 'bg-black border-noir-border text-noir-muted hover:text-white'}`}
          >
            LAPD Oficial
          </button>
          <button
            onClick={() => { setSource('USER'); setOffset(0); }}
            className={`px-6 py-2 text-sm uppercase tracking-widest font-bold transition-all border ${source === 'USER' ? 'bg-red-900 border-red-500 text-white' : 'bg-black border-noir-border text-noir-muted hover:text-white'}`}
          >
            Casos Privados
          </button>
        </div>
      </header>

      {source === 'LAPD' && (
        <section className="bg-[#0a0a0a] border border-noir-border p-6 mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Filter size={18} className="text-white" />
            <h3 className="text-sm uppercase tracking-widest font-bold text-white">Filtros de Búsqueda</h3>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4">
            <div>
              <label className="text-xs uppercase text-noir-muted mb-2 block">Área Policial</label>
              <select value={filterArea} onChange={e => setFilterArea(e.target.value)} className="w-full bg-black border border-noir-border p-3 text-sm text-white focus:border-white outline-none">
                <option value="">Todas las Áreas</option>
                {metaAreas.map(a => <option key={a.id} value={a.name}>{a.name}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs uppercase text-noir-muted mb-2 block">Sexo Víctima</label>
              <select value={filterSex} onChange={e => setFilterSex(e.target.value)} className="w-full bg-black border border-noir-border p-3 text-sm text-white focus:border-white outline-none">
                {SEXO_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs uppercase text-noir-muted mb-2 block">Descendencia</label>
              <select value={filterDescent} onChange={e => setFilterDescent(e.target.value)} className="w-full bg-black border border-noir-border p-3 text-sm text-white focus:border-white outline-none">
                <option value="">Cualquiera</option>
                {metaDescents.map(d => <option key={d.code} value={d.code}>{d.label}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs uppercase text-noir-muted mb-2 block">Código Crimen</label>
              <input type="text" placeholder="Ej: 624" value={filterCrmCd} onChange={e => setFilterCrmCd(e.target.value)} className="w-full bg-black border border-noir-border p-3 text-sm text-white focus:border-white outline-none" />
            </div>
            <div className="flex items-end">
              <button onClick={resetFilters} className="w-full py-3 border border-red-900 border-dashed text-sm uppercase tracking-widest text-red-500 hover:bg-red-900/20 transition-colors">
                Limpiar Filtros
              </button>
            </div>
          </div>
        </section>
      )}

      <AnimatePresence mode="wait">
        {loading ? (
          <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col items-center justify-center py-32 gap-4">
            <RefreshCw className="animate-spin text-gray-500" size={48} />
            <p className="text-sm uppercase tracking-[0.4em] text-noir-muted">Buscando Expedientes...</p>
          </motion.div>
        ) : crimes.length === 0 ? (
          <motion.div key="empty" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center py-20 grayscale opacity-40">
            <Search size={64} className="mx-auto mb-4 text-white" />
            <p className="text-xl uppercase tracking-widest font-bold text-white">No hay expedientes</p>
          </motion.div>
        ) : (
          <motion.div key="grid" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4 w-full">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {crimes.map((crime, i) => {
                const isUser = source === 'USER';
                const id = isUser ? (crime.user_case_id || crime.registro_id) : (crime.DR_NO || crime.id);
                // Si hay un caso expandido, ocultar los demás
                if (expandedId && expandedId !== id) return null;
                
                return (
                  <CrimeCard 
                    key={id || i} 
                    crime={crime} 
                    source={source} 
                    expanded={expandedId === id}
                    onToggle={() => setExpandedId(expandedId === id ? null : id)}
                  />
                );
              })}
            </div>

            <div className="flex items-center justify-between mt-12 pt-8 border-t border-noir-border text-lg">
              <p className="text-sm uppercase tracking-widest text-noir-muted">
                Resultados {(offset + 1).toLocaleString()} a {(offset + crimes.length).toLocaleString()}
              </p>
              <div className="flex gap-4">
                <button
                  disabled={offset === 0}
                  onClick={() => setOffset(Math.max(0, offset - limit))}
                  className="px-6 py-3 border border-noir-border text-white disabled:opacity-20 hover:bg-white hover:text-black transition-colors"
                >
                  <ChevronLeft size={24} />
                </button>
                <button
                  disabled={offset + limit >= total}
                  onClick={() => setOffset(offset + limit)}
                  className="px-6 py-3 border border-noir-border text-white disabled:opacity-20 hover:bg-white hover:text-black transition-colors"
                >
                  <ChevronRight size={24} />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}

function CrimeCard({ crime, source, expanded, onToggle }: { crime: any, source: 'LAPD' | 'USER', expanded: boolean, onToggle: () => void }) {
  const isUser = source === 'USER';
  const id = isUser ? (crime.user_case_id || crime.registro_id) : (crime.DR_NO || crime.id);
  
  // SOLUCIÓN AL BUG: Parsear datos JSON si vienen como string (como ocurre con SQLite/JSON en Casos Privados)
  let parsedDatos = crime;
  let parsedPred = crime.prediccion_ml || crime.prediccion;
  let parsedClas = crime.clasificacion_hf || crime.clasificacion?.clasificacion_hf || crime.clasificacion;
  let parsedCronica = crime.cronica;
  
  if (isUser) {
    if (crime.datos_entrada) {
      parsedDatos = typeof crime.datos_entrada === 'string' ? JSON.parse(crime.datos_entrada) : crime.datos_entrada;
    }
    if (crime.prediccion) {
      parsedPred = typeof crime.prediccion === 'string' ? JSON.parse(crime.prediccion) : crime.prediccion;
    }
    if (crime.clasificacion) {
      let rawClas = typeof crime.clasificacion === 'string' ? JSON.parse(crime.clasificacion) : crime.clasificacion;
      parsedClas = rawClas.clasificacion_hf || rawClas;
    }
  }

  const area = isUser ? parsedDatos['AREA NAME'] : (crime['AREA_NAME'] || crime['AREA NAME'] || 'N/A');
  const desc = isUser ? parsedDatos['Crm Cd Desc'] : (crime['Crm_Cd_Desc'] || crime['Crm Cd Desc'] || 'N/A');
  const date = isUser ? parsedDatos['DATE OCC'] : (crime['DATE_OCC'] || crime['DATE OCC'] || 'N/A');
  const weapon = isUser ? parsedDatos['Weapon Desc'] : (crime['Weapon_Desc'] || crime['Weapon Desc'] || 'N/A');
  const victAge = isUser ? parsedDatos['Vict Age'] : (crime['Vict_Age'] || crime['Vict Age'] || 'N/A');
  const victSex = isUser ? parsedDatos['Vict Sex'] : (crime['Vict_Sex'] || crime['Vict Sex'] || 'N/A');
  const victDescent = isUser ? parsedDatos['Vict Descent'] : (crime['Vict_Descent'] || crime['Vict Descent'] || 'X');
  const premisDesc = isUser ? parsedDatos['Premis Desc'] : (crime['Premis_Desc'] || crime['Premis Desc'] || 'N/A');
  const part_1_2 = isUser ? parsedDatos['Part 1-2'] : (crime['Part_1_2'] || crime['Part 1-2'] || 2);
  const isSevere = part_1_2 === 1;

  let neonColorClass = isUser 
    ? 'from-red-600 to-red-900 shadow-[0_0_15px_rgba(220,38,38,0.8)]' 
    : (isSevere ? 'from-noir-blood to-red-700 shadow-[0_0_15px_rgba(153,27,27,0.7)]' : 'from-gray-800 to-gray-500 shadow-[0_0_15px_rgba(255,255,255,0.1)]');

  return (
    <div 
      className={`relative bg-[#050505] border p-6 transition-all duration-300 cursor-pointer overflow-hidden glitch-hover ${expanded ? 'border-red-900 md:col-span-2 lg:col-span-4 shadow-[0_0_40px_rgba(220,38,38,0.15)] col-span-1' : 'border-noir-border hover:border-gray-500 hover:shadow-[0_0_20px_rgba(220,38,38,0.08)]'}`}
      onClick={onToggle}
    >
      <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-10 pointer-events-none" />

      {/* Neon line decoration */}
      <div className={`absolute top-0 left-0 w-full h-[2px] transition-all duration-300 bg-gradient-to-r ${neonColorClass}`} />

      <div className="flex justify-between items-start mb-4 mt-2">
        <span className="text-xl font-bold font-mono tracking-widest text-[#d4d4d4] glitch-text-frequent">{isUser ? `CASE-PRIV-${id}` : `CASE-${id}`}</span>
        <div className={`px-3 py-1 text-xs uppercase font-bold tracking-widest border ${isUser ? 'border-red-600 text-red-500' : 'border-gray-700 text-gray-500'}`}>
          {isUser ? 'Documento Privado' : 'Archivo Público'}
        </div>
      </div>

      <div className="flex items-center justify-between gap-6 relative z-10">
        <div className="flex-grow">
          <h3 className="text-lg md:text-xl font-black uppercase tracking-wider text-white mb-2">
            {desc}
          </h3>
          <div className="flex flex-wrap gap-x-6 gap-y-2">
            <div className="flex items-center gap-2 text-sm text-gray-400 uppercase tracking-widest">
              <Layers size={14} className={isUser ? "text-red-600" : "text-white"} /> {area}
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-400 uppercase tracking-widest">
              <User size={14} className={isUser ? "text-red-600" : "text-white"} /> {date?.split(' ')[0]}
            </div>
          </div>
        </div>
        <ChevronRight size={24} className={`text-white transition-transform ${expanded ? 'rotate-90' : ''}`} />
      </div>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="pt-8 mt-6 border-t border-gray-800 space-y-8">
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-sm">
                <div>
                  <span className="text-xs uppercase tracking-widest text-gray-500 block mb-1">Arma</span>
                  <span className="text-white block uppercase">{weapon}</span>
                </div>
                <div>
                  <span className="text-xs uppercase tracking-widest text-gray-500 block mb-1">Lugar</span>
                  <span className="text-white block uppercase">{premisDesc}</span>
                </div>
                <div>
                  <span className="text-xs uppercase tracking-widest text-gray-500 block mb-1">Víctima</span>
                  <span className="text-white block uppercase">{`${victAge} años (${victSex})`}</span>
                </div>
                <div>
                  <span className="text-xs uppercase tracking-widest text-gray-500 block mb-1">Etnia</span>
                  <span className="text-white block uppercase">{DESCENT_MAP[victDescent] || 'Desconocida'}</span>
                </div>
              </div>

              <div className="flex flex-wrap gap-4">
                <Link 
                  href={isUser ? `/narrate?id=${id}` : `/full-case?id=${id}`}
                  className="px-6 py-3 border border-white bg-white text-black text-sm uppercase font-black tracking-widest hover:bg-gray-200 transition-all flex items-center gap-2"
                  onClick={e => e.stopPropagation()}
                >
                  {isUser ? <BookOpen size={16} /> : <Archive size={16} />}
                  {isUser ? 'Abrir Crónica' : 'Full Case Analysis'}
                  <ChevronRight size={16} />
                </Link>
                
                {!isUser && (
                  <>
                    <Link 
                      href={`/predict?id=${id}`}
                      className="px-6 py-3 border border-blue-900 bg-blue-950/20 text-blue-400 text-sm uppercase font-black tracking-widest hover:bg-blue-900 hover:text-white transition-all flex items-center gap-2"
                      onClick={e => e.stopPropagation()}
                    >
                      <Brain size={16} /> CatBoost ML
                    </Link>
                    <Link 
                      href={`/classify?id=${id}`}
                      className="px-6 py-3 border border-purple-900 bg-purple-950/20 text-purple-400 text-sm uppercase font-black tracking-widest hover:bg-purple-900 hover:text-white transition-all flex items-center gap-2"
                      onClick={e => e.stopPropagation()}
                    >
                      <Tag size={16} /> BART Profile
                    </Link>
                  </>
                )}
              </div>

              {isUser && (
                <div className="space-y-6 pt-6 border-t border-gray-800">
                  <h4 className="text-base uppercase tracking-widest font-black text-white flex items-center gap-3">
                    <Brain size={18} className="text-red-500" /> Resultados del Servidor
                  </h4>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="p-4 border border-blue-900 bg-blue-950/10">
                      <span className="text-xs uppercase text-blue-500 block mb-2 font-bold tracking-widest">Motor de Arresto</span>
                      <p className="text-lg font-black uppercase tracking-widest text-white">
                        {parsedPred?.clase_predicha || 'SIN CLASIFICAR'} 
                        <span className="text-sm text-blue-400 ml-4">Confianza: {parsedPred?.confianza ? (parsedPred.confianza * 100).toFixed(1) : 0}%</span>
                      </p>
                    </div>
                    
                    <div className="p-4 border border-purple-900 bg-purple-950/10">
                      <span className="text-xs uppercase text-purple-500 block mb-2 font-bold tracking-widest">Perfil Psicológico</span>
                      <div className="flex flex-wrap gap-2">
                        {parsedClas?.todas_etiquetas?.labels_motivo_crimen?.slice(0, 3).map((l: any, i: number) => (
                          <span key={i} className="px-3 py-1 bg-purple-900/30 border border-purple-700 text-xs uppercase tracking-wider text-purple-200">
                            {l.label}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                  
                  {parsedCronica && (
                    <div className="p-6 bg-[#111] border border-gray-700 mt-4 shadow-[0_0_20px_rgba(255,255,255,0.05)] rounded-lg">
                      <p className="text-xs text-gray-500 font-bold uppercase tracking-widest mb-3 border-b border-gray-800 pb-2">Crónica de Archivo Privado</p>
                      <p className="text-base text-gray-300 leading-relaxed font-serif italic whitespace-pre-wrap">
                        {parsedCronica}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
