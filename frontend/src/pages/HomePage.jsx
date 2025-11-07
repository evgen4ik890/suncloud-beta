import React from 'react';
import HeroSection from '@/components/HeroSection';
import PricingPlans from '@/components/PricingPlans';
import CustomConfigurator from '@/components/CustomConfigurator';
import FeaturesSection from '@/components/FeaturesSection';
import Footer from '@/components/Footer';

export default function HomePage() {
  return (
    <div className="min-h-screen">
      <HeroSection />
      <PricingPlans />
      <CustomConfigurator />
      <FeaturesSection />
      <Footer />
    </div>
  );
}
