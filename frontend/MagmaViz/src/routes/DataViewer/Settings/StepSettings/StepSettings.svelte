<script>
    import {MultipleStep} from "./MultipleStep/MultipleStep.js";
    import {SingleStep} from "./SingleStep/SingleStep.js";


    export let episodes;
    export let displayMultipleSteps;

    export let settings;


    $: {
        if(settings === undefined) {
            settings = {};
        }
    }
</script>
<div class="container">
    {#if displayMultipleSteps}
        <MultipleStep
            {episodes}
            bind:settings={settings.multipleStep}
        ></MultipleStep>
    {:else}
        <SingleStep
            {episodes}
            bind:settings={settings.singleStep}
        ></SingleStep>
    {/if}
</div>

<style>
    .container {
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-bottom: 4px;
    }
</style>
