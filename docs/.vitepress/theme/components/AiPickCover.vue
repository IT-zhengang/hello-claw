<script setup lang="ts">
defineProps<{
  eyebrow: string
  title: string
  description: string
  chips?: string[]
}>()
</script>

<template>
  <div class="pick-cover">
    <div class="pick-cover__eyebrow">{{ eyebrow }}</div>
    <div class="pick-cover__title">{{ title }}</div>
    <p class="pick-cover__desc">{{ description }}</p>
    <div v-if="chips?.length" class="pick-cover__chips">
      <span v-for="chip in chips" :key="chip">{{ chip }}</span>
    </div>
  </div>
</template>
