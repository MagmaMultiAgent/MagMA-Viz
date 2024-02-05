<script>
    import { onMount, onDestroy, afterUpdate } from 'svelte';

    import { GET } from '$lib/utils.js';

    let selectedPropertyName = "";
    let selectedEpisodeId = -1;
    let selectedStepId = -1;

    let episodes = {};

    let data = undefined;
    let rgbBoard = [];
    $: {
        if (data !== undefined && "dimensions" in data && "data" in data) {
            if (data["dimensions"].length === 3 && data["dimensions"][2] === 3) {
                rgbBoard = data["data"];
            } else {
                rgbBoard = [];
            }
        }
    }

    $: steps = selectedEpisodeId in episodes ? episodes[selectedEpisodeId] : {};
    $: properties = selectedStepId in steps ? steps[selectedStepId] : [];
    $: maxStep = Object.keys(steps).length ? Math.max(...Object.keys(steps).map(x => parseInt(x))) : -1;

    // Handle episode change
    $: {
        if (selectedEpisodeId < 0 || !(selectedEpisodeId.toString() in episodes)) {
            console.log("Episode not found", selectedEpisodeId);
            if (Object.keys(episodes).length) {
                selectedEpisodeId = parseInt(Object.keys(episodes)[0]);
            } else {
                selectedEpisodeId = -1;
            }
        }
    }

    // Handle step change
    $: {
        if (selectedStepId < 0 || !(selectedStepId.toString() in steps)) {
            console.log("Step not found", selectedStepId);
            if (Object.keys(steps).length) {
                selectedStepId = parseInt(Object.keys(steps)[0]);
            } else {
                selectedStepId = -1;
            }
        }
    }

    // Handle property change
    $: {
        if (selectedPropertyName === "" || !properties.includes(selectedPropertyName)) {
            console.log("Property not found", selectedPropertyName);
            if (properties.length) {
                selectedPropertyName = properties[0];
            } else {
                selectedPropertyName = "";
            }
        }
    }

    let container, episodeSelector, stepSelector, propertySelector, slider, decreaseStateButton, increaseStateButton, currentStateElement;
    let ws;
    onMount(() => {
        container = document.querySelector("table#container");
        episodeSelector = document.querySelector("select#episodeSelector");
        stepSelector = document.querySelector("select#stepSelector");
        propertySelector = document.querySelector("select#propertySelector");
        slider = document.querySelector("input#stateSlider");
        decreaseStateButton = document.querySelector("button#decreaseState");
        increaseStateButton = document.querySelector("button#increaseState");
        currentStateElement = document.querySelector("span#currentState");

        decreaseStateButton.onclick = function() {
            if(selectedStepId <= 0) {
                return;
            }
            selectedStepId -= 1;
        }

        increaseStateButton.onclick = function() {
            if(selectedStepId >= maxStep) {
                return;
            }
            selectedStepId += 1;
        }

        let clientId = Date.now();
        ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
        ws.onmessage = function(event) {
            console.log("Received data");
            episodes = JSON.parse(event.data);
        };
    });
    afterUpdate(() => {
        if (currentStateElement === undefined) {
            return;
        }
        currentStateElement.innerHTML = (selectedStepId + 1) + " / " + (maxStep + 1).toString();
    });
    onDestroy(() => {
        if (ws === undefined) {
            return;
        }
        ws.close();
    });

    // Fetch data
    $: {
        if( selectedEpisodeId > -1 && selectedStepId > -1 && selectedPropertyName !== "") {
            let response = GET(`http://localhost:8000/api/get_data?episode=${selectedEpisodeId}&step=${selectedStepId}&propertyName=${selectedPropertyName}`);
            response.then((res) => {
                data = res;
            }).catch((err) => {
                console.error(err.message);
            });
        }
    }

</script>

<h1>Lux AI 2</h1>
<div>Hello there!</div>
<div>
    <label for="episodeSelector">Episode:</label>
    <select id="episodeSelector" name="episodeSelector" bind:value="{selectedEpisodeId}">
        {#each Object.keys(episodes) as episode}
            <option value="{+episode}">{episode}</option>
        {/each}
    </select>
    <label for="stepSelector">Step:</label>
    <select id="stepSelector" name="stepSelector" bind:value="{selectedStepId}">
        {#each Object.keys(steps) as step}
            <option value="{+step}">{step}</option>
        {/each}
    </select>
    <label for="propertySelector">Property:</label>
    <select id="propertySelector" name="propertySelector" bind:value="{selectedPropertyName}">
        {#each properties as property}
            <option value="{property}">{property}</option>
        {/each}
    </select>
</div>
<div id="slidecontainer">
    <button id="decreaseState" type="button">-</button>
    <label for="stateSlider"></label><input type="range" min="0" bind:value={selectedStepId} max={maxStep} class="slider" id="stateSlider">
    <button id="increaseState" type="button">+</button>
</div>
<span>State:</span>
<span id="currentState" style="font-weight:bold;color:red">1</span>
<div id="messages"></div>
{#if rgbBoard.length > 0}
    <table id="container">
        {#each rgbBoard as row}
            <tr>
                {#each row as cell}
                    <td style="background-color: rgb({cell[0]}, {cell[1]}, {cell[2]})"></td>
                {/each}
            </tr>
        {/each}
    </table>
{/if}


<style>
    #container {
        border-collapse: collapse;
    }

    /* And this to your table's `td` elements. */
    #container td {
        padding: 0;
        margin: 0;
        width: 10px;
        height: 10px;
        border: 1px solid lightgray;
    }

    #slidecontainer {
        display: flex;
        flex-direction: row;
    }
</style>