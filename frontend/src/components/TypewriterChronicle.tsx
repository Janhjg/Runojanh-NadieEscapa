'use client';

import { useState, useEffect, useRef } from 'react';

interface TypewriterProps {
  text: string;
  speed?: number;
}

export default function TypewriterChronicle({ text, speed = 30 }: TypewriterProps) {
  const [displayedText, setDisplayedText] = useState('');
  const [index, setIndex] = useState(0);
  const prevTextRef = useRef<string | null>(null);
  const firedRef = useRef(false); // evitar dobles disparos

  // Solo reiniciamos si el texto cambia de verdad
  useEffect(() => {
    if (prevTextRef.current !== text) {
      setDisplayedText('');
      setIndex(0);
      prevTextRef.current = text;
      firedRef.current = false; // resetear el flag
    }
  }, [text]);

  // 🔊 Disparar narrador2.mp3 exactamente cuando aparece la primera letra
  useEffect(() => {
    if (index === 1 && !firedRef.current) {
      firedRef.current = true;
      window.dispatchEvent(new CustomEvent('runojanh:narration-done'));
    }
  }, [index]);

  // Mecanismo de escritura carácter a carácter
  useEffect(() => {
    if (index < text.length) {
      const timeout = setTimeout(() => {
        setDisplayedText(prev => prev + text[index]);
        setIndex(prev => prev + 1);
      }, speed);
      return () => clearTimeout(timeout);
    }
  }, [index, text, speed]);

  return (
    <div className="font-noir text-lg leading-relaxed whitespace-pre-wrap p-6 noir-card border-dashed">
      {displayedText}
      {index < text.length && <span className="typewriter-cursor" />}
    </div>
  );
}
