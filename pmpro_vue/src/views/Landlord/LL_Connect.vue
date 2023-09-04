<template>
    <div class="connect">
        <h1>Connect with Tenants</h1>
        <hr>
        <h2>Invite Tenants:</h2>
        <div v-if="tenants && properties">
            <form @submit.prevent="inviteTenant" onkeydown="return event.key != 'Enter';">
                <label for="tenants">Select tenant:</label>
                <br>
                <input type="text" v-model="query" placeholder="Search"/>
                <button type="button" @click="getTenants">Search</button>
                <br>
                <select name="tenants" id="tenants" multiple>
                    <option v-for="tenant in tenants" :value="tenant.username">
                        {{ tenant.first_name }} {{ tenant.last_name }} @{{ tenant.username }}
                    </option>
                </select>
                <br>
                <br>
                <label for="properties">Select property:</label>
                <br>
                <select name="properties" id="properties" multiple>
                    <option v-for="property in properties" :value="property.property.address">{{ property.property.address }}</option>
                </select>
                <br>
                <button type="submit" class="button-invite">Send Invite</button>
                <br>
            </form>
            <div class="error" v-for="error in inviteTenantErrors">
                <h3>{{ error }}</h3>
            </div>
        </div>
        <div v-else>
            <div v-if="!tenants">
                <h3>No tenants currently exist. Please inform your prospective tenants to signup!</h3>
            </div>
            <div v-if="!properties">
                <h3>You currently manage no properties. Please <router-link to="/landlord/manage-properties/">create</router-link> one now!</h3>
            </div>
            <br>
        </div>
        <div class="error" v-for="error in getPropertyErrors">
            <h3>{{ error }}</h3>
        </div>
        <div class="error" v-for="error in getTenantErrors">
            <h3>{{ error }}</h3>
        </div>
        <hr>
        <h2>Outgoing Invitations:</h2>
        <div v-if="invitations">
            <div v-for="invitation in invitations">
                <h2 class="inline">{{ invitation.property.address }} to </h2>
                <h3 class="inline">{{ invitation.tenant.first_name }} {{ invitation.tenant.last_name }} @{{ invitation.tenant.username }} </h3>
                <button @click="deleteInvite(invitation.property.address, invitation.tenant.username)">Delete</button>
            </div>
            <div class="error" v-for="error in deleteInviteErrors">
                <h3>{{ error }}</h3>
            </div>
        </div>
        <div v-else>
            <h3>You currently have no active outgoing invitations.</h3>
            <br>
        </div>
        <div class="error" v-for="error in getInvitationErrors">
            <h3>{{ error }}</h3>
        </div>
    </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useStore } from 'vuex'

export default {
    name: 'LL_Connect',
    setup() {
        const properties = ref(null)
        const getPropertyErrors = ref([])

        const query = ref('')
        const tenants = ref(null)
        const getTenantErrors = ref([])

        const invitations = ref(null)
        const getInvitationErrors = ref([])

        const inviteTenantErrors = ref([])
        const deleteInviteErrors = ref([])

        const store = useStore()
        
        onMounted(() => {
            getProperties()
            getTenants()
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
        function getTenants() {
            getTenantErrors.value = []
            const context = {
                query: query.value
            }
            store.dispatch('getTenants', context)
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            getTenantErrors.value.push(response.errors[i])
                        }
                    } else {
                        tenants.value = response.data
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
        function inviteTenant(submitEvent) {
            inviteTenantErrors.value = []

            const tenant_username = submitEvent.target.elements.tenants.value
            const property_address = submitEvent.target.elements.properties.value

            if (tenant_username == '' || property_address == '') {
                inviteTenantErrors.value.push('Please select both a tenant and property.')
            }
            if (inviteTenantErrors.value.length == 0) {
                const context = {
                    tenant_username: tenant_username,
                    property_address: property_address
                }
                store.dispatch('sendPropertyInvite', context)
                    .then(response => {
                        if (!response.success) {
                            for (let i = 0; i < response.errors.length; i++) {
                                inviteTenantErrors.value.push(response.errors[i])
                            }
                        } else {
                            getInvitations()
                        }
                    })
            }
        }
        function deleteInvite(address, username) {
            deleteInviteErrors.value = []
            const context = {
                property_address: address,
                tenant_username: username
            }
            store.dispatch('deleteInvitation', context)
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            deleteInviteErrors.value.push(response.errors[i])
                        }
                    } else {
                        getInvitations()
                    }
                })
        }
        return {
            properties,
            getPropertyErrors,
            query,
            tenants,
            getTenantErrors,
            invitations,
            getInvitationErrors,
            inviteTenantErrors,
            deleteInviteErrors,
            getTenants,
            inviteTenant,
            deleteInvite
        }
    }
}
</script>


<style>
.inline {
    display: inline;
}
.button-invite {
    background-color: blue;
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