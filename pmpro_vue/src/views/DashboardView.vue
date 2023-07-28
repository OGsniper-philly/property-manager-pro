<template>
    <div class="dashboard">
        <h1>Welcome to your dashboard, {{ user.username }}</h1>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
    name: 'Dashboard',
    setup() {
        const user = ref({})
        const store = useStore()

        onMounted(() => {
            user.value = store.getters.getUser
        })

        return {
            user,
        }
    }
}
</script>

<style>

</style>