'use client';

import { useEffect, useRef, useState, useCallback } from 'react';

const TRACKS = [
  '/audio/bg_1.mp3',
  '/audio/bg_2.mp3',
  '/audio/bg_3.mp3',
  '/audio/bg_4.mp3'
];

const SESSION_KEY_ACTIVE = 'runojanh-music-started';
const SESSION_KEY_PLAYING = 'runojanh-music-playing';
const TRACK_NAMES = ['CASE FILE I', 'CASE FILE II', 'CASE FILE III', 'CASE FILE IV'];

export default function AudioManager() {
  const musicRef = useRef<HTMLAudioElement | null>(null);
  const [volume, setVolume] = useState(0.35);
  const [playing, setPlaying] = useState(false);
  const [visible, setVisible] = useState(false);
  const [currentTrackIndex, setCurrentTrackIndex] = useState(0);
  const [bars, setBars] = useState([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]);
  const startedRef = useRef(false);
  
  const volumeRef = useRef(0.35);
  const playingRef = useRef(false);

  useEffect(() => { volumeRef.current = volume; }, [volume]);
  useEffect(() => { 
    playingRef.current = playing;
    sessionStorage.setItem(SESSION_KEY_PLAYING, playing ? 'true' : 'false');
  }, [playing]);

  // Animación de barras sincronizada con el estado de reproducción
  useEffect(() => {
    if (!playing || !visible) {
      setBars(prev => prev.map(() => 1));
      return;
    }
    const interval = setInterval(() => {
      setBars(() => Array.from({ length: 10 }, () => Math.floor(Math.random() * 9) + 1));
    }, 180);
    return () => clearInterval(interval);
  }, [playing, visible]);

  const startPlayback = useCallback((trackIdx: number) => {
    // Si ya hay un audio, lo limpiamos
    if (musicRef.current) {
      musicRef.current.pause();
      musicRef.current.src = '';
      musicRef.current.load();
    }
    
    const audio = new Audio(TRACKS[trackIdx]);
    audio.loop = false;
    audio.volume = volumeRef.current;
    
    audio.addEventListener('ended', () => {
      setCurrentTrackIndex(prev => (prev + 1) % TRACKS.length);
    });

    musicRef.current = audio;
    
    // Solo reproducimos si el estado global es "playing"
    if (playingRef.current) {
      audio.play().catch(err => {
        console.warn("Audio autoplay blocked or failed:", err);
      });
    }
    
    setVisible(true);
  }, []);

  const handleTogglePlay = () => {
    const nextState = !playing;
    setPlaying(nextState);
    playingRef.current = nextState;
    
    if (musicRef.current) {
      if (nextState) {
        musicRef.current.play().catch(() => {});
      } else {
        musicRef.current.pause();
      }
    }
  };

  const handleVolumeChange = (newVol: number) => {
    setVolume(newVol);
    volumeRef.current = newVol;
    if (musicRef.current) {
      musicRef.current.volume = newVol;
    }
  };

  useEffect(() => {
    // Si es la primera vez o volvemos al sitio, forzamos el inicio de la música
    // (A menos que el detective la haya detenido explícitamente antes en esta sesión)
    const wasStarted = sessionStorage.getItem(SESSION_KEY_ACTIVE) === 'true';
    const wasPlayingManual = sessionStorage.getItem(SESSION_KEY_PLAYING) !== 'false'; 

    const initMusic = () => {
      if (!startedRef.current) {
        startedRef.current = true;
        sessionStorage.setItem(SESSION_KEY_ACTIVE, 'true');
        setPlaying(true);
        playingRef.current = true;
        startPlayback(0);
      }
    };

    // Forzar el inicio al montar (apenas se abre el sitio)
    if (!startedRef.current) {
      initMusic();
    }

    window.addEventListener('runojanh:start-music', initMusic);
    return () => window.removeEventListener('runojanh:start-music', initMusic);
  }, [startPlayback]);

  // Cambio de pista
  useEffect(() => {
    if (startedRef.current) {
      startPlayback(currentTrackIndex);
    }
  }, [currentTrackIndex, startPlayback]);

  const handleKey = useCallback((e: KeyboardEvent) => {
    if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
    if (e.key === '[') handleVolumeChange(Math.max(0, parseFloat((volumeRef.current - 0.1).toFixed(2))));
    if (e.key === ']') handleVolumeChange(Math.min(1, parseFloat((volumeRef.current + 0.1).toFixed(2))));
    if (e.key === 'm' || e.key === 'M' || e.key === ' ') {
      e.preventDefault();
      handleTogglePlay();
    }
  }, []);

  useEffect(() => {
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [handleKey]);

  if (!visible) return null;

  const volBlocks = Math.round(volume * 8);

  return (
    <div
      className="fixed bottom-0 right-0 z-50 select-none animate-in fade-in slide-in-from-right duration-700"
      style={{ clipPath: 'polygon(20px 0, 100% 0, 100% 100%, 0 100%)' }}
    >
      <div
        className="flex items-center gap-4 bg-[#050505] border-l border-t border-[#3a0000] px-5 pl-8 py-2"
        style={{ boxShadow: '-6px -4px 30px rgba(153,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.02)' }}
      >
        {/* Status LED */}
        <div className="flex flex-col items-center gap-1">
          <div className={`w-1.5 h-1.5 rounded-full transition-all duration-500 ${!playing ? 'bg-[#2a0000]' : 'bg-red-600 shadow-[0_0_8px_rgba(220,38,38,0.8)]'}`} />
          <span className="text-[6px] font-mono text-[#3a0000] tracking-widest uppercase">
            {playing ? 'SIGNAL' : 'STANDBY'}
          </span>
        </div>

        {/* Separator */}
        <div className="w-px h-8 bg-[#1a0000]" />

        {/* EQ Bars */}
        <div className="flex items-end gap-[2px] h-7 w-[40px] justify-center">
          {bars.map((h, i) => (
            <div
              key={i}
              className="w-[2px] transition-all duration-200"
              style={{
                height: `${h * 2.5}px`,
                background: !playing
                  ? '#1a0000'
                  : h > 6
                    ? '#dc2626'
                    : h > 3
                      ? '#991b1b'
                      : '#5c0a0a',
                boxShadow: playing && h > 7 ? '0 0 4px rgba(220,38,38,0.4)' : 'none',
              }}
            />
          ))}
        </div>

        {/* Separator */}
        <div className="w-px h-8 bg-[#1a0000]" />

        {/* Track Info */}
        <div className="flex flex-col gap-0.5 min-w-[80px]">
          <span className="text-[7px] font-mono tracking-[0.2em] text-[#5c0a0a] uppercase">SYSTEM.BGM</span>
          <span className="text-[8px] font-mono tracking-widest text-red-900 font-bold truncate max-w-[100px]">
            {playing ? TRACK_NAMES[currentTrackIndex] : '--- STOPPED ---'}
          </span>
        </div>

        {/* Separator */}
        <div className="w-px h-8 bg-[#1a0000]" />

        {/* Volume Blocks */}
        <div className="flex flex-col gap-1">
          <span className="text-[6px] font-mono text-[#3a0000] uppercase tracking-widest">OUTPUT</span>
          <div className="flex gap-[2px] items-center">
            {[...Array(8)].map((_, i) => (
              <div
                key={i}
                className="w-[3px] h-2.5 transition-all"
                style={{
                  background: i < volBlocks
                    ? (i > 5 ? '#dc2626' : '#7f1d1d')
                    : '#1a0000',
                }}
              />
            ))}
          </div>
        </div>

        {/* Volume Slider */}
        <div className="flex flex-col gap-1 ml-1">
          <input
            type="range"
            min={0}
            max={1}
            step={0.05}
            value={volume}
            onChange={e => handleVolumeChange(parseFloat(e.target.value))}
            className="w-16 h-[2px] cursor-crosshair appearance-none outline-none"
            style={{ accentColor: '#991b1b', background: '#1a0000' }}
          />
        </div>

        {/* Separator */}
        <div className="w-px h-8 bg-[#1a0000]" />

        {/* Play/Stop Button */}
        <button
          onClick={handleTogglePlay}
          className={`
            text-[9px] font-mono uppercase tracking-widest border px-3 py-1 transition-all duration-300
            ${!playing 
              ? 'border-red-900 text-red-900 hover:bg-red-900/10' 
              : 'border-red-600 text-red-600 bg-red-600/5 hover:bg-red-600/20 shadow-[0_0_10px_rgba(220,38,38,0.1)]'
            }
          `}
          title={playing ? 'Space = Detener' : 'Space = Reproducir'}
        >
          {playing ? 'STOP' : 'PLAY'}
        </button>
      </div>
    </div>
  );
}
