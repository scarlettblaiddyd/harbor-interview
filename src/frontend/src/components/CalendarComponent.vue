<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import FullCalender from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { useEventStore } from '@/stores/eventStore'
import EventTooltip from './EventTooltip.vue'
import { type components } from '../models'

type ExtractedEvent = components["schemas"]["ExtractedEvent"]

const eventStore = useEventStore()

const tooltipVisible = ref<boolean>(false)
const isHoveringTooltip = ref<boolean>(false)
const tooltipTimeout = ref<number | null>()
const tooltipX = ref<number>(0)
const tooltipY = ref<number>(0)

const closestEvent = ref<ExtractedEvent | null>()
const calendarRef = ref<any>()
const remountCalendarKey = ref<number>(0)

const calendarOptions = computed(() => (
  {
    plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
    initialView: 'dayGridMonth',
    views: {
      dayGridMonth: { buttonText: 'Month' },
      timeGridWeek: { buttonText: 'Week' },
      timeGridDay: { buttonText: 'Day' }
    },
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    weekends: true,
    // Map events from backend to calendar widget events
    events: eventStore.events.map(e => {
      return {
        start: new Date(e.date).toISOString(),
        allDay: true,
        title: e.title,
        extendedProps: { original: e }, // Store event data in extended props for ease of access
        classNames: closestEvent.value?.title === e.title ? ['highlighted-event'] : []
      }
    }),
    dayCellDidMount(info: any) {
      const targetDate = closestEvent.value?.date
      console.log(targetDate)
      if (!targetDate) return

      const eventDateStr = new Date(targetDate).toDateString()
      const cellDateStr = info.date.toDateString()

      if (eventDateStr === cellDateStr) {
        // Add text to the cell
        const label = document.createElement('div')
        label.innerHTML = 'Nearest deadline!'
        label.classList.add('bg-rose-400', 'text-md', 'text-white', '!mt-[-1.5em]', 'z-100', 'rounded-md')
        info.el.appendChild(label)

        info.el.classList.add('bg-blue-400', 'text-white')
      }
    },
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

watch(() => eventStore.events, (newVal: ExtractedEvent[], _oldValue: any[]) => {
  console.log('here')
  console.log(newVal)
  const now = new Date()
  console.log(now)

  const futureEvents = newVal.filter(e => new Date(e.date).getTime() > now.getTime())

  if(!futureEvents.length) {
    alert('All dates extracted are in the past, hope you didn\'t miss anything important!')
  }

  futureEvents.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
  closestEvent.value = futureEvents[0]
  if(!calendarRef.value) return
  const calendarApi = calendarRef.value.getApi()
  calendarApi.gotoDate(new Date(closestEvent.value.date).toISOString())
  // render extra cell styling for near deadlines
  remountCalendarKey.value++
}, {deep: true})
</script>


<template>
  <FullCalender ref="calendarRef" :key="remountCalendarKey" :options='calendarOptions' class="min-w-md w-full max-w-6xl"/>
  <EventTooltip
    :visible="tooltipVisible || isHoveringTooltip"
    :x="tooltipX"
    :y="tooltipY"
    :mouseenter="() => isHoveringTooltip = true"
    :mouseleave="() => isHoveringTooltip = false"
  />

</template>


<style lang="postcss">
.highlighted-event {
  background-color: rgb(131, 121, 29);
  border-radius: 6px;
  font-weight: bold;
  border: 1px solid orange;
}
</style>