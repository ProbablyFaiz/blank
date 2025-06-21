import React, { useState } from "react";
import { CTA } from "./features/home/CTA";
import { Features } from "./features/home/Features";
import { Footer } from "./features/home/Footer";
import { Hero } from "./features/home/Hero";
import { Navigation } from "./features/home/Navigation";

const App: React.FC = () => {
  const [email, setEmail] = useState("");
  const [isSubscribed, setIsSubscribed] = useState(false);

  const handleSubscribe = () => {
    if (email) {
      setIsSubscribed(true);
      setEmail("");
      setTimeout(() => setIsSubscribed(false), 3000);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <Navigation />
      <Hero
        email={email}
        setEmail={setEmail}
        isSubscribed={isSubscribed}
        handleSubscribe={handleSubscribe}
      />
      <Features />
      <CTA
        email={email}
        setEmail={setEmail}
        isSubscribed={isSubscribed}
        handleSubscribe={handleSubscribe}
      />
      <Footer />
    </div>
  );
};

export default App;
