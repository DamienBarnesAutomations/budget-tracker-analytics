<template>
  <div class="h-full flex flex-col">
    <h3 class="text-lg font-semibold text-white mb-4">How much am I spending per day?</h3>
    <v-chart class="chart flex-grow" :option="option" autoresize />
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
  data: Array
})

const option = computed(() => {
  if (!props.data || props.data.length === 0) return {};

  const categories = [...new Set(props.data.map(i => i.Category))];
  const countries = [...new Set(props.data.map(i => i.Country))];
  
  const series = countries.map((country, index) => {
    const colors = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#0ea5e9'];
    return {
      name: country,
      type: 'bar',
      label: { show: true, position: 'right', formatter: '{c}', color: '#fff' },
      itemStyle: { borderRadius: 4, color: colors[index % colors.length] },
      data: categories.map(cat => {
        const item = props.data.find(i => i.Country === country && i.Category === cat);
        return item ? item.Daily_Avg : 0;
      })
    };
  });

  return {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, backgroundColor: 'rgba(15, 23, 42, 0.9)', borderColor: 'rgba(255,255,255,0.1)', textStyle: { color: '#fff' } },
    legend: { bottom: 0, textStyle: { color: '#94a3b8' } },
    grid: { left: '3%', right: '10%', bottom: '15%', containLabel: true },
    xAxis: { type: 'value', name: 'Avg Daily Spend (€)', nameTextStyle: {color: '#94a3b8'}, splitLine: { show: false }, axisLabel: { color: '#94a3b8' } },
    yAxis: { type: 'category', data: categories, axisLabel: { color: '#94a3b8' } },
    series: series,
    backgroundColor: 'transparent'
  };
});

</script>

<style scoped>
.chart {
  min-height: 400px;
  width: 100%;
}
</style>