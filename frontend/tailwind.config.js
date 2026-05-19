/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "page-bg": "#F6F7F9",
        "card-surface": "#FFFFFF",
        "border-subtle": "#E9E9EB",
        "text-muted": "#7C7E8C",
        "on-surface": "#171a2c",
        primary: "#006c4f",
        "primary-container": "#00d09c",
        "primary-hover": "#00B88A",
        secondary: "#5f5e60",
        "status-success": "#00D09C",
        "status-warning": "#F5A623",
        "status-error": "#DF514C",
        "status-info": "#5367FF",
        "surface-container-low": "#f3f2ff",
        "surface-bright": "#fbf8ff",
        "surface-container-lowest": "#ffffff",
        "on-primary-container": "#00533c",
        "error-container": "#ffdad6",
        "on-error-container": "#93000a",
        groww: {
          primary: "#00D09C",
          "primary-hover": "#00B88A",
          dark: "#1D1D1F",
          body: "#44475B",
          muted: "#7C7E8C",
          bg: "#F6F7F9",
          border: "#E9E9EB",
        },
      },
      spacing: {
        gutter: "24px",
        "sidebar-width": "240px",
        "card-padding": "24px",
        "max-content": "1200px",
      },
      fontSize: {
        "headline-xl": ["28px", { lineHeight: "36px", letterSpacing: "-0.02em", fontWeight: "600" }],
        "headline-md": ["20px", { lineHeight: "28px", letterSpacing: "-0.01em", fontWeight: "600" }],
        "body-lg": ["16px", { lineHeight: "24px", fontWeight: "400" }],
        "body-md": ["14px", { lineHeight: "21px", fontWeight: "400" }],
        "label-md": ["12px", { lineHeight: "16px", letterSpacing: "0.01em", fontWeight: "500" }],
        caption: ["12px", { lineHeight: "16px", fontWeight: "400" }],
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 3px rgba(0,0,0,0.06)",
        elevated: "0 4px 12px rgba(0,0,0,0.1)",
      },
      maxWidth: {
        content: "1200px",
      },
    },
  },
  plugins: [],
};
