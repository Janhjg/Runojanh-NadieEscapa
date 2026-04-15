'use client';

import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';

const LABELS: Record<string, string> = {
  '/crimes':     'ARCHIVO POLICIAL',
  '/predict':    'MÓDULO PREDICTIVO',
  '/classify':   'PERFIL CRIMINAL',
  '/narrate':    'CRÓNICA OSCURA',
  '/full-case':  'ANÁLISIS TOTAL',
  '/new-case':   'NUEVO EXPEDIENTE',
  '/menu':       'CENTRO OPS',
};

export default function PageTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [displayChildren, setDisplayChildren] = useState(children);
  const [transitioning, setTransitioning] = useState(false);
  const [currentPath, setCurrentPath] = useState(pathname);

  useEffect(() => {
    if (pathname !== currentPath) {
      setTransitioning(true);
      const t = setTimeout(() => {
        setDisplayChildren(children);
        setCurrentPath(pathname);
        setTransitioning(false);
      }, 650); // duración total del overlay
      return () => clearTimeout(t);
    } else {
      setDisplayChildren(children);
    }
  }, [pathname, children]);

  const label = LABELS[pathname] || 'ACCESO RESTRINGIDO';

  return (
    <div className="flex flex-col flex-grow relative">
      <AnimatePresence>
        {transitioning && (
          <motion.div
            key="overlay"
            className="fixed inset-0 z-[100] flex flex-col items-center justify-center overflow-hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
          >
            {/* Fondo negro total */}
            <div className="absolute inset-0 bg-[#000]" />

            {/* Scanlines que barren de arriba a abajo */}
            <motion.div
              className="absolute inset-0"
              style={{
                background: 'repeating-linear-gradient(0deg, rgba(255,0,0,0.04) 0px, rgba(255,0,0,0.04) 1px, transparent 1px, transparent 4px)',
              }}
              animate={{ backgroundPositionY: ['0px', '200px'] }}
              transition={{ duration: 0.4, ease: 'linear', repeat: Infinity }}
            />

            {/* Sello de expediente */}
            <motion.div
              className="relative z-10 flex flex-col items-center gap-6"
              initial={{ scale: 2.5, opacity: 0, rotate: -8 }}
              animate={{ scale: 1, opacity: 1, rotate: -4 }}
              transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
            >
              {/* Sello rojo */}
              <div
                className="border-4 border-red-700 px-10 py-4 relative"
                style={{
                  boxShadow: '0 0 40px rgba(153,0,0,0.7), inset 0 0 20px rgba(100,0,0,0.5)',
                  transform: 'rotate(-4deg)',
                }}
              >
                <p className="text-red-600 font-black uppercase tracking-[0.4em] text-2xl md:text-3xl"
                  style={{ fontFamily: 'var(--font-noir)', textShadow: '0 0 20px #cc0000' }}>
                  {label}
                </p>

                {/* Esquinas del sello */}
                <div className="absolute top-1 left-1 w-3 h-3 border-t-2 border-l-2 border-red-700" />
                <div className="absolute top-1 right-1 w-3 h-3 border-t-2 border-r-2 border-red-700" />
                <div className="absolute bottom-1 left-1 w-3 h-3 border-b-2 border-l-2 border-red-700" />
                <div className="absolute bottom-1 right-1 w-3 h-3 border-b-2 border-r-2 border-red-700" />
              </div>

              {/* Barras de carga */}
              <motion.div
                className="flex gap-1"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                {[...Array(12)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="w-4 h-1.5 bg-red-900"
                    animate={{ backgroundColor: ['#7f1d1d', '#dc2626', '#7f1d1d'] }}
                    transition={{ duration: 0.3, delay: i * 0.04, repeat: Infinity }}
                  />
                ))}
              </motion.div>

              <p className="text-gray-600 font-mono text-xs uppercase tracking-[0.3em]">
                Cargando expediente...
              </p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <motion.div
        key={currentPath}
        className="flex flex-col flex-grow"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        {displayChildren}
      </motion.div>
    </div>
  );
}

