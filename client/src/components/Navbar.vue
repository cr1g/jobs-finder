<template>
    <nav id="navbar">
        <h3>JOBS</h3>
    </nav>
</template>

<script>
    import { bus } from "../main"

    export default {
        name: "Navbar",
        methods: {
            filterJobsEvent(filter) {
                bus.$emit("filterJobsEvent", filter)
            }
        }
    }
</script>

<style>
    #navbar {
        background-color: #343A40;
        height: 55px;
        color: #BFCDC9;
        display: table;
        width: 100%;
    }

    h3 {
        display: table-cell;
        vertical-align: middle;
        text-align: center;
    }
</style>