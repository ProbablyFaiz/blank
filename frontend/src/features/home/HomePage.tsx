import type React from "react";
import { useState } from "react";
import { CTA } from "./CTA";
import { Features } from "./Features";
import { Hero } from "./Hero";

const HomePage: React.FC = () => {
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
    <>
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
    </>
  );
};

export default HomePage;
