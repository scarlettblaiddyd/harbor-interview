<script setup lang="ts">
import { ref } from 'vue'
import { type components } from '../models'
import { useEventStore } from '@/stores/eventStore'

type ExtractedEventResponse = components['schemas']['ExtractedEventResponse']
type ExtractedEvent = components['schemas']['ExtractedEvent']

const selectedFiles = ref<File[]>([])
const dates = ref<ExtractedEvent[]>([])
const eventStore = useEventStore()

function handleFiles(event: Event) {
  const target = event.target as HTMLInputElement

  if(!target.files) return
  selectedFiles.value = Array.from(target.files)
  console.log(selectedFiles.value.length)
}


async function sendFilesForProcessing() {
  console.log("processing")
  const formData = new FormData()
  for(const file of selectedFiles.value) {
    formData.append("files", file)
  }

  try {
    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    })

    const result = await res.json() as ExtractedEventResponse
    console.log("Dates returned: " + JSON.stringify(result))
    dates.value = result.events
    eventStore.events = result.events
    console.log(result.events[0].date)
  } catch(e) {
    console.error(e)
    alert('Failed to upload files or parse dates')
  }
}
</script>

<template>
  <div class="flex flex-col p-2">
    <label for="docx-upload" style="cursor: pointer;" class="border p-1 w-fit">Choose Word Documents
      <input type="file" id="docx-upload" multiple accept=".docx" @change="handleFiles" style="display: none;"/>
    </label>
    <div v-for="file of selectedFiles" class="border-b w-fit">
      {{ file.name }}
    </div>
  </div>

  <button :disabled="!selectedFiles.length" @click="sendFilesForProcessing" class="border p-1 disabled:bg-gray-500">
    Add Dates To Calendar
  </button>

  <div v-if="eventStore.events?.length">
    <h3>📆 Extracted Dates:</h3>
    <ul>
      <li v-for="(d, i) in eventStore.events" :key="i">
        {{ d.date }} — {{ d.title }} ({{ d.document }})
        <br />
        <small>{{ d.context }}</small>
      </li>
    </ul>
  </div>
</template>
