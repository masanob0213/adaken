<template>
    <div class="page">
        <main class="main">
            <!-- 新着作品 -->
            <section class="section">
                <div class="section-title">
                    <span class="icon icon-clock" aria-hidden="true">
                        <!-- clock icon -->
                        <svg viewBox="0 0 24 24" fill="none">
                            <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" />
                            <path d="M12 7v6l4 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                        </svg>
                    </span>
                    <h2>新着作品</h2>
                </div>

                <div class="new-grid">
                    <div class="poster skeleton"></div>
                    <div class="poster skeleton"></div>
                </div>
            </section>

            <!-- ジャンルから絞り込む -->
            <section class="section">
                <div class="section-title">
                    <span class="icon icon-search" aria-hidden="true">
                        <!-- search icon -->
                        <svg viewBox="0 0 24 24" fill="none">
                            <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2" />
                            <path d="M20 20l-4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                        </svg>
                    </span>
                    <h2>ジャンルから絞り込む</h2>
                </div>

                <div class="chips">
                    <button class="chip">
                        着衣 <span class="chip-arrow">▶</span>
                    </button>
                    <button class="chip">
                        複数 <span class="chip-arrow">▶</span>
                    </button>
                    <button class="chip">
                        巨乳 <span class="chip-arrow">▶</span>
                    </button>
                    <button class="chip">
                        水着 <span class="chip-arrow">▶</span>
                    </button>
                </div>

                <div class="all-link">
                    <button class="all-link-btn">
                        全てのジャンルを見る <span class="all-link-arrow">→</span>
                    </button>
                </div>

                <div class="divider"></div>
            </section>

            <!-- 女優から絞り込む -->
            <section class="section">
                <div class="section-title">
                    <h2>女優から絞り込む</h2>
                </div>

                <div class="actress-grid">
                    <div class="actress-card">
                        <div class="actress-img skeleton"></div>
                        <div class="actress-name">女優名</div>
                    </div>
                    <div class="actress-card">
                        <div class="actress-img skeleton"></div>
                        <div class="actress-name">女優名</div>
                    </div>
                    <div class="actress-card">
                        <div class="actress-img skeleton"></div>
                        <div class="actress-name">女優名</div>
                    </div>
                </div>
            </section>
        </main>

        <!-- Floating button -->
        <button class="fab" aria-label="通知">
            <span class="fab-dot">0</span>
        </button>
    </div>
</template>
<script setup>
import { useMainScript } from "./MainScript.js";

const {
} = useMainScript();
</script>

<style scoped lang="scss"></style>