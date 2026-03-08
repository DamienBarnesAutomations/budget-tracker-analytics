<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
    <div class="bg-[#1e1e1e] p-4 rounded-lg shadow">
      <h3 class="text-lg mb-2 text-gray-400">📈 Total Spending Over Time</h3>
      <v-chart class="chart" :option="cumulativeOption" autoresize />
    </div>
    <div class="bg-[#1e1e1e] p-4 rounded-lg shadow">
      <h3 class="text-lg mb-2 text-gray-400">📈 Cumulative Spend Comparison</h3>
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
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: props.data.cumulative.map(i => i.Date), show: false },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: '#333' } } },
    series: [{
      name: 'Cumulative Spend',
      type: 'line',
      showSymbol: false,
      areaStyle: { opacity: 0.3, color: '#00CC96' },
      data: props.data.cumulative.map(i => i.Cumulative_Total),
      itemStyle: { color: '#00CC96' },
      lineStyle: { width: 3 },
      markLine: {
        symbol: 'none',
        label: { position: 'end', formatter: 'Budget' },
        data: [{ yAxis: 20000, lineStyle: { color: '#FF4B4B', type: 'dashed' } }]
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
    tooltip: { trigger: 'axis' },
    legend: { bottom: 0, textStyle: { color: '#ccc' } },
    grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
    xAxis: { type: 'value', name: 'Days', splitLine: { show: false } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: '#333' } } },
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