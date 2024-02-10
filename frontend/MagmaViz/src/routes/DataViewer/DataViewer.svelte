<script>
    import {getDataForStep, getDataForEpisode, getAllData} from "./Api.js";

    import {Visualization} from "./Visualization/Visualization.js";
    import {Settings} from "./Settings/Settings.js";

    export let id;
    export let properties;
    export let settings;

    export function triggerUpdate() {
        if(settings) {
            updateData(propertyName, settings.step, displayMultipleSteps);
        }
    }


    $: displayMultipleSteps = (settings && settings.main && settings.main.displayMultipleSteps) ? settings.main.displayMultipleSteps : false;
    $: propertyName = (settings && settings.main && settings.main.propertyName) ? settings.main.propertyName : "";
    $: visualizationType = (settings && settings.main && settings.main.visualizationType) ? settings.main.visualizationType : "";
    $: visualizationSubType = (settings && settings.main && settings.main.visualizationSubType) ? settings.main.visualizationSubType : "";

    // Get data
    let data = {};
    $: {
        if(settings) {
            updateData(propertyName, settings.step, displayMultipleSteps);
        }
    }

    function updateData(propertyName, stepSettings, displayMultipleSteps) {
        if(!propertyName || !stepSettings) return;

        data = {};
        if(propertyName && stepSettings) {
            if (!displayMultipleSteps) {
                updateDataWithSingleStep(propertyName, stepSettings.singleStep);
            } else {
                updateDataWithMultipleSteps(propertyName, stepSettings.multipleStep);
            }
        }
    }

    function updateDataWithSingleStep(propertyName, settings) {
        if(!propertyName || !settings) return;

        let episode = settings.episode;
        let step = settings.step;
        let env = settings.env;
        if(episode === undefined || step === undefined || env === undefined) return;

        getDataForStep(propertyName, episode, step)
            .then(response => {
                if(!response || response.message) return;

                data = (env in response) ? response[env] : {};
            })
            .catch(error => {
                console.error(error);
                data = {};
            });
    }

    function updateDataWithMultipleSteps(propertyName, settings) {
        if(!propertyName || !settings) return;

        let mode = settings.mode;
        if(!mode) return;

        if(mode === "display all") {
            if(propertyName) {
                getAllData(propertyName)
                    .then(response => {
                        if(!response || response.message) return;

                        let _data = {}
                        for (let episodeID in response) {
                            let episode = response[episodeID];
                            for (let stepID in episode) {
                                if (stepID in _data) {
                                    console.error("Duplicate stepID in response");
                                    return;
                                }

                                _data[stepID] = episode[stepID];
                            }
                        }
                        data = _data;
                    })
                    .catch(error => {
                        console.error(error);
                        data = {};
                    });
            }
        } else if(mode === "display episode") {
            let episode = settings.episode;
            if(!episode) return;

            if(propertyName && episode) {
                getDataForEpisode(propertyName, episode)
                    .then(response => {
                        if(!response || response.message) return;

                        data = response;
                    })
                    .catch(error => {
                        console.error(error);
                        data = {};
                    });
            }
        } else {
            data = {};
        }
    }

</script>

<div class="container">
    <button class="refresh" on:click={() => {
        if(settings) {
            updateData(propertyName, settings.step, displayMultipleSteps);
        }
    }}>⟳</button>

    <Settings {properties} bind:settings={settings} />

    <Visualization {id} {data} {visualizationType} {visualizationSubType} />
</div>

<style>
    * {
        background-color: dimgray;
        color: white;
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
        border-radius: 10px;
    }

    .refresh {
        position: absolute;
        top: 5px;
        left: 5px;
    }
</style>
