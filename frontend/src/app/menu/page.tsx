'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { Folder, Brain, Tag, BookOpen, Archive, PlusCircle, BarChart3 } from 'lucide-react';

const menuItems = [
  {
    title: 'Dataset Oficial',
    desc: 'Explora y visualiza casos reales del archivo LAPD (Años 2020-2023).',
    icon: Folder,
    href: '/crimes',
    color: 'text-gray-400',
    border: 'border-gray-800'
  },
  {
    title: 'Monitor Táctico',
    desc: 'Mapa de calor y estadísticas globales de criminalidad en Los Ángeles.',
    icon: BarChart3,
    href: '/stats',
    color: 'text-green-400',
    border: 'border-green-800'
  },
  {
    title: 'Predicción ML',
    desc: 'Usa Machine Learning (RandomForest) para adivinar si hubo arresto.',
    icon: Brain,
    href: '/predict',
    color: 'text-blue-500',
    border: 'border-blue-900/50'
  },
  {
    title: 'Clasificar Perfil',
    desc: 'Perfilación psicológica del caso usando HuggingFace BART-Large.',
    icon: Tag,
    href: '/classify',
    color: 'text-purple-500',
    border: 'border-purple-900/50'
  },
  {
    title: 'Generar Crónica',
    desc: 'Crea una novela negra interactiva con IA Generativa local.',
    icon: BookOpen,
    href: '/narrate',
    color: 'text-amber-500',
    border: 'border-amber-900/50'
  },
  {
    title: 'Análisis Total',
    desc: 'Flujo completo (ML + HF + GenAI) para un caso del dataset oficial.',
    icon: Archive,
    href: '/full-case',
    color: 'text-green-500',
    border: 'border-green-900/50'
  },
  {
    title: 'Crear Caso',
    desc: 'Crea tu propio caso personalizado y somételo al oráculo criminal.',
    icon: PlusCircle,
    href: '/new-case',
    color: 'text-red-600',
    border: 'border-red-900/50'
  }
];

export default function MenuPage() {
  return (
    <main className="container mx-auto px-4 py-12 flex-grow max-w-7xl">
      <header className="mb-16 text-center space-y-4">
        <h1
          className="glitch-text-frequent text-5xl font-black tracking-tighter uppercase relative inline-block"
          style={{
            fontFamily: 'var(--font-noir)',
            color: '#d4d4d4',
          }}
        >
          Centro de Operaciones
          <div className="absolute -bottom-4 left-1/2 w-32 h-1 bg-red-800 transform -translate-x-1/2"></div>
        </h1>
        <p className="text-sm uppercase tracking-widest text-gray-500 pt-6">Selecciona un módulo de instigación</p>
      </header>


      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {menuItems.map((item, i) => (
          <Link href={item.href} key={item.href}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className={`h-full relative overflow-hidden bg-black border-2 ${item.border} rounded-lg p-8
                hover:border-opacity-100 transition-all duration-300 group shadow-lg`}
              whileHover={{ scale: 1.02 }}
            >
              <div className="mb-6 bg-gray-900/30 w-16 h-16 flex items-center justify-center rounded-full border border-gray-800">
                <item.icon className={`${item.color} group-hover:scale-110 transition-transform duration-300 drop-shadow-md`} size={32} />
              </div>
              <h2 className="text-xl font-bold uppercase tracking-widest mb-3 text-white group-hover:text-white transition-colors" style={{ fontFamily: 'var(--font-noir)' }}>
                {item.title}
              </h2>
              <p className="text-base text-gray-400 group-hover:text-gray-300 transition-colors">
                {item.desc}
              </p>
              
              {/* Resplandor de fondo según el color del módulo */}
              <div className={`absolute -right-10 -bottom-10 w-40 h-40 rounded-full blur-3xl opacity-0 group-hover:opacity-20 transition-opacity duration-500 ${item.href === '/predict' ? 'bg-blue-500' : item.href === '/classify' ? 'bg-purple-500' : item.href === '/narrate' ? 'bg-amber-500' : item.href === '/full-case' ? 'bg-green-500' : item.href === '/new-case' ? 'bg-red-500' : 'bg-gray-500'}`} />
            </motion.div>
          </Link>
        ))}
      </div>
    </main>
  );
}
