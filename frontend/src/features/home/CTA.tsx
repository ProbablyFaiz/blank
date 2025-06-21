import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Mail } from "lucide-react";
import React from "react";

interface CTAProps {
  email: string;
  setEmail: (email: string) => void;
  isSubscribed: boolean;
  handleSubscribe: () => void;
}

export const CTA: React.FC<CTAProps> = ({
  email,
  setEmail,
  isSubscribed,
  handleSubscribe,
}) => {
  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-white mb-6">
          Ready to Get Started?
        </h2>
        <p className="text-lg text-slate-600 dark:text-slate-300 mb-8">
          Join thousands of developers who are already building amazing things.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <div className="flex space-x-2">
            <Input
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-80"
            />
            <Button onClick={handleSubscribe} disabled={!email || isSubscribed}>
              <Mail className="mr-2 h-4 w-4" />
              {isSubscribed ? "✓ Subscribed!" : "Get Updates"}
            </Button>
          </div>
        </div>
        {isSubscribed && (
          <p className="text-green-600 dark:text-green-400 mt-4 font-medium">
            Thanks for subscribing! We'll keep you updated.
          </p>
        )}
      </div>
    </section>
  );
};
