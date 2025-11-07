import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Shield, Zap, Clock, Headphones, Globe, Lock } from 'lucide-react';

const FEATURES = [
  {
    icon: Shield,
    title: 'DDoS Захист',
    description: 'Надійний захист від DDoS атак для безперебійної роботи вашого сервера'
  },
  {
    icon: Zap,
    title: 'Висока продуктивність',
    description: 'Потужне обладнання та оптимізована мережа для максимальної швидкості'
  },
  {
    icon: Clock,
    title: 'Миттєва активація',
    description: 'Ваш сервер буде готовий до роботи протягом декількох хвилин'
  },
  {
    icon: Headphones,
    title: 'Підтримка 24/7',
    description: 'Наша команда завжди готова допомогти вам у будь-який час доби'
  },
  {
    icon: Globe,
    title: 'Глобальна мережа',
    description: 'Дата-центри по всьому світу для найкращого підключення'
  },
  {
    icon: Lock,
    title: 'Повний контроль',
    description: 'Root доступ та повна свобода у налаштуванні вашого сервера'
  }
];

export default function FeaturesSection() {
  return (
    <section className="relative py-24 px-4">
      <div className="container mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16 space-y-4">
          <h2 className="text-4xl sm:text-5xl font-bold">
            <span className="text-foreground">Чому обирають </span>
            <span className="bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
              нас?
            </span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Професійний хостинг з найкращими характеристиками на ринку
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {FEATURES.map((feature, index) => (
            <Card
              key={index}
              className="glass-card border-primary/20 hover:border-primary/50 transition-all duration-300 group"
            >
              <CardHeader className="space-y-4">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center group-hover:scale-110 transition-transform duration-300 shadow-glow">
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
