import { ref } from 'vue'
import { defineStore } from 'pinia'
import { type components } from '../models'

type ExtractedEvent = components["schemas"]["ExtractedEvent"]

export const useEventStore = defineStore('events', () => {
  const events = ref<ExtractedEvent[]>([])

  const highlightedEvent = ref<ExtractedEvent | null>()

  return { events, highlightedEvent }
})
