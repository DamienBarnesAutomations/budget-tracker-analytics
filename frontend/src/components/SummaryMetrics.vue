<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 h-full">
    <div v-if="summary" class="glass-card flex flex-col justify-center">
      <h3 class="text-muted mb-2 font-medium text-sm tracking-wider">TOTAL SPENT</h3>
      <div class="text-4xl font-bold text-white mb-1">€{{ summary.total_spent.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
      <div class="text-sm text-accent-secondary font-medium">€{{ summary.remaining.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }} remaining</div>
    </div>
    
    <div v-if="summary" class="glass-card flex flex-col justify-center">
      <h3 class="text-muted mb-2 font-medium text-sm tracking-wider">DAILY AVERAGE</h3>
      <div class="text-4xl font-bold text-white mb-1">€{{ summary.daily_avg.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
      <div class="text-sm text-muted">{{ summary.days }} days tracked</div>
    </div>

    <div class="col-span-1 md:col-span-2 glass-card" v-if="summary">
      <div class="flex justify-between mb-3">
        <span class="font-semibold text-white">Budget Exhaustion</span>
        <span class="font-bold text-accent-primary">{{ (summary.percent_used * 100).toFixed(1) }}%</span>
      </div>
      <ProgressBar :value="summary.percent_used * 100" :show-value="false" class="h-3 rounded-full"></ProgressBar>
      <div class="mt-5 text-sm text-white flex items-center gap-3 bg-[rgba(15,23,42,0.5)] p-4 rounded-xl border border-[rgba(255,255,255,0.05)]">
        <span class="text-xl">💡</span> 
        <span class="leading-relaxed">At <strong class="text-accent-primary">€{{ summary.daily_avg.toFixed(2) }}/day</strong>, your budget lasts for <strong class="text-white">{{ summary.days_remaining }} more days</strong>.</span>
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
