<script>
    import {getDataForStep, getDataForEpisode, getAllData} from "./Api.js";

    import {Visualization} from "./Visualization/Visualization.js";
    import {Settings} from "./Settings/Settings.js";

    export let id;
    export let properties;

    let displayMultipleSteps = false;
    let selectedPropertyName = "";
    let selectedVisualizationType = "";
    let selectedVisualizationSubType = "";
    let selectedSingleStepEpisode = "";
    let selectedStep = "";
    let selectedEnv = "";
    let selectedMultipleStepMode = "";
    let selectedMultipleStepEpisode = "";

    // Get data
    let data = {};
    $: {
        if(!displayMultipleSteps) {
            if(selectedPropertyName && selectedSingleStepEpisode && selectedStep) {
                getDataForStep(selectedPropertyName, selectedSingleStepEpisode, selectedStep)
                    .then(response => data = (selectedEnv in response) ? response[selectedEnv] : {})
                    .catch(error => console.error(error));
            }
        } else {
            if(selectedMultipleStepMode === "display all") {
                if(selectedPropertyName) {
                    getAllData(selectedPropertyName)
                        .then(response => {
                            let _data = {};
                            for(let episodeID in response) {
                                for(let stepID in response[episodeID]) {
                                    if(!(stepID in _data)) {
                                        _data[stepID] = {};
                                    }
                                    for(let envID in response[episodeID][stepID]) {
                                        if(!(envID in _data[stepID])) {
                                            _data[stepID][envID] = [];
                                        }
                                        _data[stepID][envID].push(response[episodeID][stepID][envID]);
                                    }
                                }
                            }
                            data = _data;
                        })
                        .catch(error => console.error(error));
                }
            } else if(selectedMultipleStepMode === "display episode") {
                if(selectedPropertyName && selectedMultipleStepEpisode) {
                    getDataForEpisode(selectedPropertyName, selectedMultipleStepEpisode)
                        .then(response => data = response)
                        .catch(error => console.error(error));
                }
            } else {
                data = {};
            }
        }
    }

</script>

<div class="container">

    <Settings
        {properties} bind:selectedPropertyName={selectedPropertyName} bind:displayMultipleSteps={displayMultipleSteps}
        bind:selectedVisualizationType={selectedVisualizationType} bind:selectedVisualizationSubType={selectedVisualizationSubType}
        bind:selectedSingleStepEpisode={selectedSingleStepEpisode} bind:selectedStep={selectedStep} bind:selectedEnv={selectedEnv}
        bind:selectedMultipleStepMode={selectedMultipleStepMode} bind:selectedMultipleStepEpisode={selectedMultipleStepEpisode}
    />

    <Visualization {id} {data} {selectedVisualizationType} {selectedVisualizationSubType} />
</div>

<style>
    .id {
        position: absolute;
        top: 0;
        left: 0;
        font-size: 10px;
        margin: 0;
        padding: 0;
        border: 0;
    }

    .container {
        width: 100%;
        height: 100%;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 1px solid black;
        position: relative;
    }
</style>