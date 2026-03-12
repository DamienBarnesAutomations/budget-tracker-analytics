  <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 md:gap-6 h-full">
    <!-- Combined Hero Card: Total Spent & Budget Exhaustion -->
    <div v-if="summary" class="lg:col-span-2 glass-card">
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
  </div>
</template>

<script setup>
import Card from 'primevue/card';
import ProgressBar from 'primevue/progressbar';

defineProps({
  summary: Object
})
</script>
