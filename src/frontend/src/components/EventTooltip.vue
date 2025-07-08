<script setup lang="ts">
import { useRouter } from 'vue-router'
import { defineProps } from 'vue'

const router = useRouter()

const props = defineProps<{
  visible: boolean,
  x: number,
  y: number,
  title: string,
  context: string,
  documentName: string,
  mouseenter: Function,
  mouseleave: Function
}>()


</script>

<template>
  <Teleport to="body">
    <div v-if="visible"
      class="bg-red-800 absolute z-100 max-w-sm rounded-md border flex flex-col"
      :style="`top: ${y + 10}px; left: ${x + 10}px;`"
      @mouseenter="mouseenter()"
      @mouseleave="mouseleave()"
      >
        <span class="text-md">{{ title }}</span>
        <span class="text-sm">
          {{ context }} <br/>
          {{ documentName }}
        </span>
    </div>
  </Teleport>
</template>
