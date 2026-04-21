<template>
    <div>
      <input v-model="title" type="text" placeholder="タイトル検索" />
      <button @click="fetchWorks">検索</button>
  
      <ul>
        <li v-for="work in works" :key="work.id">
          {{ work.name }}
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { useMainScript } from "./MainScript.js";
  
  const {
    title,
    works,
    fetchWorks,
  } = useMainScript();
  </script>
  
  <style scoped lang="scss"></style>