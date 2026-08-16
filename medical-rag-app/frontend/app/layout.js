// ============================================================================
// ROOT LAYOUT
// ----------------------------------------------------------------------------
// Loads the three fonts used across the app via next/font (self-hosted,
// no external request at runtime) and wraps every page in the base HTML
// shell + global styles.
// ============================================================================

import { Space_Grotesk, Inter, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";

const displayFont = Space_Grotesk({
  subsets: ["latin"],
  weight: ["500", "600", "700"],
  variable: "--font-display",
});

const bodyFont = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-body",
});

const monoFont = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono",
});

export const metadata = {
  title: "MedGrounded — Document-Grounded Medical Assistant",
  description: "Ask questions answered only from the medical PDFs you upload.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${displayFont.variable} ${bodyFont.variable} ${monoFont.variable}`}>
      <body className="font-body bg-bg text-ink h-screen overflow-hidden flex flex-col">
        {children}
      </body>
    </html>
  );
}
