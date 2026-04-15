'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';

// SVG Badge policial — más dramático que el emoji
function PoliceBadge({ glitch }: { glitch: boolean }) {
  return (
    <svg
      viewBox="0 0 100 120"
      className={`w-20 h-24 transition-all duration-75 ${glitch ? 'opacity-60 scale-[0.99]' : 'opacity-100'}`}
      style={{ filter: glitch ? 'hue-rotate(15deg)' : 'none' }}
    >
      {/* Outer shield */}
      <path
        d="M50 4 L90 20 L90 65 Q90 100 50 116 Q10 100 10 65 L10 20 Z"
        fill="none"
        stroke="#7f1d1d"
        strokeWidth="1.5"
        className="drop-shadow-lg"
      />
      {/* Inner shield */}
      <path
        d="M50 12 L82 26 L82 63 Q82 92 50 106 Q18 92 18 63 L18 26 Z"
        fill="none"
        stroke="#991b1b"
        strokeWidth="0.8"
        opacity="0.6"
      />
      {/* Star center */}
      <g transform="translate(50,58)" fill="none" stroke="#991b1b" strokeWidth="0.8">
        {[0,60,120,180,240,300].map((angle, i) => (
          <line
            key={i}
            x1="0" y1="0"
            x2={Math.sin((angle * Math.PI) / 180) * 14}
            y2={-Math.cos((angle * Math.PI) / 180) * 14}
          />
        ))}
        <circle r="5" fill="#7f1d1d" strokeWidth="0" />
        <circle r="3" fill="#991b1b" strokeWidth="0" />
      </g>
      {/* Text: LAPD */}
      <text x="50" y="40" textAnchor="middle" fontSize="7" fontFamily="monospace" fill="#6b0000" letterSpacing="3" fontWeight="bold">
        L·A·P·D
      </text>
      {/* Text: DETECTIVE */}
      <text x="50" y="78" textAnchor="middle" fontSize="4.5" fontFamily="monospace" fill="#4a0000" letterSpacing="2">
        DETECTIVE
      </text>
      {/* Badge number */}
      <text x="50" y="90" textAnchor="middle" fontSize="5.5" fontFamily="monospace" fill="#7f1d1d" letterSpacing="1">
        #221B
      </text>
      {/* Glow effect */}
      <defs>
        <radialGradient id="badgeGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#991b1b" stopOpacity="0.15" />
          <stop offset="100%" stopColor="#000" stopOpacity="0" />
        </radialGradient>
      </defs>
      <ellipse cx="50" cy="60" rx="45" ry="50" fill="url(#badgeGlow)" />
    </svg>
  );
}

export default function SplashPage() {
  const router = useRouter();
  const voiceRef = useRef<HTMLAudioElement | null>(null);
  const [starting, setStarting] = useState(false);
  const [glitch, setGlitch] = useState(false);
  const [showStatic, setShowStatic] = useState(false);

  // Glitch periódico
  useEffect(() => {
    const interval = setInterval(() => {
      setGlitch(true);
      setTimeout(() => setGlitch(false), 120);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleStart = () => {
    if (starting) return;
    setStarting(true);
    setShowStatic(true);

    voiceRef.current = new Audio('/audio/narrador.mp3');
    voiceRef.current.play().catch(() => {});
    window.dispatchEvent(new CustomEvent('runojanh:start-music'));

    setTimeout(() => router.push('/menu'), 1400);
  };

  return (
    <main
      className="min-h-screen flex flex-col items-center justify-center relative overflow-hidden select-none"
      style={{ background: '#000' }}
    >
      {/* Layers: scanlines */}
      <div className="scanlines absolute inset-0 z-10 opacity-60" />

      {/* Radial bg */}
      <div
        className="absolute inset-0 z-0"
        style={{ background: 'radial-gradient(ellipse 80% 70% at 50% 50%, #0d0000 0%, #000 75%)' }}
      />

      {/* Red spotlight ambient */}
      <div
        className="absolute inset-0 z-0 pointer-events-none"
        style={{ background: 'radial-gradient(ellipse 50% 35% at 50% 48%, rgba(120,0,0,0.18) 0%, transparent 70%)' }}
      />

      {/* Static flash on start */}
      <AnimatePresence>
        {showStatic && (
          <motion.div
            initial={{ opacity: 0.8 }}
            animate={{ opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="absolute inset-0 z-30 bg-white mix-blend-overlay pointer-events-none"
          />
        )}
      </AnimatePresence>

      {/* Content */}
      <div className="relative z-20 flex flex-col items-center gap-7 px-4 text-center">

        {/* Badge SVG */}
        <motion.div
          initial={{ opacity: 0, scale: 0.5, rotate: -5 }}
          animate={{ opacity: 1, scale: 1, rotate: 0 }}
          transition={{ duration: 1.0, ease: [0.22, 1, 0.36, 1] }}
          className="relative"
        >
          <div
            className="absolute inset-0 rounded-full blur-2xl opacity-30 scale-150"
            style={{ background: 'radial-gradient(circle, #991b1b, transparent)' }}
          />
          <PoliceBadge glitch={glitch} />
        </motion.div>

        {/* Title with glitch layer */}
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.8 }}
          className="relative"
        >
          {/* Glitch clone behind */}
          {glitch && (
            <span
              className="absolute inset-0 text-red-800 text-5xl md:text-7xl font-black uppercase tracking-[0.25em] leading-none select-none translate-x-1"
              style={{ fontFamily: 'var(--font-noir)', clipPath: 'inset(30% 0 50% 0)' }}
            >
              RUNOJANH
            </span>
          )}
          <h1
            className={`text-5xl md:text-7xl font-black uppercase tracking-[0.25em] leading-none transition-colors duration-75 ${glitch ? 'text-red-600' : 'text-white'}`}
            style={{ fontFamily: 'var(--font-noir)', textShadow: '0 0 40px rgba(153,27,27,0.3)' }}
          >
            RUNOJANH
          </h1>
          <p className="mt-2 text-[10px] md:text-xs uppercase tracking-[0.7em] text-red-900 font-bold font-mono">
            ✦ Nadie Escapa ✦
          </p>
        </motion.div>

        {/* Tape line */}
        <motion.div
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ delay: 1.0, duration: 0.7 }}
          className="tape-line w-48"
        />

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.1, duration: 0.8 }}
          className="text-[10px] uppercase tracking-[0.35em] text-noir-blood font-mono"
        >
          División de Análisis Criminal · Los Ángeles
        </motion.p>

        {/* CTA */}
        <motion.button
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.5, duration: 0.5 }}
          onClick={handleStart}
          disabled={starting}
          className="
            group relative mt-2 px-10 py-3.5
            border border-red-900 text-red-800
            text-[10px] uppercase tracking-[0.45em] font-bold font-mono
            hover:bg-red-950/50 hover:border-red-700 hover:text-red-500
            transition-all duration-300 disabled:opacity-40
            hover:shadow-[0_0_25px_rgba(153,27,27,0.35)]
          "
        >
          {starting ? (
            <span className="flex items-center gap-3">
              <span className="inline-block w-2.5 h-2.5 border-t border-red-700 rounded-full animate-spin" />
              Accediendo al Sistema...
            </span>
          ) : (
            <>
              Iniciar Investigación
              <span className="absolute -bottom-px left-0 w-full h-px bg-red-900 scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-300" />
            </>
          )}
        </motion.button>

        {/* Data counter */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.35 }}
          transition={{ delay: 2.2, duration: 1 }}
          className="flex flex-col items-center gap-1"
        >
          <p className="text-[8px] uppercase tracking-[0.3em] text-gray-700 font-mono">
            663,210 expedientes · 2020 – 2023 · L.A. County
          </p>
          <p className="text-[7px] text-noir-blood/40 font-mono tracking-widest">
            ◈ USO EXCLUSIVO PARA INVESTIGACIÓN ◈
          </p>
        </motion.div>
      </div>
    </main>
  );
}
