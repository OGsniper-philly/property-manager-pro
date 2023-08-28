<template>
    <h1>Reset Password</h1>
    <hr>
    <form @submit.prevent="resetPassword">
        <label>New Password</label>
        <input type="password" v-model="new_password1"/><br><br>
        <label>Repeat New Password</label>
        <input type="password" v-model="new_password2"/><br><br>
        <button type="submit">Reset</button>
        <div class="error" v-for="error in errors">
            <h3>{{ error }}</h3>
        </div>
    </form>
</template>

<script>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

export default {
    name: 'ResetPassword',
    setup() {
        const route = useRoute()
        const new_password1 = ref('')
        const new_password2 = ref('')
        const errors = ref([])
        const store = useStore()

        function resetPassword() {
            errors.value = []
            if (new_password1.value !== new_password2.value) {
                errors.value.push("Passwords do not match.")
            }
            if (new_password1.value == '' || new_password2.value == '') {
                errors.value.push("Please fill out all fields.")
            }
            const token = route.query.token
            if (!token) {
                // No reset token present as URL parameter
                errors.value.push('An account has not been registered with this password reset.')
            }
            if (errors.value.length == 0) {
                const context = {
                    token: token,
                    password: new_password1.value
                }
                store.dispatch('resetPassword', context)
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
            new_password1,
            new_password2,
            errors,
            resetPassword,
        }
    }
}
</script>

<style>

</style>