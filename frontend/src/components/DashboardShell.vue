<template>
  <div class="min-h-screen text-white p-4 md:p-8 my-app-dark">
    <div class="w-full mx-auto">
      <header class="mb-8 text-center md:text-left">
        <h1 class="text-4xl font-bold flex items-center justify-center md:justify-start gap-2">
          <span>🌍</span> <span class="text-gradient">Travel Expenses</span>
        </h1>
        <p class="text-muted mt-2">Your interactive budget dashboard</p>
      </header>

      <div v-if="loading" class="flex flex-col items-center justify-center h-64 glass-card">
        <ProgressSpinner />
        <p class="mt-4 text-muted">Loading data from Google Sheets...</p>
      </div>

      <div v-else-if="error" class="p-4 bg-red-900/30 border border-red-500 rounded-lg text-red-200 glass-card">
        {{ error }}
      </div>

      <div v-else class="bento-grid">
        <!-- Row 1: Summary Metrics (Total Spent, Exhaustion, Flights) -->
        <div class="col-span-1 md:col-span-2 lg:col-span-3">
          <SummaryMetrics :summary="summary" />
        </div>

        <!-- Row 2: Daily Average Card and Allocation Pie Chart -->
        <div class="col-span-1 glass-card flex flex-col py-4 md:py-6" v-if="summary">
          <h3 class="text-muted mb-1 font-medium text-xs md:text-sm tracking-wider uppercase">Daily Avg</h3>
          <div class="text-2xl md:text-4xl font-bold text-white mb-1">€{{ summary.daily_avg.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
          <div class="text-xs md:text-base text-muted">{{ summary.days }} ground days</div>
        </div>
        <div class="col-span-1 md:col-span-1 lg:col-span-2 glass-card flex flex-col">
          <AllocationPieChart :data="allocation" />
        </div>

        <!-- Row 3: Spending Trend Charts (Full Width) -->
        <div class="col-span-1 md:col-span-2 lg:col-span-3 flex flex-col">
          <BurnTrendCharts :data="trends" />
        </div>
        
        <!-- Row 4: Country charts -->
        <div class="col-span-1 md:col-span-2 lg:col-span-3 flex flex-col">
          <CountryBarCharts :data="countryCharts" />
        </div>

        <!-- Full width breakdown chart -->
        <div class="col-span-1 md:col-span-2 lg:col-span-3 glass-card">
          <CategoryBreakdownChart :data="categories" />
        </div>

        <!-- Transactions Full Width -->
        <div class="col-span-1 md:col-span-2 lg:col-span-3 glass-card">
          <TransactionTable :transactions="transactions" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ProgressSpinner from 'primevue/progressspinner';
import SummaryMetrics from './SummaryMetrics.vue';
import AllocationPieChart from './AllocationPieChart.vue';
import CountryBarCharts from './CountryBarCharts.vue';
import BurnTrendCharts from './BurnTrendCharts.vue';
import CategoryBreakdownChart from './CategoryBreakdownChart.vue';
import TransactionTable from './TransactionTable.vue';
import { 
  getSummary, 
  getAllocation, 
  getCountryCharts, 
  getTrends, 
  getCategories, 
  getTransactions 
} from '../api';

const loading = ref(true);
const error = ref(null);
const summary = ref(null);
const allocation = ref([]);
const countryCharts = ref(null);
const trends = ref(null);
const categories = ref([]);
const transactions = ref([]);

const fetchData = async () => {
  try {
    loading.value = true;
    const [
      resSummary, 
      resAllocation, 
      resCountry, 
      resTrends, 
      resCategories, 
      resTransactions
    ] = await Promise.all([
      getSummary(),
      getAllocation(),
      getCountryCharts(),
      getTrends(),
      getCategories(),
      getTransactions()
    ]);

    summary.value = resSummary.data;
    allocation.value = resAllocation.data;
    countryCharts.value = resCountry.data;
    trends.value = resTrends.data;
    categories.value = resCategories.data;
    transactions.value = resTransactions.data;
    
    if (summary.value.error) {
      error.value = "No data found in Google Sheets. Please upload a CSV via the Telegram bot.";
    }
  } catch (err) {
    console.error('Failed to fetch dashboard data:', err);
    error.value = "Failed to load dashboard data. Please check the backend connection.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchData();
});
</script>
