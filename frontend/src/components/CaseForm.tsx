'use client';

import { useState } from 'react';
import { Search, ShieldAlert, FileText, Calendar, MapPin, User, ChevronRight } from 'lucide-react';

interface CaseFormProps {
  onSubmit: (data: any) => void;
  isLoading: boolean;
}

export default function CaseForm({ onSubmit, isLoading }: CaseFormProps) {
  const [formData, setFormData] = useState({
    "DATE OCC": new Date().toISOString().split('T')[0] + " 12:00:00 AM",
    "TIME OCC": 1200,   // REQUIRED by backend PredictNewInput schema
    "AREA NAME": "Central",
    "Rpt Dist No": 101,
    "Part 1-2": 1,
    "Crm Cd Desc": "",
    "Vict Age": 25,
    "Vict Sex": "M",
    "Vict Descent": "H",
    "Premis Desc": "STREET",
    "Weapon Desc": ""
  } as Record<string, any>);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === "Rpt Dist No" || name === "Part 1-2" || name === "Vict Age" 
        ? parseInt(value) || 0 
        : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const crimeOptions = [
    'VEHICLE - STOLEN', 'BATTERY - SIMPLE ASSAULT', 'ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT',
    'VANDALISM - FELONY ($400 & OVER)', 'THEFT OF IDENTITY', 'BURGLARY FROM VEHICLE',
    'INTIMATE PARTNER - SIMPLE ASSAULT', 'BURGLARY', 'THEFT PLAIN - PETTY ($950 & UNDER)', 'ROBBERY'
  ];

  const weaponOptions = [
    'UNKNOWN WEAPON/OTHER WEAPON', 'STRONG-ARM (HANDS, FIST, FEET OR BODILY FORCE)',
    'VERBAL THREAT', 'HAND GUN', 'SEMI-AUTOMATIC PISTOL', 'KNIFE WITH BLADE 6INCHES OR LESS',
    'UNKNOWN FIREARM', 'OTHER KNIFE', 'MACE/PEPPER SPRAY', 'VEHICLE'
  ];

  const areaOptions = [
    'Central', 'Rampart', 'Southwest', 'Hollenbeck', 'Harbor',
    'Hollywood', 'Wilshire', 'West LA', 'Van Nuys', 'West Valley',
    'Northeast', 'Newton', '77th Street', 'Pacific', 'N Hollywood',
    'Foothill', 'Devonshire', 'Southeast', 'Mission', 'Olympic', 'Topanga'
  ];

  const premisOptions = [
    'STREET', 'SINGLE FAMILY DWELLING', 'MULTI-UNIT DWELLING (APARTMENT, DUPLEX, ETC)',
    'PARKING LOT', 'SIDEWALK', 'VEHICLE, PASSENGER/TRUCK', 'ALLEY',
    'COMMERCIAL BUILDING', 'RESTAURANT/FAST FOOD', 'DRIVEWAY', 'GAS STATION'
  ];

  const descentOptions = [
    { code: "H", label: "Hispana/Latinoamericana" },
    { code: "B", label: "Negra" },
    { code: "W", label: "Blanca" },
    { code: "A", label: "Asiática" },
    { code: "X", label: "Desconocida" },
    { code: "C", label: "China" },
    { code: "J", label: "Japonesa" },
    { code: "O", label: "Otros" },
  ];

  const InputLabel = ({ children }: { children: React.ReactNode }) => (
    <label className="text-xs md:text-sm uppercase tracking-widest text-gray-400 font-bold block mb-2">
      {children}
    </label>
  );

  return (
    <form onSubmit={handleSubmit} className="bg-[#0f0f0f] border-2 border-red-900/50 hover:border-red-600 transition-colors duration-500 shadow-[0_0_40px_rgba(220,38,38,0.15)] rounded-xl p-6 md:p-8 relative overflow-hidden">
      
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-red-900 via-red-500 to-red-900 shadow-[0_0_20px_rgba(220,38,38,0.8)]" />

      <header className="flex items-center justify-between border-b border-gray-800 pb-6 mb-8 mt-2">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 border border-gray-700 flex items-center justify-center bg-black">
            <FileText className="text-red-600" size={24} />
          </div>
          <div>
            <h2 className="text-xl md:text-2xl font-black uppercase tracking-widest text-white" style={{ fontFamily: 'var(--font-noir)' }}>
              Ficha de Incidente
            </h2>
            <p className="text-sm font-mono text-gray-500 tracking-widest mt-1">FORM-CRIM-DS10</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6 text-base">
        
        {/* ── SECCIÓN A: TIEMPO ────────────────────────────────────────── */}
        <div className="space-y-4">
          <div className="flex items-center gap-3 mb-4">
            <Calendar size={18} className="text-red-500" />
            <span className="text-sm font-black uppercase tracking-widest text-gray-300">Cronología</span>
          </div>
          
          <div className="space-y-2">
            <InputLabel>Fecha y Hora Completa</InputLabel>
            <input 
              type="text" 
              name="DATE OCC" 
              value={formData["DATE OCC"]} 
              onChange={handleChange}
              className="w-full bg-black border border-gray-700 px-4 py-3 text-base font-mono text-white focus:border-red-600 outline-none transition-colors"
            />
          </div>

          <div className="space-y-2">
            <InputLabel>Gravedad (Part 1/2)</InputLabel>
            <select 
              name="Part 1-2" 
              value={formData["Part 1-2"]} 
              onChange={handleChange}
              className="w-full bg-black border border-gray-700 px-4 py-3 text-base font-mono text-white focus:border-red-600 outline-none transition-colors"
            >
              <option value="1">1 (Grave)</option>
              <option value="2">2 (Menor)</option>
            </select>
          </div>
        </div>

        {/* ── SECCIÓN B: LOCALIZACIÓN ──────────────────────────────────── */}
        <div className="space-y-4">
          <div className="flex items-center gap-3 mb-4">
            <MapPin size={18} className="text-red-500" />
            <span className="text-sm font-black uppercase tracking-widest text-gray-300">Geolocalización</span>
          </div>

          <div className="space-y-2">
            <InputLabel>Área Policial (División)</InputLabel>
            <input 
              type="text" 
              name="AREA NAME" 
              list="areas-list"
              value={formData["AREA NAME"]} 
              onChange={handleChange}
              className="w-full bg-black border border-gray-700 px-4 py-3 text-base font-mono text-white focus:border-red-600 outline-none transition-colors"
            />
            <datalist id="areas-list">
              {areaOptions.map(opt => <option key={opt} value={opt} />)}
            </datalist>
          </div>

          <div className="space-y-2">
            <InputLabel>Lugar Físico (Premis)</InputLabel>
            <input 
              type="text" 
              name="Premis Desc" 
              list="premis-list"
              value={formData["Premis Desc"]} 
              onChange={handleChange}
              className="w-full bg-black border border-gray-700 px-4 py-3 text-base font-mono text-white focus:border-red-600 focus:shadow-[0_0_15px_rgba(220,38,38,0.3)] outline-none transition-all"
            />
            <datalist id="premis-list">
              {premisOptions.map(opt => <option key={opt} value={opt} />)}
            </datalist>
          </div>
        </div>

        {/* ── SECCIÓN C: NATURALEZA DEL CRIMEN ─────────────────────────── */}
        <div className="md:col-span-2 space-y-6 pt-6 border-t border-gray-800">
          <div className="flex items-center gap-3 mb-4">
            <ShieldAlert size={18} className="text-red-500" />
            <span className="text-sm font-black uppercase tracking-widest text-gray-300">Detalles del Delito</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <InputLabel>Crimen Principal</InputLabel>
              <input 
                type="text" 
                name="Crm Cd Desc" 
                list="crimes-list"
                value={formData["Crm Cd Desc"]} 
                onChange={handleChange}
                placeholder="Descripción del crimen..."
                className="w-full bg-black border border-gray-700 px-4 py-3 text-base font-mono text-white focus:border-red-600 outline-none transition-colors"
              />
            </div>
            <div className="space-y-2">
              <InputLabel>Arma Involucrada</InputLabel>
              <input 
                type="text" 
                name="Weapon Desc" 
                list="weapons-list"
                value={formData["Weapon Desc"]} 
                onChange={handleChange}
                className="w-full bg-black border border-gray-700 px-4 py-3 text-base font-mono text-white focus:border-red-600 outline-none transition-colors"
              />
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[2, 3, 4].map(num => (
              <div key={num} className="space-y-2">
                <InputLabel>Cargo Adicional {num-1}</InputLabel>
                <input 
                  type="text" 
                  name={`Crm Cd ${num} Desc`} 
                  list="crimes-list"
                  value={formData[`Crm Cd ${num} Desc`] || ""} 
                  onChange={handleChange}
                  placeholder="Opcional..."
                  className="w-full bg-black border border-gray-800 border-dashed px-4 py-3 text-sm font-mono text-gray-400 focus:text-white focus:border-red-600 outline-none transition-colors"
                />
              </div>
            ))}
          </div>
          
          <datalist id="crimes-list">
            {crimeOptions.map(opt => <option key={opt} value={opt} />)}
          </datalist>
          <datalist id="weapons-list">
            {weaponOptions.map(opt => <option key={opt} value={opt} />)}
          </datalist>
        </div>

        {/* ── SECCIÓN D: VÍCTIMA ───────────────────────────────────────── */}
        <div className="md:col-span-2 space-y-6 pt-6 border-t border-gray-800">
          <div className="flex items-center gap-3 mb-4">
            <User size={18} className="text-red-500" />
            <span className="text-sm font-black uppercase tracking-widest text-gray-300">Sujeto Pasivo (Víctima)</span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <InputLabel>Edad</InputLabel>
              <input 
                type="number" 
                name="Vict Age" 
                value={formData["Vict Age"]} 
                onChange={handleChange}
                className="w-full bg-black border border-gray-700 px-4 py-3 text-base font-mono text-white focus:border-red-600 outline-none transition-colors"
              />
            </div>
            <div className="space-y-2">
              <InputLabel>Sexo</InputLabel>
              <select 
                name="Vict Sex" 
                value={formData["Vict Sex"]} 
                onChange={handleChange}
                className="w-full bg-black border border-gray-700 px-4 py-3 text-base font-mono text-white focus:border-red-600 outline-none transition-colors"
              >
                <option value="M">Masculino</option>
                <option value="F">Femenino</option>
                <option value="X">Otro</option>
              </select>
            </div>
            <div className="col-span-2 md:col-span-1 space-y-2">
              <InputLabel>Etnia</InputLabel>
              <select 
                name="Vict Descent" 
                value={formData["Vict Descent"]} 
                onChange={handleChange}
                className="w-full bg-black border border-gray-700 px-4 py-3 text-base font-mono text-white focus:border-red-600 outline-none transition-colors"
              >
                {descentOptions.map(opt => <option key={opt.code} value={opt.code}>{opt.label}</option>)}
              </select>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-12 pt-8 border-t border-gray-800 flex flex-col md:flex-row items-center justify-between gap-6">
        <p className="text-xs text-gray-500 uppercase tracking-widest max-w-lg leading-relaxed">
          Al procesar, los datos serán analizados por los motores neuronales de IA de la división criminal LAPD.
        </p>
        
        <button 
          type="submit" 
          disabled={isLoading}
          className="w-full md:w-auto bg-red-800 hover:bg-red-600 text-white font-black px-10 py-5 uppercase tracking-widest text-sm flex items-center justify-center gap-3 transition-all hover:shadow-[0_0_30px_rgba(220,38,38,0.5)] disabled:opacity-50 rounded-lg"
          style={{ fontFamily: 'var(--font-noir)' }}
        >
          {isLoading ? (
            <Search className="animate-spin" size={20} />
          ) : (
            <>
              Procesar Expediente <ChevronRight size={20} />
            </>
          )}
        </button>
      </div>
    </form>
  );
}
