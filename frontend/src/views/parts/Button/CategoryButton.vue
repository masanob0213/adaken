<template>
    <div>
        <p>{{ label }}</p>
        <img src="@/assets/images/icons/category_allow.png"
    </div>

</template>

<script setup>
import { useMainScript } from "./MainScript.js";

const {
} = useMainScript();

const props = defineProps(['label']);

</script>

<style scoped lang="scss">
</style>