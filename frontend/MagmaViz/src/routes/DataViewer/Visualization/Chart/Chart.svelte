<script>
    import { onMount, onDestroy } from 'svelte';
    import { getRGBFromHash } from "$lib/utils.js";
    import Chart from 'chart.js/auto';


    export let id;
    export let data;


    let chartData = {};
    let stepIDs = [];
    let chartName = "chart_" + id.toString();

    function generateChartData(data) {
        if (!data || data.constructor !== Object) {
            return;
        }

        chartData = {};
        stepIDs = Object.keys(data);

        for (const stepID in data) {
            for (const envID in data[stepID]) {
                if (!chartData[envID]) {
                    chartData[envID] = {};
                }
                let val = 0;
                if (stepID in data && envID in data[stepID]) {
                    val = data[stepID][envID]["data"];
                }
                chartData[envID][stepID] = val;
            }
        }
    }

    let chart;

    onMount(() => {
        generateChartData();

        const ctx = document.getElementById(chartName).getContext('2d');
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: stepIDs,
                datasets: Object.values(chartData).map((data, index) => ({
                    label: `Env ${index + 1}`,
                    data: data,
                    fill: false,
                    borderColor: getRGBFromHash(chartName + index.toString()),
                    tension: 0.1
                }))
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });

    onDestroy(() => {
        if (chart) {
            chart.destroy();
        }
    });

    $: {
        generateChartData(data);
        if (chart) {
            chart.data.labels = stepIDs;
            chart.data.datasets = Object.values(chartData).map((data, index) => ({
                label: `Line ${index + 1}`,
                data: data,
                fill: false,
                borderColor: getRGBFromHash(chartName + index.toString()),
                tension: 0.1
            }));
            chart.update();
        }
    }
</script>

<canvas id="{chartName}"></canvas>
