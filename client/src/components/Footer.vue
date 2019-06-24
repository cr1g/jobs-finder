<template>
    <footer>
        <span>Made by <a href="https://www.github.com/cr1g" target="_blank">Cristian Gira</a>. Contact: cristian.gira22@gmail.com</span>
    </footer>
</template>

<script>
    export default {
        name: "Footer"
    }
</script>

<style scoped>
    footer {
        width: 100%;
        height: 50px;
        background-color: black;
        position: absolute;
        bottom: 0;
        display: table;
    }

    span {
        display: table-cell;
        vertical-align: middle;
        text-align: center;
        color: white;
        font-size: 13px;
    }
</style>