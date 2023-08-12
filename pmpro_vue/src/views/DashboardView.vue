<template>
    <div class="dashboard">
        <h1>Welcome to your dashboard, {{ user.username }}</h1>
    </div>
</template>

<script>
import axiosInstance from '@/services/api'
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import HttpStatus from 'http-status-codes'

export default {
    name: 'Dashboard',
    setup() {
        const user = ref({})
        const store = useStore()

        onMounted(() => {
            user.value = store.getters.getUser
            testAuth()
        })
        function testAuth() {
            axiosInstance
                .get('auth/test/')
                .then(response => {
                    console.log(`Test: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
                })
                .catch(error => {
                    console.error(`Test: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
                })
        }

        return {
            user,
        }
    }
}
</script>

<style>

</style>