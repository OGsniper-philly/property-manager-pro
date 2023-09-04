<template>
    <div class="connect">
        <h1>Connect</h1>
        <hr>
        <!-- LANDLORD SCREEN -->
        <div v-if="is_landlord">
            <h1>Manage Properties:</h1>
            <hr>
            <div v-if="properties">
                <div v-for="property in properties">
                    <h1 style="display: inline;">{{ property.property.address }} - </h1>
                    <button>Update</button> - 
                    <button @click="deleteProperty(property.property.address)">Delete</button><br>
                    <h2 style="display: inline;">Tenants: </h2>
                    <h3 style="display: inline;" v-for="tenant in property.tenants">
                        {{ tenant.first_name }} <button @click="removeTenant(tenant.username)">Remove</button> ,
                    </h3>
                    <div class="error" v-for="error in editPropertyErrors">
                        <h3>{{ error }}</h3>
                    </div>
                    <br><br><br>
                </div>
            </div>
            <div v-else>
                <br><h2>You have no properties yet. Please create one.</h2><br>
            </div>
            <div class="error" v-for="error in properyErrors">
                <h3>{{ error }}</h3>
            </div>
            <h3>Create a Property:</h3>
            <form @submit.prevent="createProperty" onkeydown="return event.key != 'Enter';">
                <label>Address: </label>
                <input type="text" v-model="address"/><br>
                <label>Description: </label>
                <input type="text" v-model="description" placeholder="Optional"/><br>
                <button class="button-create">Create</button>
            </form>
            <div class="error" v-for="error in createErrors">
                <h3>{{ error }}</h3>
            </div>
            <hr>
            <h1>Invite Tenants:</h1>
            <hr>
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
                    <br><br>
                    <label for="properties">Select tenant's property:</label>
                    <br>
                    <select name="properties" id="properties" multiple>
                        <option v-for="property in properties" :value="property.property.address">{{ property.property.address }}</option>
                    </select>
                    <br>
                    <button type="submit" class="button-invite">Invite</button>
                    <br>
                </form>
                <div class="error" v-for="error in inviteTenantErrors">
                    <h3>{{ error }}</h3>
                </div>
            </div>
            <div v-else>
                <br><h2>You either have no properties or no free tenants exist. Please inform prospective tenants to signup!</h2><br>
            </div>
            <div class="error" v-for="error in tenantErrors">
                <h3>{{ error }}</h3>
            </div>
        </div>
        <!-- TENANT SCREEN -->
        <div v-else>
            <h1>Your property:</h1>
            <hr>
            <div v-if="properties">
                <h1 style="display: inline;">{{ properties[0].property.address }} - </h1>
                <button @click="leaveProperty()">Leave</button><br>
                <h2 style="display: inline;">Tenants: </h2>
                <h3 style="display: inline;" v-for="tenant in properties[0].tenants">
                    {{ tenant.first_name }},
                </h3>
                <div class="error" v-for="error in leavePropertyErrors">
                    <h3>{{ error }}</h3>
                </div>
                <br><br><br>
            </div>
            <div v-else>
                <br><h2>You have not joined a property yet. Please see your invitations.</h2><br>
            </div>
            <div class="error" v-for="error in properyErrors">
                <h3>{{ error }}</h3>
            </div>
            <hr>
            <h1>Property Invitations:</h1>
            <hr>
            <div v-if="tenantInvitations">
                <div v-for="invitation in tenantInvitations">
                    <h1 style="display: inline;">{{ invitation.property.address }} - </h1>
                    <h2 style="display: inline;">{{ invitation.landlord_first_name }} {{ invitation.landlord_last_name }} @{{ invitation.landlord_username }}</h2>
                    <button @click="acceptInvite(invitation.property.address)">Accept</button> - 
                    <button @click="deleteInvite(invitation.property.address, invitation.tenant.username)">Delete</button>
                </div>
                <div class="error" v-for="error in editInviteErrors">
                    <h3>{{ error }}</h3>
                </div>
            </div>
            <div v-else>
                <h2>You can no invitations. Please request an invite from your prospective landlord.</h2><br>
            </div>
            <div class="error" v-for="error in getTenantInviteErrors">
                <h3>{{ error }}</h3>
            </div>
        </div>
    </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import { useStore } from 'vuex';


export default{
    name: "Connect",
    setup() {
        const is_landlord = ref(false)

        const properties = ref(null)
        const properyErrors = ref([])

        const tenants = ref(null)
        const tenantErrors = ref([])

        const editPropertyErrors = ref([])

        const query = ref('')
        const queryErrors = ref([])

        const inviteTenantErrors = ref([])

        const tenantInvitations = ref(null)
        const getTenantInviteErrors = ref([])

        const leavePropertyErrors = ref([])
        const editInviteErrors = ref([])

        const address = ref('')
        const description = ref('')
        const createErrors = ref([])

        const store = useStore()

        onMounted(() => {
            const user = store.getters.getUser
            is_landlord.value = user.is_landlord

            if (is_landlord.value) {
                getTenants()
            } 
            else {
                getInvitations()
            }

            getProperties()
        })

        function getProperties() {
            properyErrors.value = []
            store.dispatch('getProperties')
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            properyErrors.value.push(response.errors[i])
                        }
                    } else {
                        properties.value = response.data
                    }
                })
        }

        function getTenants() {
            tenantErrors.value = []
            const context = {
                query: query.value
            }
            store.dispatch('getTenants', context)
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            tenantErrors.value.push(response.errors[i])
                        }
                    } else {
                        tenants.value = response.data
                    }
                })
        }

        function getInvitations() {
            getTenantInviteErrors.value = []
            store.dispatch('getInvitations')
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            getTenantInviteErrors.value.push(response.errors[i])
                        }
                    } else {
                        console.log(response.data)
                        tenantInvitations.value = response.data
                    }
                })
        }

        function acceptInvite(address) {
            editInviteErrors.value = []
            const context = {
                address: address
            }
            store.dispatch('acceptInvitation', context)
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            editInviteErrors.value.push(response.errors[i])
                        }
                    } else {
                        getProperties()
                        getInvitations()
                    }
                })
        }

        function deleteInvite(address, username) {
            editInviteErrors.value = []
            const context = {
                property_address: address,
                tenant_username: username
            }
            store.dispatch('deleteInvitation', context)
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            editInviteErrors.value.push(response.errors[i])
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
                        editInviteErrors.value = []
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
                        }
                    })
            }  
        }

        function removeTenant(username) {
            editPropertyErrors.value = []
            const context = {
                username: username
            }
            store.dispatch('removeTenant', context)
                .then(response => {
                    if (!response.success) {
                        editPropertyErrors.value.push(response.error)
                    } else {
                        getProperties()
                    } 
                })
        }
        
        function createProperty() {
            createErrors.value = []
            const context = {
                address: address.value,
                description: description.value
            }
            if (context.address === '') {
                createErrors.value.push("Address left blank. Please fill.")
            }
            if (createErrors.value.length == 0) {
                store.dispatch('createProperty', context)
                    .then(response => {
                        if (!response.success) {
                            for (let i = 0; i < response.errors.length; i++) {
                                createErrors.value.push(response.errors[i])
                            }
                        }
                        getProperties()
                    })
            }
        }

        function deleteProperty(address) {
            editPropertyErrors.value = []
            const context = {
                address: address
            }
            store.dispatch('deleteProperty', context)
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            editPropertyErrors
                            .value.push(response.errors[i])
                        }
                    } else {
                        getProperties()
                    }
                })
        }

        return {
            is_landlord,
            properties,
            properyErrors,
            tenants,
            tenantErrors,
            query,
            queryErrors,
            inviteTenantErrors,
            tenantInvitations,
            getTenantInviteErrors,
            editInviteErrors,
            editInviteErrors,
            leavePropertyErrors,
            address,
            description,
            createErrors,
            createProperty,
            getTenants,
            getProperties,
            acceptInvite,
            deleteInvite,
            leaveProperty,
            inviteTenant,
            deleteProperty,
            removeTenant
        }
    }
}
</script>

<style>
.button-create {
    background-color: green;
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