<script>
    import {GET} from "$lib/utils.js";
    import {getValueOrNone} from "$lib/utils.js";
    import {visualizationTypes} from "$lib/visualizationTypes.js";

    export let properties;
    $: propertyNames = Object.keys(properties);

    export let id;

    let selectedPropertyName = "";
    $: propertyInfo = selectedPropertyName in properties ? properties[selectedPropertyName] : {};

    let selectedVisualizationType = "";
    $: visualizationInfo = (selectedVisualizationType in visualizationTypes) ? visualizationTypes[selectedVisualizationType] : {};
    $: visualizationSubTypes = ("subTypes" in visualizationInfo) ? visualizationInfo["subTypes"] : [];

    let selectedVisualizationSubType = "";
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
    let selectedMultipleStepMode = "";
    $: {
        if (multipleStepModes.length <= 0) {
            selectedMultipleStepMode = "";
        } else if (!multipleStepModes.includes(selectedMultipleStepMode)) {
            selectedMultipleStepMode = multipleStepModes[0];
        }
    }

    let selectedMultipleStepEpisode = "";
    $: {
        if(!displayMultipleSteps || selectedMultipleStepMode !== "display episode" || episodeIDs.length <= 0) {
            selectedMultipleStepEpisode = "";
        } else if (!episodeIDs.includes(selectedMultipleStepEpisode)) {
            selectedMultipleStepEpisode = episodeIDs[0];
        }
    }


    // Displaying single step
    let selectedSingleStepEpisode = "";
    $ : {
        if(displayMultipleSteps) {
            selectedSingleStepEpisode = "";
        } else if (!episodeIDs.includes(selectedSingleStepEpisode)) {
            selectedSingleStepEpisode = episodeIDs[0];
        }
    }
    $: steps = (selectedSingleStepEpisode in episodes) ? episodes[selectedSingleStepEpisode] : {};
    $: stepIDs = Object.keys(steps);
    let selectedStep = "";
    $: {
        if (stepIDs.length <= 0) {
            selectedStep = "";
        } else if (!stepIDs.includes(selectedStep)) {
            selectedStep = stepIDs[0];
        }
    }
    $: envIDs = (selectedStep in steps) ? steps[selectedStep] : [];
    let selectedEnvID = "";
    $: {
        if (envIDs.length <= 0) {
            selectedEnvID = "";
        } else if (!envIDs.includes(selectedEnvID)) {
            selectedEnvID = envIDs[0];
        }
    }


    // Get data

    let data = {};

    async function getDataForStep(property, episode, step, env) {
        try {
            const response = await GET(`http://localhost:8000/api/getDataForStep?propertyName=${property}&episode=${episode}&step=${step}&env=${env}`)
            console.log(response);
            return response;
        } catch (error) {
            console.error('Error updating property info:', error);
            throw error;
        }
    }

    async function getAllData(property) {
        try {
            const response = await GET(`http://localhost:8000/api/getAllData?propertyName=${property}`)
            console.log(response);
            return response;
        } catch (error) {
            console.error('Error updating property info:', error);
            throw error;
        }
    }

    async function getDataForEpisode(property, episode) {
        try {
            const response = await GET(`http://localhost:8000/api/getDataForEpisode?propertyName=${property}&episode=${episode}`)
            console.log(response);
            return response;
        } catch (error) {
            console.error('Error updating property info:', error);
            throw error;
        }
    }

    $: {
        if(!displayMultipleSteps) {
            getDataForStep(selectedPropertyName, selectedSingleStepEpisode, selectedStep, selectedEnvID)
                .then(response => data = response)
                .catch(error => console.error(error));
        } else {
            if(selectedMultipleStepMode === "display all") {
                getAllData(selectedPropertyName)
                    .then(response => data = response)
                    .catch(error => console.error(error));
            } else if(selectedMultipleStepMode === "display episode") {
                getDataForEpisode(selectedPropertyName, selectedMultipleStepEpisode)
                    .then(response => data = response)
                    .catch(error => console.error(error));
            }
        }
    }

</script>

<div id="container">
    <label id="id">ID: {id}</label>

    <h2>{selectedPropertyName}</h2>

    <div id="settings">
        <div id="main-settings">
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
        <div id="step-settings">
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
                <select id="envSelector" name="envSelector" bind:value="{selectedEnvID}">
                    {#each envIDs as env}
                        <option value="{env}">{env}</option>
                    {/each}
                </select>
            {/if}
        </div>
    </div>

    <div>
        <p>Property Dtype: {propertyInfo["dtype"]}</p>
    </div>
</div>

<style>
    #id {
        position: absolute;
        top: 0;
        left: 0;
        font-size: 10px;
        margin: 0;
        padding: 0;
        border: 0;
    }

    #container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 1px solid black;
        position: relative;
    }

    #settings {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    #main-settings, #step-settings {
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    label {
        margin-left: 5px;
    }
</style>