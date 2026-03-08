<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
    <div class="bg-[#1e1e1e] p-4 rounded-lg shadow">
      <h3 class="text-lg mb-2 text-gray-400">🌏 By Country (Total)</h3>
      <v-chart class="chart" :option="totalOption" autoresize />
    </div>
    <div class="bg-[#1e1e1e] p-4 rounded-lg shadow">
      <h3 class="text-lg mb-2 text-gray-400">🌏 By Country (Daily)</h3>
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
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'value', name: '€', splitLine: { show: false } },
    yAxis: { type: 'category', data: sorted.map(i => i.Country) },
    series: [{
      type: 'bar',
      data: sorted.map(i => i.Amount),
      label: { show: true, position: 'insideRight', formatter: '€{c}' },
      itemStyle: { color: '#42b983' }
    }],
    backgroundColor: 'transparent'
  };
});

const dailyOption = computed(() => {
  if (!props.data || !props.data.daily) return {};
  const sorted = [...props.data.daily].sort((a, b) => a.Avg_Daily_Budget - b.Avg_Daily_Budget);

  return {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'value', name: '€', splitLine: { show: false } },
    yAxis: { type: 'category', data: sorted.map(i => i.Country) },
    series: [{
      type: 'bar',
      data: sorted.map(i => i.Avg_Daily_Budget),
      label: { show: true, position: 'insideRight', formatter: '€{c}' },
      itemStyle: { color: '#35495e' }
    }],
    backgroundColor: 'transparent'
  };
});

</script>

<style scoped>
.chart {
  height: 300px;
}
</style>
