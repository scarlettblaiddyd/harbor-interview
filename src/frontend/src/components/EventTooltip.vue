<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router'
import { defineProps, computed, onMounted } from 'vue'
import { useEventStore } from '@/stores/eventStore';

const router = useRouter()
const eventStore = useEventStore()
const removed = ref<boolean>(false)

const props = defineProps<{
  visible: boolean,
  x: number,
  y: number,
  mouseenter: Function,
  mouseleave: Function
}>()

// Prevent tooltip from spawning too close to right side of screen and getting squished
const tooltipStyle = computed(() => {
  const approxWidth = 300
  let left = props.x + 10
  if(props.x + 300 > window.innerWidth) left = props.x - approxWidth

  return `top: ${props.y + 10}px; left: ${left}px;`
})


function removeEvent() {
  const toRemove = eventStore.events.findIndex(e => e.context === eventStore.highlightedEvent?.context)
  if(toRemove !== -1) { 
    eventStore.events.splice(toRemove, 1)
    removed.value = true
    setTimeout(() => {
      removed.value = false
      props.mouseleave()
    }, 1000);
  }
}
</script>

<template>
  <Teleport to="body">
    <div v-if="visible"
      class="bg-gray-800 absolute z-100 max-w-sm rounded-md border flex flex-col p-4"
      :style=tooltipStyle
      @mouseenter="mouseenter()"
      @mouseleave="mouseleave()"
      >
        <div v-if="!removed">
          <span class="text-lg font-bold">{{ eventStore.highlightedEvent?.title }}</span><br/>
          <span class="text-sm">
            {{ eventStore.highlightedEvent?.context }} <br/>
            from: {{ eventStore.highlightedEvent?.document }}
          </span>
          <div class="flex flex-col items-center gap-4">
              <button class="bg-blue-500 text-white rounded-md p-2 mt-2 w-fit hover:bg-blue-700"
                @click="() => {
                  router.push(`/document/${eventStore.highlightedEvent?.document}`)
                }">
                View Event Source in Document
              </button>
            
              <button class="bg-red-500 text-white rounded-md p-2 mt-2 w-fit hover:bg-red-700"
                @click="removeEvent">
                Remove Event
              </button>
          </div>
        </div>
        <div v-else>
          Event successfully removed from calendar
        </div>
    </div>
  </Teleport>
</template>
