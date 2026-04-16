'use client';

import { useState, useEffect } from 'react';
import { Map, Marker, ZoomControl } from 'pigeon-maps';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, LineChart, Line 
} from 'recharts';
import { Activity, Map as MapIcon, BarChart3, ShieldAlert, Users, Clock } from 'lucide-react';
import { motion } from 'framer-motion';

// Gancho de debounce personalizado
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  return debouncedValue;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export default function StatsPage() {
  const [summary, setSummary] = useState<any>(null);
  const [geoData, setGeoData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [fetching, setFetching] = useState(false);
  
  const [meta, setMeta] = useState<{
    areas: any[], descents: any[], sexes: any[], statuses: any[]
  }>({
    areas: [], descents: [], sexes: [], statuses: []
  });
  const [crimesList, setCrimesList] = useState<any[]>([]);
  
  // Filtros Básicos
  const [selectedArea, setSelectedArea] = useState('');
  const [crimeDesc, setCrimeDesc] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [drNo, setDrNo] = useState('');
  
  // Filtros Avanzados (Investigación)
  const [victSex, setVictSex] = useState('');
  const [victDescent, setVictDescent] = useState('');
  const [victAgeMin, setVictAgeMin] = useState<number>(0);
  const [victAgeMax, setVictAgeMax] = useState<number>(100);
  const [timeOccMin, setTimeOccMin] = useState<number>(0);
  const [timeOccMax, setTimeOccMax] = useState<number>(2359);
  const [statusDescFilter, setStatusDescFilter] = useState('');
  const [weaponDescFilter, setWeaponDescFilter] = useState('');
  const [premisDescFilter, setPremisDescFilter] = useState('');

  const [activeFilters, setActiveFilters] = useState(0);

  // Debouncing de búsqueda de crimen (Se mantiene para fluidez visual pero no dispara fetch automático)
  const debouncedCrimeDesc = useDebounce(crimeDesc, 500);

  useEffect(() => {
    // Liberamos el loader inmediatamente para que el usuario vea el panel
    setLoading(false); 
    
    async function fetchMeta() {
      try {
        const res = await fetch(`${API_BASE_URL}/crimes/meta`, { signal: AbortSignal.timeout(5000) as any });
        const data = await res.json();
        setMeta({
          areas: data.areas || [],
          descents: data.descents || [],
          sexes: data.sexes || [],
          statuses: data.statuses || []
        });
      } catch (e) {
        console.error("Error fetching meta (background):", e);
      }
    }
    fetchMeta();
    fetchData(); // Carga inicial para que no aparezca vacío
  }, []);

  const fetchData = async () => {
    setFetching(true);
    try {
      const params = new URLSearchParams();
      if (selectedArea) params.append('area_name', selectedArea);
      if (crimeDesc) params.append('crime_desc', crimeDesc);
      if (dateFrom) params.append('date_from', dateFrom);
      if (dateTo) params.append('date_to', dateTo);
      if (victSex) params.append('vict_sex', victSex);
      if (victDescent) params.append('vict_descent', victDescent);
      if (victAgeMin > 0) params.append('vict_age_min', victAgeMin.toString());
      if (victAgeMax < 100) params.append('vict_age_max', victAgeMax.toString());
      if (timeOccMin > 0) params.append('time_occ_min', timeOccMin.toString());
      if (timeOccMax < 2359) params.append('time_occ_max', timeOccMax.toString());
      if (statusDescFilter) params.append('status_desc', statusDescFilter);
      if (weaponDescFilter) params.append('weapon_desc', weaponDescFilter);
      if (premisDescFilter) params.append('premis_desc', premisDescFilter);
      if (drNo) params.append('dr_no', drNo);

      const qs = params.toString();
      const [subRes, geoRes, listRes] = await Promise.all([
        fetch(`${API_BASE_URL}/stats/summary${qs ? '?' + qs : ''}`),
        fetch(`${API_BASE_URL}/stats/geo${qs ? '?' + qs : ''}`),
        fetch(`${API_BASE_URL}/crimes?limit=10${qs ? '&' + qs : ''}`)
      ]);
      setSummary(await subRes.json());
      setGeoData(await geoRes.json());
      const listData = await listRes.json();
      setCrimesList(listData.crimes || []);
      
      let count = 0;
      if (selectedArea) count++;
      if (crimeDesc) count++;
      if (dateFrom || dateTo) count++;
      if (drNo) count++;
      if (victSex || victDescent || victAgeMin > 0 || victAgeMax < 100) count++;
      if (statusDescFilter || weaponDescFilter || premisDescFilter) count++;
      setActiveFilters(count);

    } catch (e) {
      console.error("Error fetching stats:", e);
    } finally {
      setFetching(false);
    }
  };

  // Eliminado el useEffect automático para evitar reinicios

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black gap-6">
      <Activity size={64} className="text-green-500 animate-spin" />
      <span className="text-green-500 font-mono tracking-[0.5em] uppercase text-xl animate-pulse">
        Sincronizando con Servidores LAPD...
      </span>
    </div>
  );

  // Preparar datos para Recharts
  const pieData = [
    { name: 'Arrestos', value: summary?.arrestos },
    { name: 'Libres', value: summary?.no_arrestos },
    { name: 'Investigación', value: summary?.en_investigacion },
  ];
  const COLORS = ['#22c55e', '#ef4444', '#f59e0b']; // Verde Neón, Rojo Alerta, Ámbar Investigativo

  const hourlyData = Object.entries(summary?.distribucion_horaria || {}).map(([h, count]) => ({
    hora: `${h}:00`,
    crimenes: count
  }));

  const topCrimesData = Object.entries(summary?.top_crimenes || {}).map(([name, count]) => ({
    name: name.split(' - ')[0].substring(0, 15),
    count
  }));

  return (
    <main className="min-h-screen bg-black text-white p-6 font-mono relative overflow-hidden">
      {/* Efecto Scanline sutil */}
      <div className="pointer-events-none fixed inset-0 z-50 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_4px,3px_100%] opacity-20" />
      
      {/* Header Estilo Terminal */}
      <header className="mb-4 border-b-2 border-green-900 pb-4 flex justify-between items-end relative z-10">
        <div>
          <h1 className="text-4xl font-black text-green-500 tracking-tighter uppercase italic drop-shadow-[0_0_8px_rgba(34,197,94,0.6)]">
            CENTRO DE OPERACIONES TÁCTICAS
          </h1>
          <p className="text-green-800 text-sm mt-1 uppercase font-bold">Monitor de Incidencias en Tiempo Real · Los Ángeles District</p>
        </div>
        <div className="text-right">
          <p className="text-xs text-green-700">SESIÓN: ADMIN_DETECTIVE_77</p>
          <p className="text-xs text-green-700 font-bold animate-pulse">ESTADO: CONECTADO [CIFRADO]</p>
        </div>
      </header>

      {/* Panel de Control / Filtros */}
      <section className="mb-8 space-y-4 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 bg-green-950/20 p-4 border border-green-900/50 rounded-lg">
          <div className="space-y-1">
            <label className="text-[10px] text-green-600 font-bold uppercase tracking-widest">Sector / Área</label>
            <select 
              value={selectedArea}
              onChange={(e) => setSelectedArea(e.target.value)}
              className="w-full bg-black border border-green-900 text-green-400 p-2 text-xs outline-none focus:border-green-500 rounded font-mono"
            >
              <option value="">TODOS LOS SECTORES</option>
              {meta.areas.map(a => <option key={a.id} value={a.name}>{a.name}</option>)}
            </select>
          </div>
          <div className="space-y-1">
            <label className="text-[10px] text-green-600 font-bold uppercase tracking-widest">Tipo de Crimen</label>
            <input 
              type="text"
              placeholder="Ej: ASSAULT, THEFT..."
              value={crimeDesc}
              onChange={(e) => setCrimeDesc(e.target.value)}
              className="w-full bg-black border border-green-900 text-green-400 p-2 text-xs outline-none focus:border-green-500 rounded font-mono placeholder-green-900"
            />
          </div>
          <div className="space-y-1">
            <label className="text-[10px] text-green-600 font-bold uppercase tracking-widest">Fecha Inicio</label>
            <input 
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="w-full bg-black border border-green-900 text-green-400 p-2 text-xs outline-none focus:border-green-500 rounded font-mono [color-scheme:dark]"
            />
          </div>
          <div className="space-y-1">
            <label className="text-[10px] text-green-600 font-bold uppercase tracking-widest">Fecha Fin</label>
            <input 
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="w-full bg-black border border-green-900 text-green-400 p-2 text-xs outline-none focus:border-green-500 rounded font-mono [color-scheme:dark]"
            />
          </div>
          <div className="space-y-1">
            <label className="text-[10px] text-green-600 font-bold uppercase tracking-widest">ID Expediente (DR_NO)</label>
            <input 
              type="text"
              placeholder="Ej: 210101..."
              value={drNo}
              onChange={(e) => setDrNo(e.target.value)}
              className="w-full bg-black border border-green-900 text-green-400 p-2 text-xs outline-none focus:border-green-500 rounded font-mono placeholder-green-900"
            />
          </div>
          <div className="space-y-1">
             <label className="text-[10px] text-green-600 font-bold uppercase tracking-widest italic opacity-50">Acción</label>
             <button 
                onClick={fetchData}
                disabled={fetching}
                className="w-full h-[37px] bg-green-900/30 hover:bg-green-600 border border-green-600 text-green-400 hover:text-white font-black uppercase text-[10px] tracking-widest transition-all flex items-center justify-center gap-2 group shadow-[0_0_15px_rgba(22,163,74,0.2)]"
             >
                {fetching ? <Activity size={14} className="animate-spin" /> : <ShieldAlert size={14} className="group-hover:animate-pulse" />}
                BUSCAR
             </button>
          </div>
        </div>

        {/* Filtros Avanzados de Investigación */}
        <div className="bg-black/40 border border-green-900 p-4 rounded-lg">
          <h3 className="text-[10px] text-green-500 font-black uppercase tracking-[0.3em] mb-4 flex items-center gap-2">
            <Activity size={14} /> Filtros de Investigación (Listados)
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
            <div className="space-y-1">
              <label className="text-[9px] text-green-700 font-bold uppercase">Sexo Víctima</label>
              <select 
                value={victSex} 
                onChange={e => setVictSex(e.target.value)}
                className="w-full bg-black border border-green-900/50 text-green-500 p-1 text-[10px] outline-none rounded"
              >
                <option value="">TODOS</option>
                {meta.sexes.map(s => <option key={s} value={s}>{s === 'M' ? 'MASCULINO' : s === 'F' ? 'FEMENINO' : 'OTROS'}</option>)}
              </select>
            </div>
            <div className="space-y-1">
              <label className="text-[9px] text-green-700 font-bold uppercase">Edad Víctima ({victAgeMin}-{victAgeMax})</label>
              <div className="flex gap-2">
                <input type="number" value={victAgeMin} onChange={e => setVictAgeMin(parseInt(e.target.value) || 0)} className="w-1/2 bg-black border border-green-900/50 text-green-500 p-1 text-[10px] rounded" />
                <input type="number" value={victAgeMax} onChange={e => setVictAgeMax(parseInt(e.target.value) || 100)} className="w-1/2 bg-black border border-green-900/50 text-green-500 p-1 text-[10px] rounded" />
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-[9px] text-green-700 font-bold uppercase">Arma (Búsqueda)</label>
              <input 
                type="text" 
                placeholder="Ej: GUN, KNIFE..."
                value={weaponDescFilter}
                onChange={e => setWeaponDescFilter(e.target.value)}
                className="w-full bg-black border border-green-900/50 text-green-500 p-1 text-[10px] rounded placeholder-green-900" 
              />
            </div>
            <div className="space-y-1">
              <label className="text-[9px] text-green-700 font-bold uppercase">Estado Legal</label>
              <select 
                value={statusDescFilter}
                onChange={e => setStatusDescFilter(e.target.value)}
                className="w-full bg-black border border-green-900/50 text-green-500 p-1 text-[10px] outline-none rounded"
              >
                <option value="">TODOS</option>
                {meta.statuses.map(st => <option key={st} value={st}>{st.toUpperCase()}</option>)}
              </select>
            </div>
            <div className="space-y-1">
              <label className="text-[9px] text-green-700 font-bold uppercase">Etnia Víctima</label>
              <select 
                value={victDescent} 
                onChange={e => setVictDescent(e.target.value)}
                className="w-full bg-black border border-green-900/50 text-green-500 p-1 text-[10px] outline-none rounded"
              >
                <option value="">TODAS</option>
                {meta.descents.map(d => (
                  <option key={d.code || d} value={d.code || d}>{d.label || d}</option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 relative z-10">
        
        {/* Columna Izquierda: KPIs Rápidos */}
        <div className="space-y-6">
          <div className="bg-green-950/10 border-2 border-green-900/50 p-6 rounded-lg relative overflow-hidden group hover:border-green-500/50 transition-all">
            <div className="absolute top-0 right-0 p-2 opacity-5 group-hover:opacity-20 transition-opacity">
              <ShieldAlert size={80} />
            </div>
            <p className="text-xs text-green-600 uppercase mb-1 font-bold">Total de Expedientes</p>
            <h2 className="text-5xl font-black text-white tabular-nums drop-shadow-[0_0_10px_rgba(255,255,255,0.2)]">
              {summary?.total_casos.toLocaleString()}
            </h2>
            <div className="mt-4 flex items-center gap-2">
              <div className="h-2 flex-grow bg-green-900/40 rounded-full overflow-hidden border border-green-800">
                <div 
                  className="h-full bg-green-500 shadow-[0_0_15px_#22c55e]" 
                  style={{ width: `${summary?.tasa_arresto}%` }}
                />
              </div>
              <span className="text-xs text-green-500 font-black tracking-tighter">{summary?.tasa_arresto}% ÉXITO</span>
            </div>
          </div>

          <div className="bg-black/40 border border-green-900 p-6 rounded-lg backdrop-blur-sm">
            <div className="flex items-center gap-2 mb-4">
              <BarChart3 size={18} className="text-green-500" />
              <h3 className="text-sm font-bold uppercase tracking-widest text-green-400">Distribución Criminal</h3>
            </div>
            <div className="h-48">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={45}
                    outerRadius={65}
                    paddingAngle={8}
                    dataKey="value"
                    stroke="none"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} className="drop-shadow-[0_0_5px_rgba(0,0,0,0.5)]" />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#000', border: '1px solid #14532d', color: '#22c55e', fontSize: '10px' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex justify-between mt-2 text-[10px] text-green-700 border-t border-green-900/50 pt-2 font-bold">
              <span className="flex items-center gap-1 uppercase"><div className="w-2 h-2 bg-green-500 rounded-full shadow-[0_0_5px_#22c55e]" /> Arrestos</span>
              <span className="flex items-center gap-1 uppercase"><div className="w-2 h-2 bg-red-600 rounded-full shadow-[0_0_5px_#ef4444]" /> Libres</span>
              <span className="flex items-center gap-1 uppercase"><div className="w-2 h-2 bg-amber-500 rounded-full shadow-[0_0_5px_#f59e0b]" /> Investig.</span>
            </div>
          </div>

          <div className="bg-black/40 border border-green-900 p-6 rounded-lg backdrop-blur-sm">
             <div className="flex items-center gap-2 mb-4">
                <Clock size={18} className="text-green-500" />
                <h3 className="text-sm font-bold uppercase tracking-widest text-green-400">Picos de Actividad</h3>
             </div>
             <div className="h-40">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={hourlyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#052e16" vertical={false} strokeOpacity={0.3} />
                    <XAxis dataKey="hora" hide />
                    <YAxis hide />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#000', border: '1px solid #22c55e', color: '#22c55e', fontSize: '10px' }}
                      itemStyle={{ color: '#22c55e' }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="crimenes" 
                      stroke="#22c55e" 
                      strokeWidth={3} 
                      dot={false} 
                      className="drop-shadow-[0_0_8px_rgba(34,197,94,0.8)]"
                    />
                  </LineChart>
                </ResponsiveContainer>
             </div>
          </div>
        </div>

        {/* Columna Central y Derecha: Mapa Táctico */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-black border-2 border-green-900/50 rounded-lg overflow-hidden h-[500px] relative shadow-[0_0_40px_rgba(0,30,0,0.6)] group">
            <div className="absolute top-4 left-4 z-10 bg-black/90 border border-green-600 p-3 flex flex-col gap-1 backdrop-blur-xl shadow-2xl">
               <div className="flex items-center gap-3">
                 <MapIcon size={20} className="text-green-500 animate-pulse" />
                 <div>
                    <h4 className="text-[10px] font-black text-green-400 uppercase tracking-tighter">Mapa Táctico de Sectores</h4>
                    <p className="text-[9px] text-green-700 font-bold uppercase">Los Ángeles Metro Area</p>
                 </div>
               </div>
               <div className="mt-2 text-[9px] font-bold text-green-500 flex items-center justify-between border-t border-green-900 pt-1">
                 <span>MOSTRANDO: {geoData.length}</span>
                 <span className="text-green-800 ml-4">TOTAL FILTRADO: {summary?.total_casos || 0}</span>
               </div>
            </div>
            
            {fetching && (
               <div className="absolute inset-0 z-20 bg-black/40 flex items-center justify-center backdrop-blur-[2px]">
                  <Activity size={32} className="text-green-500 animate-spin" />
                  <span className="ml-3 text-xs text-green-500 font-bold uppercase tracking-widest animate-pulse">Sincronizando...</span>
               </div>
            )}
            
            <Map 
              height={500} 
              defaultCenter={[34.0522, -118.2437]} 
              defaultZoom={11}
              mouseWheel={false}
              metaWheelZoom={true}
              dprs={[1, 2]}
            >
              {geoData.map((d: any, idx: number) => {
                const markerColor = d.status === 'arrest' ? '#22c55e' : d.status === 'no_arrest' ? '#ef4444' : '#f59e0b';
                return (
                  <Marker 
                    key={idx} 
                    width={18} 
                    anchor={[d.lat, d.lon]} 
                    color={markerColor}
                    onClick={() => alert(`ID: ${d.id}\nCrimen: ${d.crime}\nÁrea: ${d.area}\nEstado: ${d.status === 'arrest' ? 'Arrestado' : d.status === 'no_arrest' ? 'Libre' : 'En Investigación'}`)}
                  />
                );
              })}
              <ZoomControl />
            </Map>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
             <div className="bg-green-950/10 border border-green-900 p-6 rounded-lg">
                <div className="flex items-center gap-2 mb-4">
                  <ShieldAlert size={18} className="text-green-500" />
                  <h3 className="text-sm font-bold uppercase tracking-widest text-green-400">Focos de Criminalidad</h3>
                </div>
                <div className="space-y-4">
                   {topCrimesData.map((crime, i) => (
                      <div key={i} className="group/item">
                        <div className="flex justify-between text-[10px] mb-1 font-bold">
                          <span className="text-green-400 uppercase group-hover/item:text-white transition-colors">{crime.name}</span>
                          <span className="text-green-500">{crime.count}</span>
                        </div>
                        <div className="h-1.5 bg-green-950 rounded-full overflow-hidden border border-green-900/50">
                           <motion.div 
                            initial={{ width: 0 }}
                            animate={{ width: `${(crime.count / topCrimesData[0].count) * 100}%` }}
                            className="h-full bg-green-600 shadow-[0_0_10px_rgba(22,163,74,0.5)]" 
                           />
                        </div>
                      </div>
                   ))}
                </div>
             </div>

             <div className="bg-green-950/10 border-2 border-green-900/50 p-6 rounded-lg flex flex-col justify-center items-center text-center relative overflow-hidden group">
                <div className="absolute inset-0 bg-green-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                <Users size={32} className="text-green-500 mb-3 opacity-40 group-hover:opacity-80 transition-all" />
                <h4 className="text-[10px] text-green-700 uppercase font-black tracking-[0.2em] mb-1">Estado del Núcleo</h4>
                <p className="text-xl font-black text-green-500 uppercase tracking-tighter">I.A. OPERATIVA</p>
                <p className="text-[10px] text-green-800 mt-3 italic leading-tight max-w-[200px]">
                  "Algoritmo de clasificación validado. Patrones de reincidencia detectados en el Sector 7."
                </p>
             </div>
          </div>
        </div>
      </div>

      {/* Listado de Hallazgos */}
      <section className="mt-8 relative z-10">
        <div className="bg-black border border-green-900 rounded-lg overflow-hidden">
          <div className="bg-green-900/20 p-4 border-b border-green-900 flex justify-between items-center">
             <h3 className="text-sm font-black text-green-500 uppercase tracking-widest flex items-center gap-2">
               <ShieldAlert size={16} /> Registros Encontrados (Vista Rápida)
             </h3>
             <span className="text-[10px] text-green-700 font-bold uppercase">Streaming: Activo</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[10px] border-collapse">
              <thead>
                <tr className="bg-green-900/10 text-green-600 uppercase font-black border-b border-green-900/50">
                  <th className="p-3">DR_NO</th>
                  <th className="p-3">Fecha</th>
                  <th className="p-3">Crimen</th>
                  <th className="p-3">Área</th>
                  <th className="p-3">Víctima</th>
                  <th className="p-3">Estatus</th>
                </tr>
              </thead>
              <tbody className="text-green-400 font-mono">
                {crimesList.length > 0 ? crimesList.map((c, i) => (
                  <tr key={c.DR_NO || i} className="border-b border-green-900/20 hover:bg-green-900/10 transition-colors">
                    <td className="p-3 font-bold text-white">{c.DR_NO}</td>
                    <td className="p-3">{c.DATE_OCC?.split(' ')[0]}</td>
                    <td className="p-3 uppercase">{c.Crm_Cd_Desc?.substring(0, 30)}</td>
                    <td className="p-3 uppercase">{c.AREA_NAME}</td>
                    <td className="p-3">{c.Vict_Age}a / {c.Vict_Sex} / {c.Vict_Descent}</td>
                    <td className={`p-3 font-black ${c.Status_Desc?.includes('Arrest') ? 'text-green-500' : 'text-red-500'}`}>
                      {c.Status_Desc}
                    </td>
                  </tr>
                )) : (
                  <tr>
                    <td colSpan={6} className="p-8 text-center text-green-900 uppercase italic">
                      No se han recuperado registros del núcleo...
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <style jsx global>{`
        .pigeon-attribution { display: none; }
        .pigeon-filters { filter: invert(1) hue-rotate(100deg) brightness(0.4) contrast(1.2); }
        @keyframes scanline {
          0% { transform: translateY(-100%); }
          100% { transform: translateY(100%); }
        }
      `}</style>
    </main>
  );
}
