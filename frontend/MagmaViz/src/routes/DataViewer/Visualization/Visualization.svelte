<script>
    import {Table} from "./Table/Table.js";
    import {Chart} from "./Chart/Chart.js"


    export let id;
    export let data;
    export let visualizationType;
    export let visualizationSubType;

</script>

<div class="container">
    {#if visualizationType === "table" || Array.isArray(data)}
        <Table {data} {visualizationSubType} />
    {:else if visualizationType === "chart"}
        <Chart {id} {data} {visualizationSubType} />
    {/if}
</div>

<style>
    .container {
        width: 100%;
        height: 100%;
        overflow: hidden;
    }
</style>
