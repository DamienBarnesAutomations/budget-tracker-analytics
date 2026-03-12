<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 h-full">
    <div v-if="summary" class="glass-card flex flex-col justify-center">
      <h3 class="text-muted mb-1 font-medium text-xs md:text-sm tracking-wider uppercase">Total Spent</h3>
      <div class="text-2xl md:text-3xl font-bold text-white mb-1">€{{ summary.total_spent.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
      <div class="text-xs md:text-sm text-accent-secondary font-medium">€{{ summary.remaining.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }} remaining</div>
    </div>

    <div v-if="summary" class="glass-card flex flex-col justify-center">
      <h3 class="text-muted mb-1 font-medium text-xs md:text-sm tracking-wider uppercase">Flights</h3>
      <div class="text-2xl md:text-3xl font-bold text-white mb-1">€{{ summary.flights_spent.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
      <div class="text-xs md:text-sm text-muted">Total flights</div>
    </div>
    
    <div v-if="summary" class="glass-card flex flex-col justify-center">
      <h3 class="text-muted mb-1 font-medium text-xs md:text-sm tracking-wider uppercase">Daily Avg</h3>
      <div class="text-2xl md:text-3xl font-bold text-white mb-1">€{{ summary.daily_avg.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
      <div class="text-xs md:text-sm text-muted">{{ summary.days }} ground days</div>
    </div>

    <div class="col-span-1 md:col-span-3 glass-card" v-if="summary">
      <div class="flex justify-between mb-2 md:mb-3">
        <span class="text-sm md:font-semibold text-white">Budget Exhaustion</span>
        <span class="text-sm md:font-bold text-accent-primary">{{ (summary.percent_used * 100).toFixed(1) }}%</span>
      </div>
      <ProgressBar :value="summary.percent_used * 100" :show-value="false" class="h-2 md:h-3 rounded-full"></ProgressBar>
      <div class="mt-4 md:mt-5 text-xs md:text-sm text-white flex items-start md:items-center gap-2 md:gap-3 bg-[rgba(15,23,42,0.5)] p-3 md:p-4 rounded-xl border border-[rgba(255,255,255,0.05)]">
        <span class="text-lg md:text-xl">💡</span> 
        <span class="leading-relaxed">At <strong class="text-accent-primary">€{{ summary.daily_avg.toFixed(2) }}/day (ground)</strong>, your budget lasts for <strong class="text-white">{{ summary.days_remaining }} more days</strong>.</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import Card from 'primevue/card';
import ProgressBar from 'primevue/progressbar';

defineProps({
  summary: Object
})
</script>
