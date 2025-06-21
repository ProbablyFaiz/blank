import { ArrowRight, Github } from "lucide-react";
import type React from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";

interface HeroProps {
  email: string;
  setEmail: (email: string) => void;
  isSubscribed: boolean;
  handleSubscribe: () => void;
}

export const Hero: React.FC<HeroProps> = ({
  email,
  setEmail,
  isSubscribed,
  handleSubscribe,
}) => {
  return (
    <section className="relative py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto text-center">
        <Badge variant="secondary" className="mb-4">
          ✨ New features available now
        </Badge>
        <h1 className="text-4xl sm:text-6xl font-bold text-slate-900 dark:text-white mb-6">
          Build Beautiful Apps
          <br />
          <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            That Users Love
          </span>
        </h1>
        <p className="text-xl text-slate-600 dark:text-slate-300 mb-8 max-w-3xl mx-auto">
          Create stunning applications with our modern component library. Fast,
          accessible, and beautifully designed out of the box.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Dialog>
            <DialogTrigger asChild>
              <Button size="lg" className="group">
                Start Building
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Welcome to Blank!</DialogTitle>
                <DialogDescription>
                  Join thousands of developers building amazing applications.
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-4 pt-4">
                <div className="flex space-x-2">
                  <Input
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="flex-1"
                  />
                  <Button
                    onClick={handleSubscribe}
                    disabled={!email || isSubscribed}
                  >
                    {isSubscribed ? "✓ Subscribed!" : "Subscribe"}
                  </Button>
                </div>
                <p className="text-sm text-slate-500">
                  Get updates on new components and features.
                </p>
              </div>
            </DialogContent>
          </Dialog>
          <Button variant="outline" size="lg">
            <Github className="mr-2 h-4 w-4" />
            View on GitHub
          </Button>
        </div>
      </div>
    </section>
  );
};
