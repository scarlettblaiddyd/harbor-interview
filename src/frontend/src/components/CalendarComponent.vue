<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import FullCalender from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import { useEventStore } from '@/stores/eventStore'
import EventTooltip from './EventTooltip.vue'

const eventStore = useEventStore()

const tooltipVisible = ref<boolean>(false)
const isHoveringTooltip = ref<boolean>(false)
const tooltipTimeout = ref<number | null>()
const tooltipX = ref<number>(0)
const tooltipY = ref<number>(0)

const calendarOptions = computed(() => (
  {
    plugins: [dayGridPlugin],
    initialView: 'dayGridMonth',
    weekends: true,
    // Map events from backend to calendar widget events
    events: eventStore.events.map(e => {
      return {
        start: new Date(e.date).toISOString(),
        allDay: true,
        title: e.title,
        extendedProps: { original: e } // Store event data in extended props for ease of access
      }
    }),
    eventMouseEnter(info: any) {
      // Remove hide-tooltip timer so it doesn't dissapear while hovering
      if(tooltipTimeout.value) clearTimeout(tooltipTimeout.value)

      tooltipVisible.value = true
      eventStore.highlightedEvent = info.event.extendedProps.original
      // Tooltip uses absolute positioning, set it to appear at the cursor
      const mouseEvent = info.jsEvent as MouseEvent
      if(mouseEvent) {
        tooltipX.value = mouseEvent.x
        tooltipY.value = mouseEvent.y
      }
    },

    // After 300ms, hide the tooltip. Give this time so that users can move their mouse over to the tooltip
    // before it dissapears
    eventMouseLeave() {
      tooltipTimeout.value = setTimeout(() => {
        tooltipVisible.value = false
        eventStore.highlightedEvent = null
      }, 300)
    }
  }
))

// If they hover over the tooltip, prevent it from being hidden and set the event to be highlighted on a "view document" click
watch(isHoveringTooltip, (value: boolean, _oldValue: boolean) => {
  if(value && tooltipTimeout.value) clearTimeout(tooltipTimeout.value)
  if(!value) {
    eventStore.highlightedEvent = null
    tooltipVisible.value = false
  }
})
</script>


<template>
  <FullCalender :options='calendarOptions' class="min-w-md w-full max-w-6xl"/>
  <EventTooltip
    :visible="tooltipVisible || isHoveringTooltip"
    :x="tooltipX"
    :y="tooltipY"
    :mouseenter="() => isHoveringTooltip = true"
    :mouseleave="() => isHoveringTooltip = false"
  />

</template>
