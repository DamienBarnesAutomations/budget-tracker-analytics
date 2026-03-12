<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 h-full">
    <!-- Combined Hero Card: Total Spent & Budget Exhaustion -->
    <div v-if="summary" class="md:col-span-2 glass-card">
      <div class="flex flex-col md:flex-row md:items-end justify-between mb-4 md:mb-6">
        <div>
          <h3 class="text-muted mb-1 font-medium text-xs md:text-sm tracking-wider uppercase">Total Spent</h3>
          <div class="text-3xl md:text-5xl font-bold text-white leading-none">
            €{{ summary.total_spent.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
          </div>
          <div class="text-xs md:text-base text-accent-secondary font-medium mt-1 md:mt-2">
            €{{ summary.remaining.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }} remaining
          </div>
        </div>
        <div class="mt-4 md:mt-0 text-right">
          <div class="text-xs md:text-sm text-muted uppercase tracking-wider mb-1">Budget Used</div>
          <div class="text-2xl md:text-3xl font-bold text-accent-primary">
            {{ (summary.percent_used * 100).toFixed(1) }}%
          </div>
        </div>
      </div>

      <ProgressBar :value="summary.percent_used * 100" :show-value="false" class="h-2 md:h-4 rounded-full bg-slate-800"></ProgressBar>
      
      <div class="mt-4 md:mt-6 text-xs md:text-sm text-white flex items-center gap-3 bg-[rgba(15,23,42,0.4)] p-3 md:p-4 rounded-xl border border-[rgba(255,255,255,0.05)]">
        <span class="text-lg md:text-xl shrink-0">💡</span> 
        <span class="leading-relaxed">At <strong class="text-accent-primary">€{{ summary.daily_avg.toFixed(2) }}/day (ground)</strong>, your budget lasts for <strong class="text-white">{{ summary.days_remaining }} more days</strong>.</span>
      </div>
    </div>

    <!-- Flights Card -->
    <div v-if="summary" class="glass-card flex flex-col justify-center py-4 md:py-6 lg:items-center">
      <h3 class="text-muted mb-1 font-medium text-xs md:text-sm tracking-wider uppercase lg:w-full lg:text-center text-left">Flights</h3>
      <div class="text-2xl md:text-4xl font-bold text-white mb-1">€{{ summary.flights_spent.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
      <div class="text-xs md:text-base text-muted">Total flights</div>
    </div>

    <!-- Insights Row -->
    <div v-if="summary && summary.top_category" class="md:col-span-3 grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
      <div class="glass-card p-3 md:p-4">
        <div class="text-[10px] md:text-xs text-muted uppercase mb-1">Top Category</div>
        <div class="text-sm md:text-lg font-bold text-white truncate">{{ summary.top_category.Category }}</div>
        <div class="text-[10px] md:text-xs text-accent-primary">€{{ summary.top_category.Amount.toLocaleString() }} total</div>
      </div>
      
      <div class="glass-card p-3 md:p-4" v-if="summary.weekend_stats && summary.weekend_stats.length">
        <div class="text-[10px] md:text-xs text-muted uppercase mb-1">Weekend vs Weekday</div>
        <div class="text-sm md:text-lg font-bold text-white">
          {{ ((summary.weekend_stats.find(s => s.Type === 'Weekend')?.Amount || 0) / (summary.weekend_stats.find(s => s.Type === 'Weekday')?.Amount || 1)).toFixed(1) }}x
        </div>
        <div class="text-[10px] md:text-xs text-accent-secondary">multiplier</div>
      </div>

      <div class="glass-card p-3 md:p-4" v-if="summary.most_expensive_country">
        <div class="text-[10px] md:text-xs text-muted uppercase mb-1">Most Expensive</div>
        <div class="text-sm md:text-lg font-bold text-white truncate">{{ summary.most_expensive_country.Country }}</div>
        <div class="text-[10px] md:text-xs text-red-400">€{{ summary.most_expensive_country.Avg_Daily_Budget.toFixed(0) }}/day</div>
      </div>

      <div class="glass-card p-3 md:p-4" v-if="summary.cheapest_country">
        <div class="text-[10px] md:text-xs text-muted uppercase mb-1">Cheapest</div>
        <div class="text-sm md:text-lg font-bold text-white truncate">{{ summary.cheapest_country.Country }}</div>
        <div class="text-[10px] md:text-xs text-accent-secondary">€{{ summary.cheapest_country.Avg_Daily_Budget.toFixed(0) }}/day</div>
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
