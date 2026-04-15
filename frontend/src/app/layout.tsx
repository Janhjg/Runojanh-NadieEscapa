import type { Metadata } from "next";
import { Inter, Special_Elite } from "next/font/google";
import "./globals.css";
import AudioManager from "@/components/AudioManager";
import SoundManager from "@/components/SoundManager";
import NavBar from "@/components/NavBar";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const specialElite = Special_Elite({
  variable: "--font-noir",
  subsets: ["latin"],
  weight: "400",
});

export const metadata: Metadata = {
  title: "Runojanh - Nadie Escapa",
  description: "Detective Terminal for Crime Analysis and Noir Chronicles",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="es"
      className={`${inter.variable} ${specialElite.variable} h-full antialiased`}
    >
      <body className="min-h-full bg-noir-bg text-noir-fore flex flex-col relative">
        <AudioManager />
        <SoundManager />
        <NavBar />
        {children}
      </body>
    </html>
  );
}
