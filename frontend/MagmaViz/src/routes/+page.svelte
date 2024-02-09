<script>
    import { onMount, onDestroy } from 'svelte';
    import { id, connectWebSocket } from "$lib/utils.js";
    import { DataViewer } from "./DataViewer/DataViewer.js";
    import { Header } from "./Header/Header.js";

    let properties = {};

    let ws;
    onMount(() => {
        ws = connectWebSocket();
        ws.onmessage = function(event) {
            console.log("Received data");
            properties = JSON.parse(event.data);
        };
    });
    onDestroy(() => {
        if (ws === undefined) {
            return;
        }
        ws.close();
    });

    let items = [id()];

    function addVisualization() {
        items = [...items, id()];
    }

</script>

<Header/>

<div id="settings">
    <button on:click={addVisualization}>Add visualization</button>
</div>

<div class="grid-container">
    {#each Object.entries(items) as [ind, item]}
        <DataViewer {properties} id={item} />
    {/each}
</div>


<style>
    @font-face {
        font-family: 'Roboto';
        src: url('/fonts/Roboto-Regular.ttf') format('ttf');
        font-weight: normal;
        font-style: normal;
    }

    @font-face {
        font-family: 'Roboto';
        src: url('/fonts/Roboto-Bold.ttf') format('ttf');
        font-weight: bold;
        font-style: normal;
    }

    :global(*) {
        font-family: 'Roboto', Arial, sans-serif;
    }

    * {
        background-color: gray;
        color: white;
    }

    button {
        background-color: darkgray;
        color: black;
    }

    #settings {
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-left: 10px;
    }

    #settings button {
        margin-right: 5px;
    }

    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
        gap: 10px;
        padding: 10px;
    }

    :global(html), :global(body) {
        background-color: gray;
        color: white;
        margin: 0;
        padding: 0;
        border: 0;
    }

</style>