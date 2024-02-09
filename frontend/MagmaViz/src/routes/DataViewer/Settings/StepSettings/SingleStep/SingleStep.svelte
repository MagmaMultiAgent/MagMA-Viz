<script>
    import {onMount} from "svelte";


    export let displayMultipleSteps;
    export let episodes;

    export let settings = {};


    let episode = "";
    let step = "";
    let env = "";

    let slider;
    onMount(() => {
        if (slider && step !== "") {
            slider.value = parseInt(step);
        }
    });

    $: episodeIDs = Object.keys(episodes);
    $: settings = {
        "episode": episode,
        "step": step,
        "env": env
    };
    $ : {
        if(displayMultipleSteps) {
            episode = "";
        } else if (!episodeIDs.includes(episode)) {
            episode = episodeIDs[0];
        }
    }
    $: steps = (episode in episodes) ? episodes[episode] : {};
    $: stepIDs = Object.keys(steps);
    // stepIDs are in string
    $: maxStep = Math.max(...stepIDs.map(Number), 0);
    $: minStep = Math.min(...stepIDs.map(Number), maxStep);
    $: {
        if (stepIDs.length <= 0) {
            step = "";
        } else if (!stepIDs.includes(step)) {
            step = stepIDs[0];
        }
    }
    $: {
        if (slider && step !== "") {
            slider.value = parseInt(step);
        }
    }
    $: envIDs = (step in steps) ? steps[step] : [];

    function updateStep(event) {
        step = event.target.value.toString();
    }
</script>

<div class="container">
    <div class="top-row">
        <label for="episodeSelector">Episode:</label>
        <select id="episodeSelector" name="episodeSelector" bind:value="{episode}">
            {#each episodeIDs as episodeID}
                <option value="{episodeID}">{episodeID}</option>
            {/each}
        </select>

        <label for="stepSelector">Step:</label>
        <select id="stepSelector" name="stepSelector" bind:value="{step}">
            {#each stepIDs as stepID}
                <option value="{stepID}">{stepID}</option>
            {/each}
        </select>

        <label for="envSelector">Environment:</label>
        <select id="envSelector" name="envSelector" bind:value="{env}">
            {#each envIDs as envID}
                <option value="{envID}">{envID}</option>
            {/each}
        </select>
    </div>
    <div class="bottom-row">
        <button on:click={() => step = (parseInt(step) - 1).toString()} class="button">-</button>
        <input type="range" min="{minStep}" max="{maxStep}" bind:this={slider} on:input={updateStep} class="slider" id="step-slider">
        <button on:click={() => step = (parseInt(step) + 1).toString()} class="button">+</button>
    </div>
</div>

<style>
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
