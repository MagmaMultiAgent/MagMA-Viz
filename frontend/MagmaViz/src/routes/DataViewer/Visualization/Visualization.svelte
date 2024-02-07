<script>
    import {Table} from "./Table/Table.js";
    import {Chart} from "./Chart/Chart.js"

    export let id;
    export let data;
    export let selectedVisualizationType;
    export let selectedVisualizationSubType;

</script>

<div class="container">
    {#if selectedVisualizationType === "table" || Array.isArray(data)}
        <Table {data} {selectedVisualizationSubType} />
    {:else if selectedVisualizationType === "chart"}
        <Chart {id} {data} {selectedVisualizationSubType} />
    {/if}
</div>

<style>
    .container {
        width: 100%;
        height: 100%;
        overflow: hidden;
    }
</style>
