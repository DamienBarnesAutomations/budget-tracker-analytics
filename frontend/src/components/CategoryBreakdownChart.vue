<template>
  <div class="mb-6 bg-[#1e1e1e] p-4 rounded-lg shadow">
    <h3 class="text-xl mb-4 text-gray-300">How much am I spending per day in each country?</h3>
    <v-chart class="chart" :option="option" autoresize />
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

  const series = countries.map(country => {
    return {
      name: country,
      type: 'bar',
      label: {
        show: true,
        position: 'right',
        formatter: '€{c}',
        color: '#aaa',
        fontSize: 11,
        fontFamily: 'Inter, sans-serif',
      },
      data: categories.map(cat => {
        const item = props.data.find(i => i.Country === country && i.Category === cat);
        return item ? item.Daily_Avg : 0;
      })
    };
  });

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: '#2a2a2a',
      borderColor: '#444',
      borderWidth: 1,
      textStyle: { color: '#eee', fontFamily: 'Inter, sans-serif', fontSize: 13 },
      formatter: params => {
        const header = `<div style="margin-bottom:6px;font-weight:600;color:#fff">${params[0].axisValue}</div>`;
        const rows = params.map(p =>
          `<div style="display:flex;justify-content:space-between;gap:16px">
            <span>${p.marker}${p.seriesName}</span>
            <span style="font-weight:600">€${p.value}</span>
          </div>`
        ).join('');
        return header + rows;
      }
    },
    legend: {
      bottom: 0,
      textStyle: { color: '#aaa', fontFamily: 'Inter, sans-serif', fontSize: 12 },
      itemGap: 20,
    },
    grid: { left: '3%', right: '12%', bottom: '15%', containLabel: true },
    xAxis: {
      type: 'value',
      name: 'Avg Daily Spend (€)',
      nameTextStyle: { color: '#666', fontSize: 11, fontFamily: 'Inter, sans-serif' },
      splitLine: { show: false },
      axisLabel: { color: '#666', fontFamily: 'Inter, sans-serif', fontSize: 11 },
      axisLine: { show: false },
      axisTick: { show: false },
    },
    yAxis: {
      type: 'category',
      data: categories,
      axisLabel: { color: '#bbb', fontFamily: 'Inter, sans-serif', fontSize: 12 },
      axisLine: { lineStyle: { color: '#333' } },
      axisTick: { show: false },
    },
    series: series,
    backgroundColor: 'transparent'
  };
});

</script>

<style scoped>
.chart {
  height: 500px;
}
</style>