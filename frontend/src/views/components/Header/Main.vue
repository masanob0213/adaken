<template>
    <header class="header">
        <div class="header-inner">
            <div class="header-title-wrapper">
                <p class="header-title-text"><label class="header-title-text-label">ADA</label>KEN</p>
            </div>
            <div class="header-search-wrapper"></div>
        </div>
    </header>
</template>

<script setup>
</script>

<style scoped lang="scss">
.header {
    &-inner {
        display: flex;
    }

    &-title {
        &-wrapper {}
        &-text {
            &-label {
                color: $color-main;
            }
        }
    }

}
</style>