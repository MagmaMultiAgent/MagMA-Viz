<script>
    import { onMount, onDestroy } from 'svelte';
    import { id, connectWebSocket, getKeysFromLocalStorage, saveToLocalStorage, getFromLocalStorage } from "$lib/utils.js";
    import { DataViewer } from "./DataViewer/DataViewer.js";
    import { Header } from "./Header/Header.js";
    import { saveData, loadData } from "./Api.js";

    let properties = {};

    let ws;
    let initDone = false;
    onMount(() => {
        ws = connectWebSocket();
        ws.onmessage = function(event) {
            properties = JSON.parse(event.data);
        };

        initDone = true;
        configs = getSavedConfigs();
    });
    onDestroy(() => {
        if (ws === undefined) {
            return;
        }
        ws.close();
    });

    let items = [];

    function addVisualization() {
        let newVisualization = [id(), {}];
        items = [...items, newVisualization];
    }

    let config = "";
    let configs = [];
    $: {
        loadItems(config);
    }

    let saveConfigName = "";

    function saveItems(name) {
        if(name === "" || !items || !initDone) {
            return;
        }

        let itemsJSON = JSON.stringify(items.map(([_, settings]) => settings));
        if(!itemsJSON) {
            return;
        }

        console.log("Saving config with name " + name);
        saveToLocalStorage(`items`, name, itemsJSON);
        configs = getSavedConfigs();
    }

    function loadItems(name) {
        if(name === "" || !initDone) {
            console.log("Init not done yet, not loading config");
            return;
        }

        let itemsJSON = getFromLocalStorage(`items`, name);
        if(!itemsJSON) {
            console.log("No items found in local storage under key " + name);
            return;
        }

        console.log("Loading config with name " + name);
        let _items = JSON.parse(itemsJSON);
        items = [];
        for (let i = 0; i < _items.length; i++) {
            addVisualization();
            items[i][1] = _items[i];
        }
    }

    function getSavedConfigs() {
        if(!initDone) {
            console.log("Init not done yet, no saved configs");
            return [];
        }

        return getKeysFromLocalStorage("items");
    }

    let dataViewers = [];
    function refreshAll() {
        for (let i = 0; i < dataViewers.length; i++) {
            dataViewers[i].triggerUpdate();
        }
    }

    let refreshInterval = undefined;
    function setRefreshPeriod(event) {
        if(!initDone) {
            console.log("Init not done yet, not setting refresh period");
            return;
        }
        if(event.target.value) {
            console.log("Setting refresh period to " + event.target.value);
        }
        if(refreshInterval !== undefined) {
            clearInterval(refreshInterval);
        }
        if(!event.target.value) {
            console.log("Refresh period cleared");
            return;
        }
        let minutes = parseInt(event.target.value);
        refreshInterval = setInterval(refreshAll, minutes * 60 * 1000);
    }

    let selectedFile = "";
    $: {
        if(selectedFile) {
            loadData(selectedFile);
        }
    }

</script>

<Header/>

<div id="settings">
    <button on:click={addVisualization}>Add visualization</button>

    <button on:click={refreshAll}>Refresh All</button>
    <label for="refreshPeriodSelector">Refresh periodically:</label>
    <select id="refreshPeriodSelector" on:change={setRefreshPeriod}>
        <option value="">none</option>
        <option value="1">1 minute</option>
        <option value="2">2 minutes</option>
        <option value="5">5 minutes</option>
        <option value="10">10 minutes</option>
    </select>

    <button on:click={saveData}>Save</button>
    <input type="file" bind:value={selectedFile}>

    <div id="configs">
        <label for="configSelector">Configs:</label>

        <select id="configSelector" bind:value={config}>
            {#each configs as config}
                <option value={config}>{config}</option>
            {/each}
        </select>

        <button on:click={() => loadItems(config)}>Load</button>

        <input type="text" bind:value={saveConfigName} placeholder="New config name..." />

        <button on:click={() => saveItems(saveConfigName)}>Save</button>
    </div>
</div>

<div class="grid-container">
    {#each Object.entries(items) as [ind, [id, settings]]}
        <DataViewer {properties} id={id} bind:settings={settings} bind:this={dataViewers[ind]} />
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

    #settings, #configs {
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-left: 10px;
    }

    #settings {
        position: relative;
    }

    #configs {
        position: absolute;
        right: 0;
    }

    #settings *, #configs * {
        margin-right: 5px;
        color: black;
    }

    #settings select {
        background-color: darkgray;
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

    input::-webkit-input-placeholder, input:-moz-placeholder {
        color: darkgray;
    }

</style>