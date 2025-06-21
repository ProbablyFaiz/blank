import { createRootRoute, Outlet } from "@tanstack/react-router";
import { Footer } from "@/features/home/Footer";
import { Navigation } from "@/features/home/Navigation";

export const Route = createRootRoute({
  component: () => (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <Navigation />
      <Outlet />
      <Footer />
    </div>
  ),
});
