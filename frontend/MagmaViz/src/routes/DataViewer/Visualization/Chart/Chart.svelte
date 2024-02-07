<script>
    import { onMount, onDestroy } from 'svelte';
    import Chart from 'chart.js/auto';

    export let id;
    export let data;

    let chartData = {};
    let stepIDs = [];

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

        const ctx = document.getElementById("chart_"+id.toString()).getContext('2d');
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: stepIDs,
                datasets: Object.values(chartData).map((data, index) => ({
                    label: `Line ${index + 1}`,
                    data: data,
                    fill: false,
                    borderColor: getRandomColor(),
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

    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    $: {
        generateChartData(data);
        if (chart) {
            chart.data.labels = stepIDs;
            chart.data.datasets = Object.values(chartData).map((data, index) => ({
                label: `Line ${index + 1}`,
                data: data,
                fill: false,
                borderColor: getRandomColor(),
                tension: 0.1
            }));
            chart.update();
        }
    }
</script>

<canvas id="chart_{id}"></canvas>