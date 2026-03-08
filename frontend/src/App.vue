<script setup>
import DashboardShell from './components/DashboardShell.vue'
</script>

<template>
  <DashboardShell />
</template>

<style>
body {
  margin: 0;
  padding: 0;
  background-color: #121212;
}

/* Base grid and spacing (Tailwind-like utility classes used in components) */
.grid { display: grid; }
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.gap-4 { gap: 1rem; }
.mb-6 { margin-bottom: 1.5rem; }
.p-4 { padding: 1rem; }
.rounded-lg { border-radius: 0.5rem; }
.shadow { box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06); }
.text-3xl { font-size: 1.875rem; line-height: 2.25rem; }
.font-bold { font-weight: 700; }
.text-sm { font-size: 0.875rem; line-height: 1.25rem; }
.text-gray-500 { color: #6b7280; }
.text-gray-400 { color: #9ca3af; }
.text-gray-300 { color: #d1d5db; }
.flex { display: flex; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.mb-1 { margin-bottom: 0.25rem; }
.mt-4 { margin-top: 1rem; }
.mt-2 { margin-top: 0.5rem; }
.font-medium { font-weight: 500; }
.text-blue-400 { color: #60a5fa; }
.max-w-6xl { max-width: 72rem; }
.mx-auto { margin-left: auto; margin-right: auto; }
.mb-8 { margin-bottom: 2rem; }
.text-4xl { font-size: 2.25rem; line-height: 2.5rem; }
.justify-center { justify-content: center; }
.gap-2 { gap: 0.5rem; }

@media (min-width: 768px) {
  .md\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .md\:p-8 { padding: 2rem; }
  .md\:text-left { text-align: left; }
  .md\:justify-start { justify-content: flex-start; }
  .col-span-1 { grid-column: span 1 / span 1; }
  .md\:col-span-2 { grid-column: span 2 / span 2; }
}
</style>
