<script>
    import { onMount, onDestroy } from 'svelte';
    import { id, connectWebSocket } from "$lib/utils.js";
    import { DataViewer } from "./DataViewer/DataViewer.js";

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

<div>Hello there!</div>

<div id="settings">
    <button on:click={addVisualization}>Add visualization</button>
</div>

<div class="grid-container">
    {#each Object.entries(items) as [ind, item]}
        <DataViewer {properties} id={item} />
    {/each}
</div>


<style>
    #settings {
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
        gap: 10px;
    }
</style>