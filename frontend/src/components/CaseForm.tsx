'use client';

import { useState } from 'react';
import { Search, ShieldAlert, FileText } from 'lucide-react';

interface CaseFormProps {
  onSubmit: (data: any) => void;
  isLoading: boolean;
}

export default function CaseForm({ onSubmit, isLoading }: CaseFormProps) {
  const [formData, setFormData] = useState({
    "DATE OCC": new Date().toISOString().split('T')[0] + " 12:00:00 AM",
    "TIME OCC": 1200,
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
      [name]: name === "TIME OCC" || name === "Rpt Dist No" || name === "Part 1-2" || name === "Vict Age" 
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

  return (
    <form onSubmit={handleSubmit} className="noir-card space-y-4">
      <div className="flex items-center gap-2 border-b border-noir-border pb-2 mb-4">
        <FileText className="text-noir-accent" size={20} />
        <h2 className="text-lg font-bold uppercase tracking-widest">Nueva Ficha de Crimen</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-1 md:col-span-2">
          <label className="text-xs uppercase text-noir-muted">Fecha del Incidente</label>
          <input 
            type="text" 
            name="DATE OCC" 
            value={formData["DATE OCC"]} 
            onChange={handleChange}
            placeholder="DD/MM/YYYY 12:00:00 AM"
            className="w-full bg-black border border-noir-border p-2 text-sm focus:border-noir-accent outline-none"
          />
        </div>
        <div className="space-y-1">
          <label className="text-xs uppercase text-noir-muted">Área / Distrito</label>
          <input 
            type="text" 
            name="AREA NAME" 
            list="areas-list"
            value={formData["AREA NAME"]} 
            onChange={handleChange}
            className="w-full bg-black border border-noir-border p-2 text-sm focus:border-noir-accent outline-none"
          />
          <datalist id="areas-list">
            {areaOptions.map(opt => <option key={opt} value={opt} />)}
          </datalist>
        </div>
        <div className="space-y-1">
          <label className="text-xs uppercase text-noir-muted">Crimen Principal</label>
          <input 
            type="text" 
            name="Crm Cd Desc" 
            list="crimes-list"
            value={formData["Crm Cd Desc"]} 
            onChange={handleChange}
            className="w-full bg-black border border-noir-border p-2 text-sm focus:border-noir-accent outline-none"
          />
        </div>

        {/* Crímenes Secundarios (Opcionales) */}
        <div className="space-y-1">
          <label className="text-xs uppercase text-noir-muted">Secundario 1 (Opcional)</label>
          <input 
            type="text" 
            name="Crm Cd 2 Desc" 
            list="crimes-list"
            value={formData["Crm Cd 2 Desc"] || ""} 
            onChange={handleChange}
            className="w-full bg-black border border-noir-border p-2 text-sm focus:border-noir-accent outline-none border-dashed"
          />
        </div>
        <div className="space-y-1">
          <label className="text-xs uppercase text-noir-muted">Secundario 2 (Opcional)</label>
          <input 
            type="text" 
            name="Crm Cd 3 Desc" 
            list="crimes-list"
            value={formData["Crm Cd 3 Desc"] || ""} 
            onChange={handleChange}
            className="w-full bg-black border border-noir-border p-2 text-sm focus:border-noir-accent outline-none border-dashed"
          />
        </div>
        <div className="space-y-1">
          <label className="text-xs uppercase text-noir-muted">Secundario 3 (Opcional)</label>
          <input 
            type="text" 
            name="Crm Cd 4 Desc" 
            list="crimes-list"
            value={formData["Crm Cd 4 Desc"] || ""} 
            onChange={handleChange}
            className="w-full bg-black border border-noir-border p-2 text-sm focus:border-noir-accent outline-none border-dashed"
          />
        </div>

        <datalist id="crimes-list">
          {crimeOptions.map(opt => <option key={opt} value={opt} />)}
        </datalist>

        <div className="space-y-1">
          <label className="text-xs uppercase text-noir-muted">Víctima (Edad / Sexo)</label>
          <div className="flex gap-2">
            <input 
              type="number" 
              name="Vict Age" 
              value={formData["Vict Age"]} 
              onChange={handleChange}
              className="w-1/2 bg-black border border-noir-border p-2 text-sm focus:border-noir-accent outline-none"
            />
            <select 
              name="Vict Sex" 
              value={formData["Vict Sex"]} 
              onChange={handleChange}
              className="w-1/2 bg-black border border-noir-border p-2 text-sm focus:border-noir-accent outline-none"
            >
              <option value="M">Masc.</option>
              <option value="F">Fem.</option>
              <option value="X">Otro</option>
            </select>
          </div>
        </div>
        <div className="space-y-1">
          <label className="text-xs uppercase text-noir-muted">Descendencia de Víctima</label>
          <select 
            name="Vict Descent" 
            value={formData["Vict Descent"]} 
            onChange={handleChange}
            className="w-full bg-black border border-noir-border p-2 text-sm focus:border-noir-accent outline-none"
          >
            {descentOptions.map(opt => <option key={opt.code} value={opt.code}>{opt.label}</option>)}
          </select>
        </div>
        <div className="space-y-1 md:col-span-2">
          <label className="text-xs uppercase text-noir-muted">Arma Utilizada</label>
          <input 
            type="text" 
            name="Weapon Desc" 
            list="weapons-list"
            value={formData["Weapon Desc"]} 
            onChange={handleChange}
            className="w-full bg-black border border-noir-border p-2 text-sm focus:border-noir-accent outline-none"
          />
          <datalist id="weapons-list">
            {weaponOptions.map(opt => <option key={opt} value={opt} />)}
          </datalist>
        </div>
      </div>

      <button 
        type="submit" 
        disabled={isLoading}
        className="w-full mt-6 bg-noir-accent hover:bg-red-800 text-white font-bold py-3 uppercase tracking-tighter flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
      >
        {isLoading ? (
          <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-white" />
        ) : (
          <>
            <Search size={18} />
            Analizar Caso
          </>
        )}
      </button>
    </form>
  );
}
