<script setup lang="ts">
import { ref } from 'vue'
import { type components } from '@/models'
import { useEventStore } from '@/stores/eventStore'
import { useInputFileStore } from '@/stores/fileStore'
import { RouterLink } from 'vue-router'
import { NavArrowDownSolid, NavArrowUpSolid } from '@iconoir/vue'

type ExtractedEventResponse = components['schemas']['ExtractedEventResponse']

const eventStore = useEventStore()
const fileStore = useInputFileStore()
const showAllFiles = ref<Boolean>(false)
const DEFAULT_FILES_TO_SHOW = 3
const processing = ref<Boolean>(false)

// When user selects files, add them to unprocessed array
// Overwrite old array, as users might realize they have mis-input a document
// Or they may select one or more of the same document, and we don't want to double process docs
function handleFiles(event: Event) {
  const target = event.target as HTMLInputElement
  if(!target.files) return
  fileStore.unprocessed = Array.from(target.files)
}

async function sendFilesForProcessing() {
  // TODO: Could try to enforce/validate the data format before sending to api?
  const formData = new FormData()
  for(const file of fileStore.unprocessed) {
    formData.append("files", file)
  }

  try {
    processing.value = true
    const res = await fetch(import.meta.env.VITE_DOCX_PARSING_SERVICE_URL, {
      method: "POST",
      body: formData,
    })

    const result = await res.json() as ExtractedEventResponse
    // Concatonate events so we aren't losing previously processed document events
    eventStore.events = eventStore.events.concat(result.events)
    fileStore.processed = fileStore.unprocessed
    fileStore.unprocessed = []
  } catch(e) {
    console.error(e)
    alert('Failed to upload files or parse dates')
  } finally {
    processing.value = false
  }
}
</script>

<template>
  <div class="flex flex-row w-full justify-between items-center">
    <div class="flex flex-row justify-start">
      <div class="flex flex-col p-2">
      <!-- Custom button/label so that we don't get the ugly, default file input styling -->
      <label for="docx-upload" style="cursor: pointer;" 
        class="border p-2 w-fit hover:bg-blue-700 bg-blue-500 text-white rounded-md p-2 mt-2">Choose Word Documents
        <input type="file" id="docx-upload" multiple accept=".docx" @change="handleFiles" style="display: none;"/>
      </label>
      </div>
      <div  class="flex flex-col">
        <RouterLink :to="`/document/${file.name}`" v-for="file of (showAllFiles ? fileStore.unprocessed : fileStore.unprocessed.slice(0, DEFAULT_FILES_TO_SHOW))" 
          class="hover:text-blue-400 hover:!underline">
          {{ file.name }}
        </RouterLink>
        <div v-if="fileStore.unprocessed.length > DEFAULT_FILES_TO_SHOW && !showAllFiles">+{{ fileStore.unprocessed.length - DEFAULT_FILES_TO_SHOW }} more...</div>
      </div>
      <button v-if="fileStore.unprocessed.length > DEFAULT_FILES_TO_SHOW" @click="showAllFiles = !showAllFiles">
        <NavArrowDownSolid v-if="!showAllFiles"></NavArrowDownSolid>
        <NavArrowUpSolid v-else></NavArrowUpSolid>
      </button>
    </div>
    
    <div v-if="processing" class="fixed inset-0 z-50 bg-black opacity-50 flex items-center justify-center pointer-events-auto">
      <div class="sk-chase text-blue-500">
        <div class="sk-chase-dot"></div>
        <div class="sk-chase-dot"></div>
        <div class="sk-chase-dot"></div>
        <div class="sk-chase-dot"></div>
        <div class="sk-chase-dot"></div>
        <div class="sk-chase-dot"></div>
      </div>
    </div>
    <button :disabled="(!fileStore.unprocessed.length)" @click="sendFilesForProcessing" 
      class="w-fit border bg-blue-500 text-white rounded-md p-2 mt-2 disabled:bg-gray-500 hover:bg-blue-700">
      Add Dates To Calendar
    </button>
  </div>
</template>
