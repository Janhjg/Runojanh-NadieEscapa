'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Database, Brain, Tag, BookOpen, Archive, Shield, Home } from 'lucide-react';

export default function NavBar() {
  const pathname = usePathname();

  // Ocultar barra en la pantalla de inicio (splash)
  if (pathname === '/') return null;

  const getAccentColor = (path: string) => {
    switch (path) {
      case '/predict': return 'text-blue-500 border-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.3)] bg-blue-950/20';
      case '/classify': return 'text-purple-500 border-purple-500 shadow-[0_0_15px_rgba(168,85,247,0.3)] bg-purple-950/20';
      case '/narrate': return 'text-amber-500 border-amber-500 shadow-[0_0_15px_rgba(245,158,11,0.3)] bg-amber-950/20';
      case '/full-case': return 'text-green-500 border-green-500 shadow-[0_0_15px_rgba(34,197,94,0.3)] bg-green-950/20';
      case '/new-case': return 'text-red-500 border-red-500 shadow-[0_0_15px_rgba(239,68,68,0.3)] bg-red-950/20';
      case '/crimes': return 'text-gray-300 border-gray-500 bg-gray-900/30';
      default: return 'text-white border-transparent hover:border-gray-800';
    }
  };

  const navLinks = [
    { href: '/crimes', label: 'Archivos', icon: Database },
    { href: '/predict', label: 'Predicción', icon: Brain },
    { href: '/classify', label: 'Clasificar', icon: Tag },
    { href: '/narrate', label: 'Narrativa', icon: BookOpen },
    { href: '/full-case', label: 'Full Case', icon: Archive },
  ];

  return (
    <>
      <nav className="border-b border-gray-900 bg-black sticky top-0 z-40 relative">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-red-600 via-red-900 to-red-600 opacity-80" />
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center h-auto min-h-[60px] py-4 md:py-0 gap-4">
            
            <Link href="/menu" className="flex items-center gap-3 group">
              <div className="w-10 h-10 border border-gray-800 flex items-center justify-center transition-all group-hover:border-red-600 bg-black">
                <Shield size={20} className="text-red-600 group-hover:animate-pulse" />
              </div>
              <div className="flex flex-col">
                <span className="font-black text-xl uppercase tracking-widest text-white leading-none" style={{ fontFamily: 'var(--font-noir)' }}>
                  RUNOJANH
                </span>
                <span className="text-[10px] text-gray-500 uppercase tracking-widest leading-none mt-1 group-hover:text-red-400 transition-colors">
                  Nadie Escapa · CPD
                </span>
              </div>
            </Link>

            <div className="flex items-center gap-2 overflow-x-auto w-full md:w-auto pb-2 md:pb-0">
              <Link
                href="/menu"
                className={`flex items-center gap-2 px-4 py-2 border-b-2 text-sm uppercase font-bold tracking-wider transition-all
                  ${pathname === '/menu' ? 'border-red-600 text-white bg-red-950/20' : 'border-transparent text-gray-500 hover:text-white hover:bg-gray-900'}`}
              >
                <Home size={16} /> Hub
              </Link>
              
              {navLinks.map((link) => {
                const Icon = link.icon;
                const isActive = pathname === link.href;
                const activeStyle = getAccentColor(link.href);
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={`flex items-center gap-2 px-4 py-2 border-b-2 text-sm uppercase font-bold tracking-wider transition-all
                      ${isActive ? activeStyle : 'border-transparent text-gray-500 hover:text-white hover:bg-gray-900'}`}
                  >
                    <Icon size={16} className={isActive ? '' : 'text-gray-600'} />
                    <span className="whitespace-nowrap">{link.label}</span>
                  </Link>
                );
              })}
            </div>

            <div className="hidden md:flex items-center gap-3 border border-gray-800 bg-[#050505] px-4 py-1.5 rounded-sm">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-xs font-mono uppercase tracking-[0.2em] text-gray-400 font-bold">Lvl 4 Access</span>
            </div>
          </div>
        </div>
      </nav>
    </>
  );
}
