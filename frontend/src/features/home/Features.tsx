import { useQuery } from "@tanstack/react-query";
import { Shield, Users, Zap } from "lucide-react";
import type React from "react";
import { readProxyPatternOptions } from "@/client/@tanstack/react-query.gen";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const features = [
  {
    id: "lightning-fast",
    icon: <Zap className="h-6 w-6" />,
    title: "Lightning Fast",
    description:
      "Built with modern technologies for optimal performance and speed.",
  },
  {
    id: "secure-by-default",
    icon: <Shield className="h-6 w-6" />,
    title: "Secure by Default",
    description:
      "Enterprise-grade security with end-to-end encryption and privacy protection.",
  },
  {
    id: "team-collaboration",
    icon: <Users className="h-6 w-6" />,
    title: "Team Collaboration",
    description:
      "Work together seamlessly with real-time collaboration features.",
  },
];

export const Features: React.FC = () => {
  const { data: patterns } = useQuery({
    ...readProxyPatternOptions({
      path: {
        pattern_id: 1,
      },
    }),
  });

  console.log(patterns);

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-white mb-4">
            Why Choose Blank?
          </h2>
          <p className="text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
            Everything you need to build modern applications, from small
            projects to enterprise solutions.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature) => (
            <Card
              id={feature.id}
              key={feature.id}
              className="group hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
            >
              <CardHeader>
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center text-blue-600 dark:text-blue-400 mb-4 group-hover:scale-110 transition-transform">
                  {feature.icon}
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};
