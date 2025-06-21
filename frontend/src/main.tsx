import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { client } from "@/client/client.gen";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 10000,
    },
  },
});

const API_BASE_URL = import.meta.env.VITE_BLANK_API_URL;

if (!API_BASE_URL) {
  throw new Error("VITE_BLANK_API_URL is not set");
}

client.setConfig({
  baseURL: API_BASE_URL,
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>,
);
