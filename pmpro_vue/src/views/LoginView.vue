<template>
    <div class="login">
        <h1>Login Page</h1>
        <hr>
        <form @submit.prevent="loginUser">
            <h3>Username</h3>
            <input type="text" v-model="username"><br>
            <h3>Password</h3>
            <input type="password" v-model="password"><br>
            <button class="button-login" type="submit">Login</button>
            <div class="error" v-for="error in errors">
                <h3>{{ error }}</h3>
            </div>
        </form>
        
    </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'

export default {
    name: 'Login',
    setup() {
        const username = ref('')
        const password = ref('')
        const errors = ref([])
        const store = useStore()
        
        function loginUser() {
            errors.value = []
            const credentials = {
                username: username.value, 
                password: password.value
            }
            store.dispatch('login', credentials)
                .then(status => {
                    switch(status) {
                        case 400:
                            errors.value.push("Please fill out all fields.")
                            break;
                        case 401:
                            errors.value.push("Username or password incorrect.")
                            break;
                        default:
                            errors.value.push("Something went wrong. Please try again later.")
                    }
                }) 
        }

        return {
            username,
            password,
            errors,
            loginUser,
        }
    }
}
</script>

<style>
.button-login {
    background-color: darkgreen;
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
.error {
    color: red;
}
</style>