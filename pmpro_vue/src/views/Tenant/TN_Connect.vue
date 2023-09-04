<template>
    <div class="connect">
        <h1>Connect with Landlords</h1>
        <hr>
        <h2>Your property:</h2>
        <div v-if="properties">
            <h1 class="inline">{{ properties[0].property.address }} - </h1>
            <button @click="leaveProperty()">Leave</button>
            <br>
            <h2 class="inline">Tenants: </h2>
            <h3 class="inline" v-for="tenant in properties[0].tenants">
                {{ tenant.first_name }} {{ tenant.last_name }},
            </h3>
            <div class="error" v-for="error in leavePropertyErrors">
                <h3>{{ error }}</h3>
            </div>
            <br>
        </div>
        <div v-else>
            <h3>You have not joined a property yet. Please see your invitations.</h3>
            <br>
        </div>
        <div class="error" v-for="error in getPropertyErrors">
            <h3>{{ error }}</h3>
        </div>
        <hr>
        <h2>Incoming Invitations:</h2>
        <div v-if="invitations">
            <div v-for="invitation in invitations">
                <h2 class="inline">{{ invitation.property.address }} from </h2>
                <h3 class="inline">{{ invitation.landlord_first_name }} {{ invitation.landlord_last_name }} @{{ invitation.landlord_username }}</h3>
                <button @click="acceptInvite(invitation.property.address)">Accept</button> - 
                <button @click="deleteInvite(invitation.property.address, invitation.tenant.username)">Delete</button>
            </div>
            <div class="error" v-for="error in manageInvitationErrors">
                <h3>{{ error }}</h3>
            </div>
        </div>
        <div v-else>
            <h3>You currently have no invitations. Please request an invite from your prospective landlord.</h3>
            <br>
        </div>
        <div class="error" v-for="error in getInvitationErrors">
            <h3>{{ error }}</h3>
        </div>
    </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import { useStore } from 'vuex';

export default {
    name: 'TN_Connect',
    setup() {
        const properties = ref(null)
        const getPropertyErrors = ref([])

        const leavePropertyErrors = ref([])

        const invitations = ref(null)
        const getInvitationErrors = ref([])

        const manageInvitationErrors = ref([])

        const store = useStore()

        onMounted(() => {
            getProperties()
            getInvitations()
        })
        function getProperties() {
            getPropertyErrors.value = []
            store.dispatch('getProperties')
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            getPropertyErrors.value.push(response.errors[i])
                        }
                    } else {
                        properties.value = response.data
                    }
                })
        }
        function getInvitations() {
            getInvitationErrors.value = []
            store.dispatch('getInvitations')
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            getInvitationErrors.value.push(response.errors[i])
                        }
                    } else {
                        invitations.value = response.data
                    }
                })
        }
        function acceptInvite(address) {
            manageInvitationErrors.value = []
            const context = {
                address: address
            }
            store.dispatch('acceptInvitation', context)
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            manageInvitationErrors.value.push(response.errors[i])
                        }
                    } else {
                        getProperties()
                        getInvitations()
                    }
                })
        }
        function deleteInvite(address, username) {
            manageInvitationErrors.value = []
            const context = {
                property_address: address,
                tenant_username: username
            }
            store.dispatch('deleteInvitation', context)
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            manageInvitationErrors.value.push(response.errors[i])
                        }
                    } else {
                        getInvitations()
                    }
                })
        }
        function leaveProperty() {
            leavePropertyErrors.value = []
            store.dispatch('leaveProperty', {})
                .then(response => {
                    if (!response.success) {
                        leavePropertyErrors.value.push(response.error)
                    } else {
                        getProperties()
                        getInvitations()
                    } 
                })
        }
        return {
            properties,
            getPropertyErrors,
            leavePropertyErrors,
            invitations,
            getInvitationErrors,
            manageInvitationErrors,
            leaveProperty,
            acceptInvite,
            deleteInvite
        }
    }
}
</script>

<style>
.inline {
    display: inline;
}
.error {
    color: red;
}
</style>