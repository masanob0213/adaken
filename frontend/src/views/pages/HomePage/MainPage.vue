<template>
    <div class="home">
      <!-- <BaseCard>
        <h1>Home</h1>
        <p>Design System bootstrap ✅</p>
        <BaseButton>Primary</BaseButton>
        <BaseButton variant="ghost">Ghost</BaseButton>
        <BaseButton variant="danger">Danger</BaseButton>
      </BaseCard>
  
      <BaseCard>
        <BaseInput v-model="text" label="Sample" />
        <p>{{ text }}</p>
      </BaseCard> -->
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  // import BaseButton from '@/views/components/base/BaseButton.vue'
  // import BaseCard from '@/views/components/base/BaseCard.vue'
  // import BaseInput from '@/views/components/base/BaseInput.vue'
  
  import './Main.scss'
  
  const text = ref('')
  </script>