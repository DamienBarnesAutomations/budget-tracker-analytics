<template>
  <div class="mb-6">
    <h3 class="text-xl mb-2 text-gray-300">Daily Budget Allocation</h3>
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<script setup>
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { PieChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
} from 'echarts/components';
import VChart from 'vue-echarts';
import { ref, computed, watch } from 'vue';

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
]);

const props = defineProps({
  data: Array
})

const option = computed(() => {
  if (!props.data || props.data.length === 0) return {};

  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: €{c} ({d}%)'
    },
    series: [
      {
        name: 'Daily Budget Allocation',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#1e1e1e',
          borderWidth: 2
        },
        label: {
          show: true,
          position: 'outside',
          formatter: '{b} {d}%',
          color: '#ccc'
        },
        labelLine: {
          show: true
        },
        data: props.data.map(item => ({
          name: item.Category,
          value: item.Daily_Avg_Euro
        }))
      }
    ],
    backgroundColor: 'transparent'
  };
});

</script>

<style scoped>
.chart {
  height: 400px;
}
</style>
