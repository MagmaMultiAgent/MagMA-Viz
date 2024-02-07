<script>
    import {ValueBoard} from "./ValueBoard.js";
    import {GrayScaleBoard} from "./GrayScaleBoard.js";
    import {RGBBoard} from "./RGBBoard.js";

    export let data;
    export let selectedVisualizationSubType;
</script>

{#if selectedVisualizationSubType === "values"}
    <ValueBoard data={data} />
{:else if selectedVisualizationSubType === "RGBMap"}
    <RGBBoard data={data} />
{:else if selectedVisualizationSubType === "GrayscaleMap"}
    <GrayScaleBoard data={data} />
{/if}