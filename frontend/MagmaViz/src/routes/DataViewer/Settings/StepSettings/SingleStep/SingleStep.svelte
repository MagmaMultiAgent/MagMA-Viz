<script>
    import {onMount} from "svelte";


    export let episodes;

    export let settings;


    let slider;
    onMount(() => {
        if (slider && settings && settings.step) {
            slider.value = parseInt(settings.step);
        }
    });

    $: episodeIDs = Object.keys(episodes);
    let steps = {};
    let stepIDs = [];
    let envIDs = [];
    let maxStep = 0;
    let minStep = 0;
    $: {
        if(settings === undefined) {
            settings = {};
        }
        if(settings.episode === undefined) {
            settings.episode = "";
        }
        if(settings.step === undefined) {
            settings.step = "";
        }
        if(settings.env === undefined) {
            settings.env = "";
        }
    }
    $: {
        if(settings && settings.episode !== undefined && episodes && settings.episode in episodes && episodes[settings.episode] !== steps) {
            steps = episodes[settings.episode];
            stepIDs = Object.keys(steps);
            maxStep = Math.max(...stepIDs.map(Number), 0);
            minStep = Math.min(...stepIDs.map(Number), maxStep);
        }
    }
    $: {
        if(settings && settings.step && steps && settings.step in steps && steps[settings.step] !== envIDs) {
            envIDs = steps[settings.step];
        }
    }
    $: {
        if (slider && settings && settings.step !== "") {
            slider.value = parseInt(settings.step);
        }
    }

    function updateStep(event) {
        if(!settings) {
            return;
        }

        settings.step = event.target.value.toString();
    }

    function incrementStep() {
        if(!settings) {
            return;
        }

        if(parseInt(settings.step) >= maxStep) {
            return;
        }

        settings.step = (parseInt(settings.step) + 1).toString();
    }

    function decrementStep() {
        if(!settings) {
            return;
        }

        if(parseInt(settings.step) <= minStep) {
            return;
        }

        settings.step = (parseInt(settings.step) - 1).toString();
    }
</script>

<div class="container">
    <div class="top-row">
        <label for="episodeSelector">Episode:</label>
        <select id="episodeSelector" name="episodeSelector" bind:value="{settings.episode}">
            {#each episodeIDs as episodeID}
                <option value="{episodeID}">{episodeID}</option>
            {/each}
        </select>

        <label for="stepSelector">Step:</label>
        <select id="stepSelector" name="stepSelector" bind:value="{settings.step}">
            {#each stepIDs as stepID}
                <option value="{stepID}">{stepID}</option>
            {/each}
        </select>

        <label for="envSelector">Environment:</label>
        <select id="envSelector" name="envSelector" bind:value="{settings.env}">
            {#each envIDs as envID}
                <option value="{envID}">{envID}</option>
            {/each}
        </select>
    </div>
    <div class="bottom-row">
        <button on:click={() => decrementStep()} class="button">-</button>
        <input type="range" min="{minStep}" max="{maxStep}" bind:this={slider} on:input={updateStep} class="slider" id="step-slider">
        <button on:click={() => incrementStep()} class="button">+</button>
    </div>
</div>

<style>
    * {
        background-color: dimgray;
        color: white;
    }

    select, option, button {
        background-color: darkgray;
        color: black;
    }

    .container{
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 10px;
    }

    .top-row, .bottom-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-bottom: 4px;
    }

    .bottom-row {
        width: 100%;
    }

    label {
        margin-left: 5px;
        margin-right: 2px;
    }

    input {
        width: 100%;
    }
</style>
