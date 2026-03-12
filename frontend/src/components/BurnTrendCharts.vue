<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 h-full">
    <div class="glass-card">
      <h3 class="text-lg font-semibold text-white mb-4">📈 Total Spending Over Time</h3>
      <v-chart class="chart" :option="cumulativeOption" autoresize />
    </div>
    <div class="glass-card">
      <h3 class="text-lg font-semibold text-white mb-4">📈 Cumulative Spend Comparison</h3>
      <v-chart class="chart" :option="comparisonOption" autoresize />
    </div>
  </div>
</template>

<script setup>
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  MarkLineComponent
} from 'echarts/components';
import VChart from 'vue-echarts';
import { computed } from 'vue';

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  MarkLineComponent
]);

const props = defineProps({
  data: Object
})

const cumulativeOption = computed(() => {
  if (!props.data || !props.data.cumulative) return {};

  return {
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' }, backgroundColor: 'rgba(15, 23, 42, 0.9)', borderColor: 'rgba(255,255,255,0.1)', textStyle: { color: '#fff' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: props.data.cumulative.map(i => i.Date), show: false },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }, axisLabel: { color: '#94a3b8' } },
    series: [{
      name: 'Cumulative Spend',
      type: 'line',
      areaStyle: {
        opacity: 0.3,
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [{ offset: 0, color: '#3b82f6' }, { offset: 1, color: 'rgba(59, 130, 246, 0)' }]
        }
      },
      data: props.data.cumulative.map(i => i.Cumulative_Total),
      itemStyle: { color: '#3b82f6' },
      lineStyle: { width: 3, color: '#3b82f6' },
      markLine: {
        symbol: 'none',
        label: { position: 'end', formatter: 'Budget', color: '#f87171' },
        data: [{ yAxis: 20000, lineStyle: { color: '#ef4444', type: 'dashed' } }]
      }
    }],
    backgroundColor: 'transparent'
  };
});

const comparisonOption = computed(() => {
  if (!props.data || !props.data.comparison) return {};

  const countries = [...new Set(props.data.comparison.map(i => i.Country))];
  const series = countries.map(country => {
    const countryData = props.data.comparison.filter(i => i.Country === country);
    return {
      name: country,
      type: 'line',
      showSymbol: false,
      data: countryData.map(i => [i.Day_Num, i.Cumulative_Total]),
      smooth: true,
      lineStyle: { width: 3 }
    };
  });

  return {
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(15, 23, 42, 0.9)', borderColor: 'rgba(255,255,255,0.1)', textStyle: { color: '#fff' } },
    legend: { bottom: 0, textStyle: { color: '#94a3b8' }, itemGap: 20 },
    grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
    xAxis: { type: 'value', name: 'Days', nameTextStyle: {color: '#94a3b8'}, splitLine: { show: false }, axisLabel: { color: '#94a3b8' } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }, axisLabel: { color: '#94a3b8' } },
    series: series,
    backgroundColor: 'transparent'
  };
});

</script>

<style scoped>
.chart {
  height: 300px;
}
</style>