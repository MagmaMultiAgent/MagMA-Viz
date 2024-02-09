<script>
    export let displayMultipleSteps;
    export let episodes;

    export let settings = {};


    let episode = "";
    let step = "";
    let env = "";

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
    $: {
        if (stepIDs.length <= 0) {
            step = "";
        } else if (!stepIDs.includes(step)) {
            step = stepIDs[0];
        }
    }
    $: envIDs = (step in steps) ? steps[step] : [];
</script>

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

<style>
    label {
        margin-left: 5px;
        margin-right: 2px;
    }
</style>
