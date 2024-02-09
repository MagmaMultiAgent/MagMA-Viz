<script>
    import {getValueOrNone} from "$lib/utils.js";
    import {visualizationTypes} from "$lib/visualizationTypes.js";


    export let propertyNames;
    export let visualizationInfo;

    export let settings;


    let visualizationSubTypes = [];
    $: {
        console.log("Main");

        if (settings === undefined) {
            settings = {};
        }
        if(settings.propertyName === undefined) {
            settings.propertyName = "";
        }
        if(settings.visualizationType === undefined) {
            settings.visualizationType = "";
        }
        if(settings.visualizationSubType === undefined) {
            settings.visualizationSubType = "";
        }
    }
    $: visualizationSubTypes = visualizationInfo["subTypes"] ? visualizationInfo["subTypes"] : [];
    $: {
        if(visualizationSubTypes.length > 0 && visualizationSubTypes && !visualizationSubTypes.includes(settings.visualizationSubType)) {
            settings.visualizationSubType = visualizationSubTypes[0];
        }
    }
</script>

<div class="container">
    <label for="propertySelector">Property:</label>
    <select id="propertySelector" name="propertySelector" bind:value="{settings.propertyName}">
        {#each ["", ...propertyNames] as propertyName}
            <option value="{propertyName}">{getValueOrNone(propertyName)}</option>
        {/each}
    </select>

    <label for="visualizationTypeSelector">Type:</label>
    <select id="visualizationTypeSelector" name="visualizationTypeSelector" bind:value="{settings.visualizationType}">
        {#each ["", ...Object.keys(visualizationTypes)] as visualizationType}
            <option value="{visualizationType}">{getValueOrNone(visualizationType)}</option>
        {/each}
    </select>

    {#if visualizationSubTypes.length > 0}
        <label for="visualizationSubTypeSelector">Sub Type:</label>
        <select id="visualizationSubTypeSelector" name="visualizationSubTypeSelector" bind:value="{settings.visualizationSubType}">
            {#each visualizationSubTypes as visualizationSubType}
                <option value="{visualizationSubType}">{visualizationSubType}</option>
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
