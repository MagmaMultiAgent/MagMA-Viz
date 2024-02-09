<script>
    import {ValueBoard} from "./ValueBoard/ValueBoard.js";
    import {GrayScaleBoard} from "./GrayScaleBoard/GrayScaleBoard.js";
    import {RGBBoard} from "./RGBBoard/RGBBoard.js";


    export let data;
    export let visualizationSubType;
</script>

{#if visualizationSubType === "values"}
    <ValueBoard data={data} />
{:else if visualizationSubType === "RGBMap"}
    <RGBBoard data={data} />
{:else if visualizationSubType === "GrayscaleMap"}
    <GrayScaleBoard data={data} />
{/if}
