<template>
    <div class="account">
        <h1>Account</h1>
        <h3>User: {{ user.username }}</h3>
        <hr>
        <button class="button-logout" @click="logoutUser">Logout</button>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import toastMixin from '@/services/alerts';

export default {
    name: 'Account',
    setup() {
        const user = ref({})
        const store = useStore()

        onMounted(() => {
            user.value = store.getters.getUser
        })

        function logoutUser() {
            store.dispatch('logout')
        }

        return {
            user,
            logoutUser
        }
    }
}
</script>

<style>
.button-logout {
    background-color: darkred;
    border: none;
    color: white;
    padding: 10px 22px;
    margin: 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    cursor: pointer;
}
</style>