import { Link } from "@tanstack/react-router";
import { ArrowLeft, Code, Coffee, Heart } from "lucide-react";
import type React from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const AboutPage: React.FC = () => {
  return (
    <div className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <Link to="/">
            <Button variant="outline" size="sm" className="mb-6">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Home
            </Button>
          </Link>
          <Badge variant="secondary" className="mb-4">
            About Us
          </Badge>
          <h1 className="text-4xl sm:text-5xl font-bold text-slate-900 dark:text-white mb-6">
            About Blank
          </h1>
          <p className="text-xl text-slate-600 dark:text-slate-300 mb-8">
            Building the future of web development, one component at a time.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          <Card>
            <CardHeader>
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center text-blue-600 dark:text-blue-400 mb-4">
                <Heart className="h-6 w-6" />
              </div>
              <CardTitle>Our Mission</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-base">
                We believe that great software should be accessible to everyone.
                Our mission is to provide developers with beautiful, functional
                components that make building amazing applications effortless.
              </CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center text-green-600 dark:text-green-400 mb-4">
                <Code className="h-6 w-6" />
              </div>
              <CardTitle>Our Values</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-base">
                Quality, simplicity, and developer experience are at the core of
                everything we do. We're committed to creating tools that
                developers love to use.
              </CardDescription>
            </CardContent>
          </Card>
        </div>

        <div className="text-center bg-slate-50 dark:bg-slate-800 rounded-lg p-8">
          <Coffee className="h-12 w-12 text-amber-600 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">
            Built with Care
          </h2>
          <p className="text-lg text-slate-600 dark:text-slate-300 mb-6">
            Every component is crafted with attention to detail, tested
            thoroughly, and designed to work seamlessly with your existing
            codebase.
          </p>
          <Link to="/">
            <Button size="lg">Explore Components</Button>
          </Link>
        </div>

        <div className="mt-12 text-center">
          <p className="text-slate-500 dark:text-slate-400">
            Have questions? We'd love to hear from you.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;
