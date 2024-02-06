<script>
    import { onMount, onDestroy, afterUpdate } from 'svelte';
    import { DataViewer } from "./DataViewer.js";

    let properties = {};
    let visualizations = [];

    let container, propertySelector;
    let ws;
    onMount(() => {
        container = document.querySelector("table#container");
        propertySelector = document.querySelector("select#propertySelector");

        let clientId = Date.now();
        ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
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

    function addVisualization() {
        let currentDate = new Date();
        let timestamp = currentDate.getTime();
        visualizations = [...visualizations, timestamp];
    }

</script>

<h1>Lux AI 2</h1>
<div>Hello there!</div>

<div id="settings">
    <button on:click={addVisualization}>Add visualization</button>
</div>

<div id="visualizations">
    {#each visualizations as visualization}
        <DataViewer {properties} id={visualization} />
    {/each}
</div>


<style>
    #settings {
        display: flex;
        flex-direction: row;
        align-items: center;
    }
</style>