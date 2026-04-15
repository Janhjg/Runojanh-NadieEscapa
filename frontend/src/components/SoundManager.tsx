'use client';

/**
 * SoundManager — Gestor de Efectos de Sonido Global
 * 
 * Maneja:
 * - tecla.mp3: suena en cada click de botón/enlace
 * - cuervo.mp3: suena aleatoriamente cada 30-90 segundos
 * - narrador2.mp3: suena cuando Ollama termina de generar texto (evento global)
 * 
 * Coloca los archivos en: frontend/public/audio/
 */

import { useEffect, useRef } from 'react';

function playOneShot(src: string) {
  try {
    const audio = new Audio(src);
    audio.volume = 0.3; // Mucho más bajo para no distraer
    audio.play().catch(() => {});
  } catch {}
}

export default function SoundManager() {
  const crowTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // ── Sonido de tecla en cada click y tecla presionada ────────────────────────────
  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      const isInteractive = target.closest('button, a, input[type="submit"], [role="button"]');
      if (isInteractive) {
        playOneShot('/audio/tecla2.mp3');
      }
    };

    const handleKeyDown = (e: KeyboardEvent) => {
      // Solo sonar si el foco está en un input o textarea (simulando escritura)
      const target = e.target as HTMLElement;
      if (target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement) {
        playOneShot('/audio/tecla2.mp3');
      }
    };

    document.addEventListener('click', handleClick);
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('click', handleClick);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  // ── Cuervo aleatorio ─────────────────────────────────────────
  useEffect(() => {
    const scheduleNextCrow = () => {
      const delay = 30_000 + Math.random() * 60_000; // 30-90 segundos
      crowTimerRef.current = setTimeout(() => {
        playOneShot('/audio/cuervo.mp3');
        scheduleNextCrow(); // reprogramar
      }, delay);
    };

    // Primera aparición: entre 20 y 50 segundos tras montar
    const firstDelay = 20_000 + Math.random() * 30_000;
    crowTimerRef.current = setTimeout(() => {
      playOneShot('/audio/cuervo.mp3');
      scheduleNextCrow();
    }, firstDelay);

    return () => {
      if (crowTimerRef.current) clearTimeout(crowTimerRef.current);
    };
  }, []);

  // ── Narrador2: suena cuando Ollama termina de generar ────────
  useEffect(() => {
    const handleNarrationDone = () => {
      playOneShot('/audio/narrador2.mp3');
    };
    window.addEventListener('runojanh:narration-done', handleNarrationDone);
    return () => window.removeEventListener('runojanh:narration-done', handleNarrationDone);
  }, []);

  return null; // Sin UI visible
}
