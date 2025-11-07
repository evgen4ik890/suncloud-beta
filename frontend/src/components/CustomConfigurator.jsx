import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Label } from '@/components/ui/label';
import { Cpu, Database, HardDrive, Network, Archive, Sparkles } from 'lucide-react';

const PRICING = {
  core: 24,
  ram: 24,
  disk: 1,
  port: 2,
  backup: 8
};

const MAX_VALUES = {
  cores: 16,
  ram: 64,
  disk: 200,
  ports: 10,
  backups: 10
};

export default function CustomConfigurator() {
  const [config, setConfig] = useState({
    cores: 4,
    ram: 8,
    disk: 50,
    ports: 2,
    backups: 2
  });

  const calculatePrice = () => {
    return (
      config.cores * PRICING.core +
      config.ram * PRICING.ram +
      config.disk * PRICING.disk +
      config.ports * PRICING.port +
      config.backups * PRICING.backup
    );
  };

  const handleSliderChange = (key, value) => {
    setConfig(prev => ({ ...prev, [key]: value[0] }));
  };

  const price = calculatePrice();

  return (
    <section id="configurator" className="relative py-24 px-4">
      <div className="container mx-auto max-w-6xl">
        {/* Section Header */}
        <div className="text-center mb-16 space-y-4">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card border border-accent/30 backdrop-blur-xl mb-4">
            <Sparkles className="w-4 h-4 text-accent" />
            <span className="text-sm font-medium text-foreground">Конфігуратор</span>
          </div>
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-bold">
            <span className="bg-gradient-to-r from-accent via-primary to-accent bg-clip-text text-transparent">
              Створіть свій план
            </span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Налаштуйте конфігурацію сервера під ваші потреби
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Configurator Panel */}
          <Card className="glass-card border-primary/30">
            <CardHeader>
              <CardTitle className="text-2xl">Налаштування сервера</CardTitle>
              <CardDescription className="text-base">Налаштуйте параметри вашого сервера</CardDescription>
            </CardHeader>
            <CardContent className="space-y-8">
              {/* CPU Cores */}
              <ConfigSlider
                icon={Cpu}
                label="Ядра процесора"
                value={config.cores}
                max={MAX_VALUES.cores}
                unit="ядер"
                price={config.cores * PRICING.core}
                onChange={(value) => handleSliderChange('cores', value)}
              />

              {/* RAM */}
              <ConfigSlider
                icon={Database}
                label="Оперативна пам'ять"
                value={config.ram}
                max={MAX_VALUES.ram}
                unit="ГБ"
                price={config.ram * PRICING.ram}
                onChange={(value) => handleSliderChange('ram', value)}
              />

              {/* Disk Space */}
              <ConfigSlider
                icon={HardDrive}
                label="Дисковий простір"
                value={config.disk}
                max={MAX_VALUES.disk}
                unit="ГБ"
                price={config.disk * PRICING.disk}
                onChange={(value) => handleSliderChange('disk', value)}
              />

              {/* Ports */}
              <ConfigSlider
                icon={Network}
                label="Додаткові порти"
                value={config.ports}
                max={MAX_VALUES.ports}
                unit="портів"
                price={config.ports * PRICING.port}
                onChange={(value) => handleSliderChange('ports', value)}
              />

              {/* Backups */}
              <ConfigSlider
                icon={Archive}
                label="Резервні копії"
                value={config.backups}
                max={MAX_VALUES.backups}
                unit="бекапів"
                price={config.backups * PRICING.backup}
                onChange={(value) => handleSliderChange('backups', value)}
              />
            </CardContent>
          </Card>

          {/* Price Summary */}
          <div className="space-y-6">
            <Card className="glass-card border-accent/30 sticky top-8">
              <CardHeader>
                <CardTitle className="text-2xl">Підсумок замовлення</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Configuration Summary */}
                <div className="space-y-4">
                  <SummaryItem label="Ядра CPU" value={`${config.cores} x 24 ₽`} total={config.cores * PRICING.core} />
                  <SummaryItem label="Оперативна пам'ять" value={`${config.ram} ГБ x 24 ₽`} total={config.ram * PRICING.ram} />
                  <SummaryItem label="Дисковий простір" value={`${config.disk} ГБ x 1 ₽`} total={config.disk * PRICING.disk} />
                  <SummaryItem label="Додаткові порти" value={`${config.ports} x 2 ₽`} total={config.ports * PRICING.port} />
                  <SummaryItem label="Резервні копії" value={`${config.backups} x 8 ₽`} total={config.backups * PRICING.backup} />
                </div>

                {/* Total Price */}
                <div className="pt-6 border-t border-border">
                  <div className="flex items-baseline justify-between mb-2">
                    <span className="text-lg font-medium text-muted-foreground">Загальна вартість</span>
                  </div>
                  <div className="text-5xl font-bold bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
                    {price} ₽
                    <span className="text-xl text-muted-foreground">/міс</span>
                  </div>
                </div>

                {/* Features Included */}
                <div className="pt-4 space-y-2 text-sm">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <div className="w-1.5 h-1.5 rounded-full bg-accent"></div>
                    <span>DDoS захист включено</span>
                  </div>
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <div className="w-1.5 h-1.5 rounded-full bg-accent"></div>
                    <span>Миттєва активація</span>
                  </div>
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <div className="w-1.5 h-1.5 rounded-full bg-accent"></div>
                    <span>Підтримка 24/7</span>
                  </div>
                </div>
              </CardContent>
              <CardFooter>
                <Button
                  size="lg"
                  className="w-full bg-gradient-to-r from-accent to-primary hover:from-accent/90 hover:to-primary/90 transition-all duration-300 shadow-glow hover:shadow-glow-strong text-base"
                >
                  Замовити конфігурацію
                </Button>
              </CardFooter>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
}

function ConfigSlider({ icon: Icon, label, value, max, unit, price, onChange }) {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/10">
            <Icon className="w-5 h-5 text-primary" />
          </div>
          <Label className="text-base font-medium">{label}</Label>
        </div>
        <div className="text-right">
          <div className="text-lg font-bold text-foreground">
            {value} {unit}
          </div>
          <div className="text-sm text-muted-foreground">{price} ₽</div>
        </div>
      </div>
      <Slider
        value={[value]}
        onValueChange={onChange}
        max={max}
        min={0}
        step={1}
        className="cursor-pointer"
      />
    </div>
  );
}

function SummaryItem({ label, value, total }) {
  return (
    <div className="flex items-center justify-between text-sm">
      <div>
        <div className="font-medium text-foreground">{label}</div>
        <div className="text-muted-foreground">{value}</div>
      </div>
      <div className="font-semibold text-foreground">{total} ₽</div>
    </div>
  );
}
