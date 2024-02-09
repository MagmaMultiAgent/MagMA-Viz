<script>
    import {visualizationTypes} from "$lib/visualizationTypes.js";
    import {MainSettings} from "./MainSettings/MainSettings.js";
    import {StepSettings} from "./StepSettings/StepSettings.js";


    export let properties;

    export let settings;


    $: propertyNames = Object.keys(properties);
    let propertyName = "";
    let visualizationType = "";
    let propertyInfo = {};
    let episodes = {};
    let visualizationInfo = {};
    let displayMultipleSteps = false;
    $: {
        if(settings === undefined)
        {
            settings = {};
        }

        if(settings && settings.main)
        {
            if(settings.main.propertyName && settings.main.propertyName !== propertyName) {
                propertyName = settings.main.propertyName;
            }
            if(settings.main.visualizationType && settings.main.visualizationType !== visualizationType) {
                visualizationType = settings.main.visualizationType;
            }
        }
        if(visualizationTypes[visualizationType] && visualizationInfo !== visualizationTypes[visualizationType]) {
            visualizationInfo = visualizationTypes[visualizationType];
        }
        if(visualizationInfo && visualizationInfo.displayMultipleSteps !== undefined && visualizationInfo.displayMultipleSteps !== displayMultipleSteps) {
            if(displayMultipleSteps !== visualizationInfo.displayMultipleSteps) {
                displayMultipleSteps = visualizationInfo.displayMultipleSteps;
            }
            if(settings.main.displayMultipleSteps !== visualizationInfo.displayMultipleSteps) {
                settings.main.displayMultipleSteps = visualizationInfo.displayMultipleSteps;
            }
        }
    }
    $: {
        propertyInfo = properties[propertyName] ? properties[propertyName] : {};
        episodes = propertyInfo["step_ids"] ? propertyInfo["step_ids"] : {};
    }
</script>

<div class="container">
    <MainSettings
        {propertyNames}
        {visualizationInfo}
        bind:settings={settings.main}
    ></MainSettings>
    <StepSettings
        {episodes}
        {displayMultipleSteps}
        bind:settings={settings.step}
    ></StepSettings>
</div>

<style>
    * {
        background-color: dimgray;
        color: white;
    }

    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 8px;
    }
</style>
