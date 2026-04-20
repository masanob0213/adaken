<script setup>
import HelloWorld from './views/components/HelloWorld.vue'
import HeaderComponent from '@/views/components/Header/Main.vue'
import { ref, onMounted } from "vue";

const result = ref(null);

onMounted(async () => {
  const res = await fetch("/api/ping");
  console.log(res)
  result.value = await res.json();
});

</script>

<template>
  <HeaderComponent />
  <router-view />
  <div>
    <a href="https://vite.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld msg="Vite + Vue" />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
