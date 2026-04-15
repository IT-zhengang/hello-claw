<script setup lang="ts">
type SummaryItem = {
  label: string
  value: string
}

defineProps<{
  items: SummaryItem[]
}>()
</script>

<template>
  <div class="pick-summary-grid">
    <div v-for="item in items" :key="item.label" class="pick-summary-card">
      <div class="pick-summary-card__label">{{ item.label }}</div>
      <div class="pick-summary-card__value">{{ item.value }}</div>
    </div>
  </div>
</template>
