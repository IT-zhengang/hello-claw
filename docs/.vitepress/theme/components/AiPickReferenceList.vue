<script setup lang="ts">
type ReferenceItem = {
  title: string
  description: string
  href: string
}

const props = defineProps<{
  items: ReferenceItem[]
}>()

const formatIndex = (index: number) => String(index + 1).padStart(2, '0')
</script>

<template>
  <div class="pick-reference-list">
    <a
      v-for="(item, index) in props.items"
      :key="item.href"
      class="pick-reference-card"
      :href="item.href"
      target="_blank"
      rel="noreferrer"
    >
      <span class="pick-reference-card__index">{{ formatIndex(index) }}</span>
      <span class="pick-reference-card__body">
        <strong>{{ item.title }}</strong>
        <span>{{ item.description }}</span>
      </span>
    </a>
  </div>
</template>
