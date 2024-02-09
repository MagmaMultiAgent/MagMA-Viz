<script>
    import {getValueOrNone} from "$lib/utils.js";
    import {visualizationTypes} from "$lib/visualizationTypes.js";


    export let propertyNames;

    export let settings = {};


    let propertyName = "";
    let visualizationType = "";
    let visualizationSubType = "";

    $: settings = {
        "propertyName": propertyName,
        "visualizationType": visualizationType,
        "visualizationSubType": visualizationSubType
    };
    $: visualizationInfo = (visualizationType in visualizationTypes) ? visualizationTypes[visualizationType] : {};
    $: visualizationSubTypes = ("subTypes" in visualizationInfo) ? visualizationInfo["subTypes"] : [];

    $: {
        if (visualizationSubTypes.length > 0 && !visualizationSubTypes.includes(visualizationSubType)) {
            visualizationSubType = visualizationSubTypes[0];
        }
    }

</script>

<div class="container">
    <label for="propertySelector">Property:</label>
    <select id="propertySelector" name="propertySelector" bind:value="{propertyName}">
        {#each ["", ...propertyNames] as propertyName}
            <option value="{propertyName}">{getValueOrNone(propertyName)}</option>
        {/each}
    </select>

    <label for="visualizationTypeSelector">Visualization Type:</label>
    <select id="visualizationTypeSelector" name="visualizationTypeSelector" bind:value="{visualizationType}">
        {#each ["", ...Object.keys(visualizationTypes)] as visualizationType}
            <option value="{visualizationType}">{getValueOrNone(visualizationType)}</option>
        {/each}
    </select>

    {#if visualizationSubTypes.length > 0}
        <label for="visualizationSubTypeSelector">Visualization Sub Type:</label>
        <select id="visualizationSubTypeSelector" name="visualizationSubTypeSelector" bind:value="{visualizationSubType}">
            {#each visualizationSubTypes as visualizationSubType}
                <option value="{visualizationSubType}">{visualizationSubType}</option>
            {/each}
        </select>
    {/if}
</div>

<style>
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
