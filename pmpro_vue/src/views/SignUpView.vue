<template>
    <div class="signup">
        <h1>SignUp</h1>
        <form @submit.prevent="signup">
            <label>First Name:</label>
            <input type="text" v-model="first"><br>
            <label>Last Name:</label>
            <input type="text" v-model="last"><br>
            <label>Username:</label>
            <input type="text" v-model="username"><br>
            <label>Email:</label>
            <input type="text" v-model="email"><br>
            <label>Password:</label>
            <input type="password" v-model="password1"><br>
            <label>Repeat Password:</label>
            <input type="password" v-model="password2"><br>
            <input type="radio" id="landlord" name="user_status" @click="is_landlord = true">
            <label for="landlord">Landlord</label><br>
            <input type="radio" id="tenant" name="user_status" @click="is_landlord = false">
            <label for="tenant">Tenant</label><br>
            <button type="submit">Submit</button>
        </form>
        <div class="error" v-for="error in errors">
            <h3>{{ error }}</h3>
        </div>
    </div>
</template>

<script>
import emailValidator from 'email-validator'
import { ref, watch } from 'vue';
import { useStore } from 'vuex';

export default {
    name: 'Signup',
    setup() {
        const first = ref('')
        const last = ref('')
        const username = ref('')
        const email = ref('')
        const password1 = ref('')
        const password2 = ref('')
        const is_landlord = ref('')
        const errors = ref([])
        const store = useStore()

        watch(first, (newFirst) => {
            first.value = newFirst.replace(/[^A-Za-z]/g, '')
            first.value = first.value.substring(0, 15)
        })
        watch(last, (newLast) => {
            last.value = newLast.replace(/[^A-Za-z]/g, '')
            last.value = last.value.substring(0, 20)
        })
        watch(username, (newUsername) => {
            username.value = newUsername.replace(/[^A-Za-z0-9_]/g, '')
            username.value = username.value.substring(0, 10)
        })

        function signup() {
            errors.value = []
            const context = {
                first: first.value,
                last: last.value,
                username: username.value,
                email: email.value,
                password: password1.value,
                is_landlord: is_landlord.value
                
            }
            for (const key in context) {
                if (context[key] === '') {
                    errors.value.push("One or more fields left blank. Please fill.")
                    break
                }
            }
            if (!emailValidator.validate(email.value)) {
                errors.value.push("Email invalid.")
            }
            if (password1.value !== password2.value) {
                errors.value.push("Passwords do not match.")
            }
            if (is_landlord.value === '') {
                errors.value.push("Please select landlord or tenant.")
            }
            if (errors.value.length == 0) {
                store.dispatch('signupUser', context)
                    .then(response => {
                        if (!response.success) {
                            for (let i = 0; i < response.errors.length; i++) {
                                errors.value.push(response.errors[i])
                            }
                        }   
                    })
            }
        }
        return {
            first,
            last,
            username,
            email,
            password1,
            password2,
            is_landlord,
            errors,
            signup,
        }
    }
}
</script>

<style>
.error {
    color: red;
}
</style>