<template>
    <div class="account">
        <h1>Account</h1>
        <hr>
        <h3>User Profile</h3>
        <form @submit.prevent="updateUser">
            <label>Username</label>
            <input type="text" v-model="username" :placeholder="user.username"/><br><br>
            <label>First Name</label>
            <input type="text" v-model="first" :placeholder="user.first_name"/>
            <label>Last Name</label>
            <input type="text" v-model="last" :placeholder="user.last_name"/>
            <label>Email</label>
            <input type="text" v-model="email" :placeholder="user.email"/><br>
            <button class="button-update" type="submit">Update Profile</button>
            <div class="error" v-for="error in errors">
                <h3>{{ error }}</h3>
            </div>
        </form>
        <button class="button-reset" @click="requestPasswordReset">Reset Password</button>
        <hr>
        <button class="button-logout" @click="logoutUser">Logout</button>
        <hr>
        <button class="button-delete" @click="deleteUser">Delete Account</button>
        <div class="error" v-for="error in deleteErrors">
            <h3>{{ error }}</h3>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import emailValidator from 'email-validator'

export default {
    name: 'Account',
    setup() {
        const user = ref({})
        const first = ref('')
        const last = ref('')
        const email = ref('')
        const username = ref('')
        const updateErrors = ref([])
        const deleteErrors = ref([])
        const store = useStore()

        onMounted(() => {
            user.value = store.getters.getUser
            first.value = user.value.first_name
            last.value = user.value.last_name
            email.value = user.value.email
            username.value = user.value.username
        })
        
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

        function updateUser() {
            updateErrors.value = []
            const context = {
                key: user.value.user_id,
                first: first.value,
                last: last.value,
                username: username.value,
                email: email.value
            }
            for (const key in context) {
                if (context[key] === '') {
                    updateErrors.value.push("One or more fields left blank. Please fill.")
                    break
                }
            }
            if (!emailValidator.validate(email.value)) {
                updateErrors.value.push("Email invalid.")
            }
            if (updateErrors.value.length == 0) {
                store.dispatch('updateUser', context)
                    .then(response => {
                        if (!response.success) {
                            for (let i = 0; i < response.errors.length; i++) {
                                updateErrors.value.push(response.errors[i])
                            }
                        }   
                    })
            }
        }

        function logoutUser() {
            store.dispatch('logoutUser')
        }
        
        function deleteUser() {
             deleteErrors.value = []
             const context = {
                key: user.value.user_id,
            }
            store.dispatch('deleteUser', context)
                .then(response => {
                    if (!response.success) {
                        deleteErrors.value.push(response.error)
                    }   
                })
        }

        function requestPasswordReset() {
            user.value = store.getters.getUser
            const context = {
                email: user.value.email
            }
            store.dispatch('requestResetEmail', context)
        }

        return {
            user,
            first,
            last,
            email,
            username,
            updateErrors,
            deleteErrors,
            updateUser,
            logoutUser,
            deleteUser,
            requestPasswordReset
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
.button-reset {
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
.button-update {
    background-color: darkblue;
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
.button-delete {
    background-color: black;
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