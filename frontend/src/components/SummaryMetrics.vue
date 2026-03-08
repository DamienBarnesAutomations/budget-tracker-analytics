<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
    <Card v-if="summary">
      <template #title>Total Spent</template>
      <template #content>
        <div class="text-3xl font-bold">€{{ summary.total_spent.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
        <div class="text-sm text-gray-500">€{{ summary.remaining.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }} remaining</div>
      </template>
    </Card>
    
    <Card v-if="summary">
      <template #title>Daily Average</template>
      <template #content>
        <div class="text-3xl font-bold">€{{ summary.daily_avg.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
        <div class="text-sm text-gray-500">{{ summary.days }} days tracked</div>
      </template>
    </Card>

    <div class="col-span-1 md:col-span-2 mt-4" v-if="summary">
      <div class="flex justify-between mb-1">
        <span class="text-sm font-medium">Budget Exhaustion</span>
        <span class="text-sm font-medium">{{ (summary.percent_used * 100).toFixed(1) }}%</span>
      </div>
      <ProgressBar :value="summary.percent_used * 100" :show-value="false"></ProgressBar>
      <div class="mt-2 text-sm text-blue-400">
        💡 At €{{ summary.daily_avg.toFixed(2) }}/day, your budget lasts for <b>{{ summary.days_remaining }} more days</b>.
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
