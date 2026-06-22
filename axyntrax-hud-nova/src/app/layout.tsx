import type { Metadata } from "next";
import { Inter, Space_Grotesk } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const inter = Inter({
  variable: "--font-geist-sans", // Keeping variable name for compatibility but using Inter
  subsets: ["latin"],
});

const spaceGrotesk = Space_Grotesk({
  variable: "--font-geist-mono", // Keeping variable name for compatibility but using Space Grotesk
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AXYNTRAX | Omni-Core Neural System",
  description: "Arquitectura autónoma de nivel élite, impulsada por L99.",
};

export const viewport = {
  themeColor: "#020202",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="es"
      className={cn("dark", inter.variable, spaceGrotesk.variable, "h-full antialiased")}
      suppressHydrationWarning
    >
      <body className="min-h-full flex flex-col bg-background text-foreground selection:bg-cyan-l99/30">
        {children}
      </body>
    </html>
  );
}
