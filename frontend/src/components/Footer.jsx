import React from 'react';
import { Server } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="relative border-t border-border/50 py-12 px-4">
      <div className="container mx-auto">
        <div className="flex flex-col items-center space-y-6">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-glow">
              <Server className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              GameHost
            </span>
          </div>

          {/* Links */}
          <div className="flex flex-wrap justify-center gap-6 text-sm text-muted-foreground">
            <a href="#" className="hover:text-primary transition-colors">Про нас</a>
            <a href="#" className="hover:text-primary transition-colors">Документація</a>
            <a href="#" className="hover:text-primary transition-colors">Підтримка</a>
            <a href="#" className="hover:text-primary transition-colors">Контакти</a>
          </div>

          {/* Copyright */}
          <div className="text-center text-sm text-muted-foreground pt-6 border-t border-border/50 w-full">
            <p>© 2024 GameHost. Всі права захищені.</p>
          </div>
        </div>
      </div>
    </footer>
  );
}
