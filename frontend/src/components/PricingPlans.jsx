import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Cpu, HardDrive, Database, Network, Archive, Check } from 'lucide-react';

const PRICING = {
  core: 24,
  ram: 24,
  disk: 1,
  port: 2,
  backup: 8
};

const PLANS = [
  { name: 'Game-1', cores: 1, ram: 1, disk: 10, ports: 0, backups: 0, popular: false },
  { name: 'Game-2', cores: 2, ram: 4, disk: 25, ports: 1, backups: 1, popular: false },
  { name: 'Game-3', cores: 3, ram: 6, disk: 30, ports: 2, backups: 2, popular: true },
  { name: 'Game-4', cores: 4, ram: 8, disk: 50, ports: 3, backups: 3, popular: false },
  { name: 'Game-5', cores: 4, ram: 12, disk: 75, ports: 5, backups: 5, popular: false },
  { name: 'Game-6', cores: 6, ram: 16, disk: 100, ports: 6, backups: 6, popular: false },
  { name: 'Game-7', cores: 8, ram: 24, disk: 125, ports: 8, backups: 8, popular: false },
  { name: 'Game-8', cores: 8, ram: 32, disk: 150, ports: 9, backups: 9, popular: false },
  { name: 'Game-9', cores: 10, ram: 48, disk: 175, ports: 10, backups: 10, popular: false }
];

const calculatePrice = (plan) => {
  return (
    plan.cores * PRICING.core +
    plan.ram * PRICING.ram +
    plan.disk * PRICING.disk +
    plan.ports * PRICING.port +
    plan.backups * PRICING.backup
  );
};

export default function PricingPlans() {
  const [hoveredPlan, setHoveredPlan] = useState(null);

  return (
    <section id="pricing-plans" className="relative py-24 px-4">
      <div className="container mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16 space-y-4">
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-bold">
            <span className="bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
              Тарифні плани
            </span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Оберіть ідеальний план для вашого ігрового сервера
          </p>
        </div>

        {/* Plans Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {PLANS.map((plan, index) => {
            const price = calculatePrice(plan);
            const isHovered = hoveredPlan === index;

            return (
              <Card
                key={index}
                className={`glass-card glass-card-hover relative overflow-hidden transition-all duration-300 ${
                  plan.popular ? 'ring-2 ring-primary' : ''
                }`}
                onMouseEnter={() => setHoveredPlan(index)}
                onMouseLeave={() => setHoveredPlan(null)}
              >
                {/* Popular Badge */}
                {plan.popular && (
                  <div className="absolute top-4 right-4">
                    <Badge className="bg-gradient-to-r from-primary to-accent border-none text-white shadow-glow">
                      Популярний
                    </Badge>
                  </div>
                )}

                {/* Glow Effect on Hover */}
                {isHovered && (
                  <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-accent/5 to-transparent pointer-events-none"></div>
                )}

                <CardHeader className="space-y-4 relative z-10">
                  <CardTitle className="text-2xl font-bold text-foreground">{plan.name}</CardTitle>
                  <div className="space-y-2">
                    <div className="text-4xl font-bold text-primary">
                      {price} ₽
                      <span className="text-base font-normal text-muted-foreground">/міс</span>
                    </div>
                  </div>
                </CardHeader>

                <CardContent className="space-y-4 relative z-10">
                  <div className="space-y-3">
                    <SpecItem icon={Cpu} label="Ядра CPU" value={`${plan.cores} ${plan.cores === 1 ? 'ядро' : 'ядра'}`} />
                    <SpecItem icon={Database} label="Оперативна пам'ять" value={`${plan.ram} ГБ`} />
                    <SpecItem icon={HardDrive} label="Дисковий простір" value={`${plan.disk} ГБ`} />
                    <SpecItem icon={Network} label="Додаткові порти" value={plan.ports} />
                    <SpecItem icon={Archive} label="Резервні копії" value={plan.backups} />
                  </div>

                  {/* Features */}
                  <div className="pt-4 border-t border-border/50 space-y-2">
                    <FeatureItem text="DDoS захист" />
                    <FeatureItem text="Миттєва активація" />
                    <FeatureItem text="Повний root доступ" />
                  </div>
                </CardContent>

                <CardFooter className="relative z-10 mt-auto">
                  <Button
                    className="w-full bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 transition-all duration-300 shadow-lg hover:shadow-glow"
                    size="lg"
                  >
                    Замовити
                  </Button>
                </CardFooter>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
}

function SpecItem({ icon: Icon, label, value }) {
  return (
    <div className="flex items-center justify-between group">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-lg bg-primary/10 group-hover:bg-primary/20 transition-colors">
          <Icon className="w-4 h-4 text-primary" />
        </div>
        <span className="text-sm text-muted-foreground">{label}</span>
      </div>
      <span className="text-sm font-semibold text-foreground">{value}</span>
    </div>
  );
}

function FeatureItem({ text }) {
  return (
    <div className="flex items-center gap-2">
      <Check className="w-4 h-4 text-accent" />
      <span className="text-sm text-foreground">{text}</span>
    </div>
  );
}
