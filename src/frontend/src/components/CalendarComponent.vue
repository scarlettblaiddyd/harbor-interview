<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import FullCalender from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import { useEventStore } from '@/stores/eventStore'
import EventTooltip from './EventTooltip.vue'

const eventStore = useEventStore()

const tooltipTitle = ref<string>("")
const tooltipDocName = ref<string>("")
const tooltipContext = ref<string>("")
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
    events: eventStore.events.map(e => {
      return {
        start: new Date(e.date).toISOString(),
        allDay: true,
        title: e.title,
        extendedProps: { context: e.context, document: e.document }
      }
    }),
    eventMouseEnter(info: any) {
      if(tooltipTimeout.value) clearTimeout(tooltipTimeout.value)
      console.log(info.event.title)
      console.log(info.event.extendedProps.document)

      tooltipTitle.value = info.event.title
      tooltipContext.value = info.event.extendedProps.context
      tooltipDocName.value = info.event.extendedProps.document
      tooltipVisible.value = true
      const mouseEvent = info.jsEvent as MouseEvent
      if(mouseEvent) {
        tooltipX.value = mouseEvent.x
        tooltipY.value = mouseEvent.y
      }
    },
    eventMouseLeave() {
      tooltipTimeout.value = setTimeout(() => {
        tooltipVisible.value = false
        console.log('clearing visibility from mouseleave')
      }, 300)
    }
  }
))


watch(isHoveringTooltip, (value: boolean, _oldValue: boolean) => {
  if(value && tooltipTimeout.value) clearTimeout(tooltipTimeout.value)
  if(!value) tooltipVisible.value = false
})
</script>


<template>
  <h1>Demo calendar</h1>
  <FullCalender :options='calendarOptions' />
  <EventTooltip
    :visible="tooltipVisible || isHoveringTooltip"
    :x="tooltipX"
    :y="tooltipY"
    :title="tooltipTitle"
    :context="tooltipContext"
    :document-name="tooltipDocName"
    :mouseenter="() => isHoveringTooltip = true"
    :mouseleave="() => isHoveringTooltip = false"
  />

</template>
