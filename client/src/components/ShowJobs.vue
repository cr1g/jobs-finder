<template>
    <div class="container">
        <b-tabs content-class="mt-3" fill>
            <b-tab title="All" active @click="filterJobsEvent({'key': 'all', 'value': 1})"></b-tab>
            <b-tab title="Seen" @click="filterJobsEvent({'key': 'status', 'value': 'seen'})"></b-tab>
            <b-tab title="Unseen" @click="filterJobsEvent({'key': 'status', 'value': 'unseen'})"></b-tab>
            <b-tab title="Favourite" @click="filterJobsEvent({'key': 'favourite', 'value': 1})"></b-tab>
        </b-tabs>
        <JobsTable></JobsTable>
    </div>
</template>

<script>
    import JobsTable from '../components/JobsTable.vue'
    import { bus } from "../main"

    export default {
        name: "ShowJobs",
        components: {
            JobsTable
        },
        methods: {
            filterJobsEvent(filter) {
                bus.$emit("filterJobsEvent", filter)
            }
        }
    }
</script>

<style scoped>
    .container {
        margin-top: 50px;
    }
</style>