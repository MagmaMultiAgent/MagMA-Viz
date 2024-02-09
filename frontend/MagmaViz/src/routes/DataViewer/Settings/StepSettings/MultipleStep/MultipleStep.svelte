<script>
    export let episodes;

    export let settings;


    $: episodeIDs = Object.keys(episodes);
    const modes = ["display all", "display episode", "aggregate episodes"];
    $: {
        if(settings === undefined) {
            settings = {};
        }
        if(settings.mode === undefined) {
            settings.mode = "";
        }
        if(settings.episode === undefined) {
            settings.episode = "";
        }
    }
</script>

<div class="container">
    <label for="multipleStepModeSelector">Multiple Step Mode:</label>
    <select id="multipleStepModeSelector" name="multipleStepModeSelector" bind:value="{settings.mode}">
        {#each modes as mode}
            <option value="{mode}">{mode}</option>
        {/each}
    </select>

    {#if settings.mode === "display episode"}
        <label for="episodeSelector">Episode:</label>
        <select id="episodeSelector" name="episodeSelector" bind:value="{settings.episode}">
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
