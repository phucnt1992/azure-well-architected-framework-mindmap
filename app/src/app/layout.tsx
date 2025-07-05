import type { Metadata } from "next";
import './globals.css';

import { Geist, Geist_Mono } from 'next/font/google';

import { Footer } from '@/components/footer';
import { Header } from '@/components/header';
import { ThemeProvider } from 'next-themes'

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Azure Mind Map",
  description: "Azure Mind Map is a collection of Azure Well-Architected and Azure Docs in a mind map.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ThemeProvider>
          <Header />
          <div className="mx-auto max-w-4xl px-4 pt-16 pb-8">
            {children}
          </div>
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  );
}
