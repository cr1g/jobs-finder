<template>
    <div id="app">
        <Navbar></Navbar>
        <ShowJobs></ShowJobs>
        <Footer></Footer>
    </div>
</template>

<script>
    import Footer from './components/Footer'
    import JobsTable from './components/JobsTable'
    import Navbar from './components/Navbar'
    import ShowJobs from './components/ShowJobs'

    export default {
        name: 'app',
        components: {
            Footer,
            JobsTable,
            Navbar,
            ShowJobs,
        }
    }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #2c3e50;
    }
</style>
