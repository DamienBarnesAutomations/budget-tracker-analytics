<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 h-full">
    <div class="glass-card">
      <h3 class="text-lg font-semibold text-white mb-2 md:mb-4">🌏 By Country (Total)</h3>
      <v-chart class="chart" :option="totalOption" autoresize />
    </div>
    <div class="glass-card">
      <h3 class="text-lg font-semibold text-white mb-2 md:mb-4">🌏 By Country (Daily)</h3>
      <v-chart class="chart" :option="dailyOption" autoresize />
    </div>
  </div>
</template>

<script setup>
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
} from 'echarts/components';
import VChart from 'vue-echarts';
import { computed } from 'vue';

use([
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
]);

const props = defineProps({
  data: Object
})

const totalOption = computed(() => {
  if (!props.data || !props.data.total) return {};
  const sorted = [...props.data.total].sort((a, b) => a.Amount - b.Amount);

  return {
    tooltip: { 
      trigger: 'axis', 
      axisPointer: { type: 'shadow' }, 
      backgroundColor: 'rgba(15, 23, 42, 0.9)', 
      borderColor: 'rgba(255,255,255,0.1)', 
      textStyle: { color: '#fff' },
      formatter: (params) => {
        const p = params[0];
        return `${p.name}: <b>€${p.value.toLocaleString()}</b>`;
      }
    },
    grid: { left: '3%', right: '8%', bottom: '3%', containLabel: true },
    xAxis: { 
      type: 'log', 
      name: '€', 
      nameTextStyle: {color: '#94a3b8'}, 
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }, 
      axisLabel: { 
        color: '#94a3b8',
        formatter: (value) => {
          if (value >= 1000) return '€' + (value / 1000) + 'k';
          return '€' + value;
        }
      } 
    },
    yAxis: { type: 'category', data: sorted.map(i => i.Country), axisLabel: { color: '#94a3b8' } },
    series: [{
      type: 'bar',
      data: sorted.map(i => i.Amount),
      label: { 
        show: true, 
        position: 'insideRight', 
        formatter: (params) => '€' + params.value.toLocaleString(), 
        color: '#fff', 
        fontWeight: 'bold',
        fontSize: 10
      },
      itemStyle: { color: '#10b981', borderRadius: 4 }
    }],
    backgroundColor: 'transparent'
  };
});

const dailyOption = computed(() => {
  if (!props.data || !props.data.daily) return {};
  const sorted = [...props.data.daily].sort((a, b) => a.Avg_Daily_Budget - b.Avg_Daily_Budget);

  return {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, backgroundColor: 'rgba(15, 23, 42, 0.9)', borderColor: 'rgba(255,255,255,0.1)', textStyle: { color: '#fff' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'value', name: '€', nameTextStyle: {color: '#94a3b8'}, splitLine: { show: false }, axisLabel: { color: '#94a3b8' } },
    yAxis: { type: 'category', data: sorted.map(i => i.Country), axisLabel: { color: '#94a3b8' } },
    series: [{
      type: 'bar',
      data: sorted.map(i => i.Avg_Daily_Budget),
      label: { show: true, position: 'insideRight', formatter: '€{c}', color: '#fff', fontWeight: 'bold' },
      itemStyle: { color: '#3b82f6', borderRadius: 4 }
    }],
    backgroundColor: 'transparent'
  };
});

</script>

<style scoped>
.chart {
  height: 250px;
}
@media (min-width: 768px) {
  .chart {
    height: 300px;
  }
}
</style>
