<template>
  <div class="h-full">
    <Panel header="📝 Recent Transactions" toggleable :collapsed="false" class="transaction-panel">
      <DataTable :value="transactions" size="small" stripedRows scrollable
        class="p-datatable-sm custom-table text-xs md:text-sm">
        <Column field="Date" header="Date"></Column>
        <Column field="Category" header="Category"></Column>
        <Column field="Country" header="Country" class="hidden md:table-cell"></Column>
        <Column field="Amount" header="Amount">
          <template #body="slotProps">
            <span class="font-medium text-white">€{{ slotProps.data.Amount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</span>
          </template>
        </Column>
      </DataTable>
    </Panel>
  </div>
</template>

<style>
/* Override PrimeVue Panel styles to fix glassmorphism background */
.transaction-panel.p-panel {
  background: transparent;
  border: none;
}
.transaction-panel .p-panel-header {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(255,255,255,0.05);
  border-bottom: none;
  border-top-left-radius: 0.5rem;
  border-top-right-radius: 0.5rem;
}
.transaction-panel .p-panel-content {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.05);
  border-bottom-left-radius: 0.5rem;
  border-bottom-right-radius: 0.5rem;
  padding: 0;
}
/* Custom table styling to fit glass theme */
.custom-table .p-datatable-header,
.custom-table .p-datatable-thead > tr > th {
  background: rgba(15, 23, 42, 0.8);
  color: #94a3b8;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  font-weight: 600;
}
.custom-table .p-datatable-tbody > tr {
  background: transparent;
  color: #e2e8f0;
}
.custom-table .p-datatable-tbody > tr.p-datatable-row-striped {
  background: rgba(255, 255, 255, 0.02);
}
.custom-table .p-datatable-tbody > tr > td {
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
</style>

<script setup>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Panel from 'primevue/panel';

defineProps({
  transactions: Array
})
</script>
