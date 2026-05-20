/** @type {import('tailwindcss').Config} */
/** Tokens from doc/stitch pulse 6/DESIGN.md */
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
        "primary-fixed": "#2fe0aa",
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
        "secondary-fixed-dim": "#c8c6c8",
        background: "#fbf8ff",
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
        gutter: "32px",
        "sidebar-width": "260px",
        "card-padding": "28px",
        "max-content": "1200px",
      },
      fontSize: {
        "headline-xl": ["32px", { lineHeight: "40px", letterSpacing: "-0.03em", fontWeight: "800" }],
        "headline-md": ["22px", { lineHeight: "30px", letterSpacing: "-0.02em", fontWeight: "700" }],
        "body-lg": ["16px", { lineHeight: "24px", fontWeight: "400" }],
        "body-md": ["14px", { lineHeight: "21px", fontWeight: "400" }],
        "label-md": ["12px", { lineHeight: "16px", letterSpacing: "0.02em", fontWeight: "600" }],
        caption: ["12px", { lineHeight: "16px", fontWeight: "400" }],
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 3px rgba(0,0,0,0.06)",
        elevated: "0 4px 12px rgba(0,0,0,0.1)",
        stitch: "0 20px 25px -5px rgba(23, 26, 44, 0.05), 0 8px 10px -6px rgba(23, 26, 44, 0.05)",
        "success-glow": "0 0 12px rgba(0, 208, 156, 0.4)",
        "logo-glow": "0 10px 15px -3px rgba(0, 208, 156, 0.3)",
      },
      maxWidth: {
        content: "1200px",
      },
      backgroundImage: {
        "groww-gradient": "linear-gradient(to right, #00D09C, #2fe0aa)",
        "page-mesh":
          "radial-gradient(at 0% 0%, rgba(0, 208, 156, 0.05) 0px, transparent 50%), radial-gradient(at 100% 0%, rgba(83, 103, 255, 0.05) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(0, 208, 156, 0.05) 0px, transparent 50%), radial-gradient(at 0% 100%, rgba(83, 103, 255, 0.05) 0px, transparent 50%)",
      },
    },
  },
  plugins: [],
};
