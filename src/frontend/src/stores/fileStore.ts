import { ref } from 'vue'
import { defineStore } from 'pinia'

// Holds refs to the files selected by the user so that they can be easily displayed with superdoc
export const useInputFileStore = defineStore('inputFiles', () => {
  const processed = ref<File[]>([])
  const unprocessed = ref<File[]>([])

  // Very naive function, for now just assume that if two documents have the same name they're inter-changable
  function findFileByName(fileName: string) : File | null {
    // no reason we check the processed files first
    let file = processed.value.find(file => file.name === fileName)
    if(file) return file
    file = unprocessed.value.find(file => file.name === fileName)
    if(file) return file

    return null;
  }

  return { processed, unprocessed, findFileByName }
})
