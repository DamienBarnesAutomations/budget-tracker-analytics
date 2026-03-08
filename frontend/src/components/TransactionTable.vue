<template>
  <div class="mb-6">
    <Panel header="📝 Recent Transactions" toggleable collapsed>
      <DataTable :value="transactions" size="small" stripedRows tableStyle="min-width: 50rem">
        <Column field="Date" header="Date"></Column>
        <Column field="Category" header="Category"></Column>
        <Column field="Country" header="Country"></Column>
        <Column field="Amount" header="Amount">
          <template #body="slotProps">
            €{{ slotProps.data.Amount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
          </template>
        </Column>
      </DataTable>
    </Panel>
  </div>
</template>

<script setup>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Panel from 'primevue/panel';

defineProps({
  transactions: Array
})
</script>
