<template>
  <div class="h-full flex flex-col">
    <h3 class="text-lg font-semibold text-white mb-4">Daily Budget Allocation</h3>
    <v-chart class="chart flex-grow" :option="option" autoresize />
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
      formatter: '{b}: €{c} ({d}%)',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: 'rgba(255,255,255,0.1)',
      textStyle: { color: '#fff' }
    },
    series: [
      {
        name: 'Daily Budget Allocation',
        type: 'pie',
        radius: ['50%', '80%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: 'rgba(30, 41, 59, 1)',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold',
            color: '#fff'
          }
        },
        labelLine: {
          show: false
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
  min-height: 220px;
  width: 100%;
}
@media (min-width: 768px) {
  .chart {
    min-height: 250px;
  }
}
</style>
