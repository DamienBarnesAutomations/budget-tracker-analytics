<script setup>
import DashboardShell from './components/DashboardShell.vue'
</script>

<template>
  <DashboardShell />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --bg-dark: #0B0F19;
  --card-bg: rgba(30, 41, 59, 0.7);
  --card-border: rgba(255, 255, 255, 0.1);
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --accent-primary: #3b82f6;
  --accent-secondary: #10b981;
}

body {
  margin: 0;
  padding: 0;
  background-color: var(--bg-dark);
  color: var(--text-main);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-image: 
    radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.15) 0px, transparent 50%);
  background-attachment: fixed;
  min-height: 100vh;
}

/* Base grid and spacing */
.grid { display: grid; }
.grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.w-full { width: 100%; }
.bento-grid {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 1rem;
}
.gap-4 { gap: 0.75rem; }
.gap-6 { gap: 1rem; }
.mb-6 { margin-bottom: 1.5rem; }
.p-4 { padding: 1rem; }
.p-6 { padding: 1.5rem; }
.rounded-lg { border-radius: 0.5rem; }
.rounded-xl { border-radius: 1rem; }
.shadow { box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06); }
.text-3xl { font-size: 1.5rem; line-height: 2rem; }
.text-2xl { font-size: 1.25rem; line-height: 1.75rem; }
.font-bold { font-weight: 700; }
.font-semibold { font-weight: 600; }
.text-sm { font-size: 0.75rem; line-height: 1rem; }
.text-gray-500 { color: #6b7280; }
.text-gray-400 { color: #9ca3af; }
.text-gray-300 { color: #d1d5db; }
.text-muted { color: var(--text-muted); }
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-8 { margin-bottom: 2rem; }
.mt-4 { margin-top: 1rem; }
.mt-2 { margin-top: 0.5rem; }
.font-medium { font-weight: 500; }
.text-blue-400 { color: #60a5fa; }

.mx-auto { margin-left: auto; margin-right: auto; }
.text-4xl { font-size: 1.875rem; line-height: 2.25rem; }
.justify-center { justify-content: center; }
.gap-2 { gap: 0.5rem; }

/* Glassmorphism Card (Mobile optimized padding) */
.glass-card {
  background: var(--card-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--card-border);
  border-radius: 1rem;
  padding: 1.25rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.glass-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
}

.glass-card h3 {
  margin-top: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Gradient Text for Header */
.text-gradient {
  background: linear-gradient(135deg, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@media (min-width: 768px) {
  .bento-grid { gap: 1.5rem; }
  .text-3xl { font-size: 1.875rem; line-height: 2.25rem; }
  .text-2xl { font-size: 1.5rem; line-height: 2rem; }
  .text-4xl { font-size: 2.25rem; line-height: 2.5rem; }
  .text-sm { font-size: 0.875rem; line-height: 1.25rem; }
  .glass-card { padding: 1.5rem; }
  .glass-card h3 { font-size: 1.125rem; margin-bottom: 1rem; }
  .bento-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .md\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .md\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .md\:p-8 { padding: 2rem; }
  .md\:text-left { text-align: left; }
  .md\:justify-start { justify-content: flex-start; }
  .col-span-1 { grid-column: span 1 / span 1; }
  .md\:col-span-2 { grid-column: span 2 / span 2; }
  .md\:col-span-3 { grid-column: span 3 / span 3; }
  .md\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
}

@media (min-width: 1024px) {
  .bento-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .lg\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .lg\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  .lg\:col-span-2 { grid-column: span 2 / span 2; }
  .lg\:col-span-3 { grid-column: span 3 / span 3; }
  .lg\:row-span-2 { grid-row: span 2 / span 2; }
}
</style>
