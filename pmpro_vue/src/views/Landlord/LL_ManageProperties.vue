<template>
    <div class="manage-properties">
        <h1>Manage Properties</h1>
        <hr>
        <div v-if="properties">
            <div v-for="property in properties">
                <h1 class="inline">{{ property.property.address }} - </h1>
                <button @click="updateProperty(property.property.address)">Update</button> - 
                <button @click="deleteProperty(property.property.address)">Delete</button>
                <br>
                <h2 class="inline">Tenants: </h2>
                <h3 class="inline" v-for="tenant in property.tenants">
                    {{ tenant.first_name }} {{ tenant.last_name }} <button @click="removeTenant(tenant.username)">Remove</button> ,
                </h3>
                <br>
                <br>
                <br>
            </div>
            <div class="error" v-for="error in managePropertyErrors">
                <h3>{{ error }}</h3>
            </div>
        </div>
        <div v-else>
            <h3>You have no properties yet. Please create one.</h3>
            <br>
        </div>
        <div class="error" v-for="error in getPropertyErrors">
            <h3>{{ error }}</h3>
        </div>
        <br><br><br>
        <hr>
        <h2>Create</h2>
        <form @submit.prevent="createProperty" onkeydown="return event.key != 'Enter';">
            <label>Address: </label>
            <input type="text" v-model="address"/><br>
            <label>Description: </label>
            <input type="text" v-model="description" placeholder="Optional"/><br>
            <button class="button-create">Create</button>
        </form>
        <div class="error" v-for="error in createPropertyErrors">
            <h3>{{ error }}</h3>
        </div>
    </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import { useStore } from 'vuex';

export default {
    name: 'LL_ManageProperties',
    setup() {
        const properties = ref(null)
        const getPropertyErrors = ref([])
        const managePropertyErrors = ref([])

        const address = ref('')
        const description = ref('')
        const createPropertyErrors = ref([])

        const store = useStore()

        onMounted(() => {
            getProperties()
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
        function createProperty() {
            createPropertyErrors.value = []
            if (address.value === '') {
                createPropertyErrors.value.push("Address left blank. Please fill.")
            }
            if (createPropertyErrors.value.length == 0) {
                const context = {
                    address: address.value,
                    description: description.value
                }
                store.dispatch('createProperty', context)
                    .then(response => {
                        if (!response.success) {
                            for (let i = 0; i < response.errors.length; i++) {
                                createPropertyErrors.value.push(response.errors[i])
                            }
                        }
                        getProperties()
                    })
            }
        }
        function updateProperty(address) {

        }
        function deleteProperty(address) {
            managePropertyErrors.value = []
            const context = {
                address: address
            }
            store.dispatch('deleteProperty', context)
                .then(response => {
                    if (!response.success) {
                        for (let i = 0; i < response.errors.length; i++) {
                            managePropertyErrors.value.push(response.errors[i])
                        }
                    } else {
                        getProperties()
                    }
                })
        }
        function removeTenant(username) {
            managePropertyErrors.value = []
            const context = {
                username: username
            }
            store.dispatch('removeTenant', context)
                .then(response => {
                    if (!response.success) {
                        managePropertyErrors.value.push(response.error)
                    } else {
                        getProperties()
                    } 
                })
        }

        return {
            properties,
            getPropertyErrors,
            managePropertyErrors,
            address,
            description,
            createPropertyErrors,
            createProperty,
            updateProperty,
            deleteProperty,
            removeTenant
        }
    }
}
</script>

<style>
.inline {
    display: inline;
}
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
.error {
    color: red;
}
</style>