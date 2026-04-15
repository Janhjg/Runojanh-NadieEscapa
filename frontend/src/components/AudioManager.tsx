'use client';

/**
 * AudioManager — Controlador de música y volumen.
 * Estilizado como un mini-panel de control Noir.
 */

import { useEffect, useRef, useState, useCallback } from 'react';
import { Volume2, VolumeX, Volume1, Music, Radio } from 'lucide-react';

const TRACKS = [
  '/audio/bg_1.mp3',
  '/audio/bg_2.mp3',
  '/audio/bg_3.mp3',
  '/audio/bg_4.mp3'
];

const SESSION_KEY = 'runojanh-music-active';

export default function AudioManager() {
  const musicRef = useRef<HTMLAudioElement | null>(null);
  const [volume, setVolume] = useState(0.35);
  const [muted, setMuted] = useState(false);
  const [visible, setVisible] = useState(false);
  const [currentTrackIndex, setCurrentTrackIndex] = useState(0);
  const startedRef = useRef(false);

  const startPlayback = useCallback((trackIdx: number) => {
    if (musicRef.current) {
      musicRef.current.pause();
      musicRef.current.src = '';
    }

    const audio = new Audio(TRACKS[trackIdx]);
    audio.loop = false;
    audio.volume = muted ? 0 : volume;

    audio.addEventListener('ended', () => {
      setCurrentTrackIndex(prev => (prev + 1) % TRACKS.length);
    });

    musicRef.current = audio;
    audio.play().catch(() => {});
    setVisible(true);
  }, [muted, volume]);

  useEffect(() => {
    const wasActive = sessionStorage.getItem(SESSION_KEY) === 'true';

    const handleStart = () => {
      if (!startedRef.current) {
        startedRef.current = true;
        sessionStorage.setItem(SESSION_KEY, 'true');
        startPlayback(0);
      }
    };

    if (wasActive && !startedRef.current) {
      startedRef.current = true;
      startPlayback(0);
    }

    window.addEventListener('runojanh:start-music', handleStart);
    return () => {
      window.removeEventListener('runojanh:start-music', handleStart);
    };
  }, [startPlayback]);

  useEffect(() => {
    if (startedRef.current) {
      startPlayback(currentTrackIndex);
    }
  }, [currentTrackIndex, startPlayback]);

  useEffect(() => {
    if (musicRef.current) {
      musicRef.current.volume = muted ? 0 : volume;
    }
  }, [volume, muted]);

  const handleKey = useCallback((e: KeyboardEvent) => {
    if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
    if (e.key === '[') setVolume(v => Math.max(0, parseFloat((v - 0.1).toFixed(2))));
    if (e.key === ']') setVolume(v => Math.min(1, parseFloat((v + 0.1).toFixed(2))));
    if (e.key === 'm' || e.key === 'M') setMuted(m => !m);
  }, []);

  useEffect(() => {
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [handleKey]);

  if (!visible) return null;

  const VolumeIcon = muted || volume === 0 ? VolumeX : volume < 0.5 ? Volume1 : Volume2;

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-2 bg-[#0a0a0a] border border-noir-border px-4 py-2 shadow-[0_0_30px_rgba(0,0,0,0.8)] border-b-2 border-b-noir-accent">
      <div className="flex items-center gap-3">
        <button
          id="audio-mute-btn"
          onClick={() => setMuted(m => !m)}
          className="text-noir-muted hover:text-noir-accent transition-colors"
          title="M = Mutear"
        >
          <VolumeIcon size={14} className={muted ? 'text-noir-blood' : 'text-noir-muted'} />
        </button>
        
        <div className="relative flex items-center group">
          <input
            type="range"
            min={0}
            max={1}
            step={0.05}
            value={muted ? 0 : volume}
            onChange={e => { setMuted(false); setVolume(parseFloat(e.target.value)); }}
            className="w-20 accent-noir-accent h-[2px] bg-noir-dim cursor-crosshair appearance-none outline-none"
          />
        </div>

        <span className="text-[8px] font-mono tracking-widest text-noir-ink min-w-[20px] text-right">
          {muted ? 'OFF' : `${Math.round(volume * 100)}`}
        </span>
      </div>

      <div className="flex items-center justify-between border-t border-noir-border/30 pt-1.5">
        <div className="flex items-center gap-1.5">
          <Radio size={8} className={`text-noir-accent ${!muted ? 'animate-pulse' : 'opacity-20'}`} />
          <span className="text-[7px] text-noir-muted uppercase tracking-[0.2em] font-mono">
            Track 0{currentTrackIndex + 1}
          </span>
        </div>
        <div className="flex gap-0.5">
          {[...Array(4)].map((_, i) => (
            <div 
              key={i} 
              className={`w-1 h-1 ${i === currentTrackIndex ? 'bg-noir-accent' : 'bg-noir-border'}`} 
            />
          ))}
        </div>
      </div>
    </div>
  );
}
