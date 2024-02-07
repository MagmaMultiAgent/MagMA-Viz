<script>
    import {getValueOrNone} from "$lib/utils.js";
    import {visualizationTypes} from "$lib/visualizationTypes.js";

    export let properties;
    export let displayMultipleSteps;
    export let selectedPropertyName;
    export let selectedVisualizationType;
    export let selectedVisualizationSubType;
    export let selectedSingleStepEpisode;
    export let selectedStep;
    export let selectedEnv;
    export let selectedMultipleStepMode;
    export let selectedMultipleStepEpisode;


    $: propertyNames = Object.keys(properties);
    $: propertyInfo = selectedPropertyName in properties ? properties[selectedPropertyName] : {};

    $: visualizationInfo = (selectedVisualizationType in visualizationTypes) ? visualizationTypes[selectedVisualizationType] : {};
    $: visualizationSubTypes = ("subTypes" in visualizationInfo) ? visualizationInfo["subTypes"] : [];

    $: {
        if (visualizationSubTypes.length > 0 && !visualizationSubTypes.includes(selectedVisualizationSubType)) {
            selectedVisualizationSubType = visualizationSubTypes[0];
        }
    }

    $: displayMultipleSteps = "displayMultipleSteps" in visualizationInfo ? visualizationInfo["displayMultipleSteps"] : false;
    $: episodes = "step_ids" in propertyInfo ? propertyInfo["step_ids"] : {};
    $: episodeIDs = Object.keys(episodes);


    // Displaying multiple steps
    $: multipleStepModes = displayMultipleSteps ? ["display all", "display episode", "aggregate episodes"]: [];
    $: {
        if (multipleStepModes.length <= 0) {
            selectedMultipleStepMode = "";
        } else if (!multipleStepModes.includes(selectedMultipleStepMode)) {
            selectedMultipleStepMode = multipleStepModes[0];
        }
    }

    $: {
        if(!displayMultipleSteps || selectedMultipleStepMode !== "display episode" || episodeIDs.length <= 0) {
            selectedMultipleStepEpisode = "";
        } else if (!episodeIDs.includes(selectedMultipleStepEpisode)) {
            selectedMultipleStepEpisode = episodeIDs[0];
        }
    }


    // Displaying single step
    $ : {
        if(displayMultipleSteps) {
            selectedSingleStepEpisode = "";
        } else if (!episodeIDs.includes(selectedSingleStepEpisode)) {
            selectedSingleStepEpisode = episodeIDs[0];
        }
    }
    $: steps = (selectedSingleStepEpisode in episodes) ? episodes[selectedSingleStepEpisode] : {};
    $: stepIDs = Object.keys(steps);
    $: {
        if (stepIDs.length <= 0) {
            selectedStep = "";
        } else if (!stepIDs.includes(selectedStep)) {
            selectedStep = stepIDs[0];
        }
    }
    $: envIDs = (selectedStep in steps) ? steps[selectedStep] : [];

</script>
<div class="container">
    <div class="main-settings">
        <label for="propertySelector">Property:</label>
        <select id="propertySelector" name="propertySelector" bind:value="{selectedPropertyName}">
            {#each ["", ...propertyNames] as property}
                <option value="{property}">{getValueOrNone(property)}</option>
            {/each}
        </select>

        <label for="visualizationTypeSelector">Visualization Type:</label>
        <select id="visualizationTypeSelector" name="visualizationTypeSelector" bind:value="{selectedVisualizationType}">
            {#each ["", ...Object.keys(visualizationTypes)] as visualizationType}
                <option value="{visualizationType}">{getValueOrNone(visualizationType)}</option>
            {/each}
        </select>

        {#if visualizationSubTypes.length > 0}
            <label for="visualizationSubTypeSelector">Visualization Sub Type:</label>
            <select id="visualizationSubTypeSelector" name="visualizationSubTypeSelector" bind:value="{selectedVisualizationSubType}">
                {#each visualizationSubTypes as visualizationSubType}
                    <option value="{visualizationSubType}">{visualizationSubType}</option>
                {/each}
            </select>
        {/if}
    </div>
    <div class="step-settings">
        {#if displayMultipleSteps}
            <label for="multipleStepModeSelector">Multiple Step Mode:</label>
            <select id="multipleStepModeSelector" name="multipleStepModeSelector" bind:value="{selectedMultipleStepMode}">
                {#each multipleStepModes as mode}
                    <option value="{mode}">{mode}</option>
                {/each}
            </select>

            {#if selectedMultipleStepMode === "display episode"}
                <label for="episodeSelector">Episode:</label>
                <select id="episodeSelector" name="episodeSelector" bind:value="{selectedMultipleStepEpisode}">
                    {#each episodeIDs as episode}
                        <option value="{episode}">{episode}</option>
                    {/each}
                </select>
            {/if}
        {:else}
            <label for="episodeSelector">Episode:</label>
            <select id="episodeSelector" name="episodeSelector" bind:value="{selectedSingleStepEpisode}">
                {#each episodeIDs as episode}
                    <option value="{episode}">{episode}</option>
                {/each}
            </select>

            <label for="stepSelector">Step:</label>
            <select id="stepSelector" name="stepSelector" bind:value="{selectedStep}">
                {#each stepIDs as step}
                    <option value="{step}">{step}</option>
                {/each}
            </select>

            <label for="envSelector">Environment:</label>
            <select id="envSelector" name="envSelector" bind:value="{selectedEnv}">
                {#each envIDs as env}
                    <option value="{env}">{env}</option>
                {/each}
            </select>
        {/if}
    </div>
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 8px;
    }

    .main-settings, .step-settings {
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