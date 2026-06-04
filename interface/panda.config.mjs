import { defineConfig } from "@pandacss/dev";

export default defineConfig({
  // Whether to use css reset
  preflight: true,

  // Where to look for your css declarations
  include: ["./src/**/*.{js,jsx,ts,tsx}"],

  // Files to exclude
  exclude: [],

  // Useful for theme customization
  theme: {
    extend: {
      tokens: {
        colors: {
          bg: { value: "#0b0d11" },
          sidebar: { value: "#12141a" },
          card: { value: "#171a21" },
          accent: { value: "#e14e4e" },
          secondary: { value: "#3b82f6" }, // Keeping a secondary blue for validation
          border: { value: "rgba(255, 255, 255, 0.05)" },
          text: {
            primary: { value: "#ffffff" },
            secondary: { value: "#9ba1a6" },
            muted: { value: "#5d636a" },
          },
        },
        fonts: {
          sans: { value: "'Inter', system-ui, sans-serif" },
          mono: { value: "'JetBrains Mono', monospace" },
        },
      },
    },
  },

  // The output directory for your css system
  outdir: "styled-system",
});
