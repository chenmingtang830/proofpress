import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { blogPages } from "./scripts/blog-pages.mjs";

export default defineConfig({
  plugins: [react(), blogPages()],
  build: { outDir: "dist", emptyOutDir: true },
});
