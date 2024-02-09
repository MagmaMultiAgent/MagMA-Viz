<script>
    export let displayMultipleSteps;
    export let episodes;

    export let settings = {};


    let mode = "";
    let episode = "";

    $: episodeIDs = Object.keys(episodes);
    $: settings = {
        "mode": mode,
        "episode": episode
    };
    $: modes = displayMultipleSteps ? ["display all", "display episode", "aggregate episodes"]: [];
    $: {
        if (modes.length <= 0) {
            mode = "";
        } else if (!modes.includes(mode)) {
            mode = modes[0];
        }
    }

    $: {
        if(!displayMultipleSteps || mode !== "display episode" || episodeIDs.length <= 0) {
            episode = "";
        } else if (!episodeIDs.includes(episode)) {
            episode = episodeIDs[0];
        }
    }
</script>

<div class="container">
    <label for="multipleStepModeSelector">Multiple Step Mode:</label>
    <select id="multipleStepModeSelector" name="multipleStepModeSelector" bind:value="{mode}">
        {#each modes as mode}
            <option value="{mode}">{mode}</option>
        {/each}
    </select>

    {#if mode === "display episode"}
        <label for="episodeSelector">Episode:</label>
        <select id="episodeSelector" name="episodeSelector" bind:value="{episode}">
            {#each episodeIDs as episodeID}
                <option value="{episodeID}">{episodeID}</option>
            {/each}
        </select>
    {/if}
</div>

<style>
    * {
        background-color: dimgray;
        color: white;
    }

    select, option {
        background-color: darkgray;
        color: black;
    }

    .container {
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-bottom: 4px;
    }

    label {
        margin-left: 5px;
        margin-right: 2px;
    }
</style>
