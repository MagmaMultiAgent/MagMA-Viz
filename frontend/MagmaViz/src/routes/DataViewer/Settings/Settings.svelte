<script>
    import {visualizationTypes} from "$lib/visualizationTypes.js";
    import {MainSettings} from "./MainSettings/MainSettings.js";
    import {StepSettings} from "./StepSettings/StepSettings.js";


    export let properties;

    export let settings = {};


    let mainSettings = {};
    let stepSettings = {};
    $: propertyName = (mainSettings && mainSettings.propertyName) ? mainSettings.propertyName : "";
    $: visualizationType = (mainSettings && mainSettings.visualizationType) ? mainSettings.visualizationType : "";
    $: settings.main = {...mainSettings};
    $: settings.step = {...stepSettings};

    $: propertyNames = Object.keys(properties);
    $: propertyInfo = propertyName in properties ? properties[propertyName] : {};
    $: episodes = "step_ids" in propertyInfo ? propertyInfo["step_ids"] : {};
    $: visualizationInfo = (visualizationType in visualizationTypes) ? visualizationTypes[visualizationType] : {};
    $: displayMultipleSteps = "displayMultipleSteps" in visualizationInfo ? visualizationInfo["displayMultipleSteps"] : false;
    $: settings.main = {...settings.main, "displayMultipleSteps": displayMultipleSteps};
</script>

<div class="container">
    <MainSettings
        {propertyNames}
        bind:settings={mainSettings}
    ></MainSettings>
    <StepSettings
        {episodes}
        {displayMultipleSteps}
        bind:settings={stepSettings}
    ></StepSettings>
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 8px;
    }
</style>
