<script setup lang="ts">
import UploadComponent from '@/components/UploadComponent.vue';
import CalendarComponent from '@/components/CalendarComponent.vue';
</script>

<template>
  <div class="flex flex-col w-full h-full overflow-y-auto items-center">
    <UploadComponent />
    <CalendarComponent />
  </div>
</template>
