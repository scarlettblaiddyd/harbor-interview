<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { SuperDoc } from '@harbour-enterprises/superdoc';
import { useInputFileStore } from '@/stores/fileStore';
import { useEventStore } from '@/stores/eventStore';
import { ArrowLeft } from '@iconoir/vue'

const fileStore = useInputFileStore();
const eventStore = useEventStore();
const route = useRoute()
const error = ref<string>("")

onMounted(() => {
    error.value = ""
    const docName = route.params.name as string
    if(!docName) {
        error.value = "Error: No document specified to load"
    }
    const file = fileStore.findFileByName(docName)
    if(!file) {
        error.value = `Error: Failed to load file '${docName}'`
    }
    new SuperDoc({
        selector: '#superdoc-container',
        documentMode: 'viewing',
        documents: [{
            id: 'uploaded-doc',
            type: 'docx',
            data: file
        }],
        // Don't seem to be able to get high constrast mode working
        onReady: async (event) => {
            const superdoc = event.superdoc
            console.log('Superdoc ready')
            superdoc.setHighContrastMode(true)
            console.log(superdoc)
            console.log(superdoc.highContrastModeStore)
            console.log(superdoc.setHighContrastMode)
            //
            if(eventStore.highlightedEvent) {
                // TODO: Superdoc doesn't seem to like searching for text across mutliple lines, and the context I'm pulling
                // from the document often includes newline chars. This is hacky but I'll just highlight the middle from the
                // context, that should be close enough to be useful
                const splitContext = eventStore.highlightedEvent.context.split('\n')
                const match = superdoc.search(splitContext[Math.floor((splitContext.length - 1) / 2)])[0]
                console.log(superdoc.goToSearchResult(match))
            }
           
        }
    })
})

</script>

<template>
    <div class="flex flex-col items-center h-full">
        <div class="flex flex-row w-full">
            <button class="flex flex-row group bg-blue-500 text-white rounded-md p-2 mt-2 w-fit hover:bg-blue-700">
            <ArrowLeft></ArrowLeft>
            <RouterLink class="hover:!underline" to="/">Back to Calendar</RouterLink>
            </button>
            <div class="flex flex-grow"></div>
        </div>
        
        <div v-if="error" class="color-red-500 text-lg">
            {{ error }}
        </div>
        <span>{{ route.params.name }}</span>
        <div v-if="!error" id="superdoc-container" class="bg-white h-full overflow-auto">
        </div>
    </div>
</template>
