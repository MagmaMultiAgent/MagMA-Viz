<script>
    import { onMount } from 'svelte';
    let container, episodeSelector, stepSelector, propertySelector, slider, decreaseStateButton, increaseStateButton, currentStateElement;

    onMount(() => {
        // DOM elements
        container = document.querySelector("table#container");
        episodeSelector = document.querySelector("select#episodeSelector");
        stepSelector = document.querySelector("select#stepSelector");
        propertySelector = document.querySelector("select#propertySelector");
        slider = document.querySelector("input#stateSlider");
        decreaseStateButton = document.querySelector("button#decreaseState");
        increaseStateButton = document.querySelector("button#increaseState");
        currentStateElement = document.querySelector("span#currentState");

        slider.oninput = function() {
            selectStep(parseInt(this.value));
        }

        episodeSelector.onchange = function() {
            selectEpisode(parseInt(this.value), true);
        }

        stepSelector.onchange = function() {
            selectStep(parseInt(this.value));
        }

        propertySelector.onchange = function() {
            selectProperty(this.value);
        }

        decreaseStateButton.onclick = function() {
            if(selectedStep <= 0) {
                return;
            }
            selectStep(selectedStep - 1);
        }

        increaseStateButton.onclick = function() {
            if(selectedStep >= max_step) {
                return;
            }
            selectStep(selectedStep + 1);
        }

        let clientId = Date.now();
        let ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
        ws.onmessage = function(event) {
            episodes = JSON.parse(event.data);

            // Update episode selector
            episodeSelector.innerHTML = '';
            for (let key in episodes) {
                let option = document.createElement("option");
                option.value = key;
                option.text = key;
                episodeSelector.add(option);
            }
            if (selectedEpisode in episodes) {
                selectEpisode(selectedEpisode);
            } else {
                selectEpisode(parseInt(Object.keys(episodes)[0]), true);
            }
        };
    });

    let selectedEpisode = undefined;
    let selectedStep = undefined;
    let selectedProperty = undefined;

    let episodes = {};
    let steps = {};
    let properties = [];

    let max_step = -1;

    function adjustSlider(){
        slider.setAttribute("max", max_step.toString());
        currentStateElement.innerHTML = (selectedStep + 1) + " / " + (max_step + 1).toString();
    }

    function selectEpisode(episode, resetStep = false) {
        if (!(episode.toString() in episodes)) {
            console.log("Episode not found", episode);
            return;
        }
        console.log("Selecting episode", episode)

        selectedEpisode = episode;
        episodeSelector.value = selectedEpisode.toString();
        steps = episodes[selectedEpisode];
        max_step = Math.max(...Object.keys(steps).map(x => parseInt(x)));
        adjustSlider();

        stepSelector.innerHTML = '';
        for (let key in steps) {
            let option = document.createElement("option");
            option.value = key;
            option.text = key;
            stepSelector.add(option);
        }

        if (resetStep) {
            selectStep(parseInt(Object.keys(steps)[0]));
        }
    }

    function selectStep(step) {
        if (!Object.keys(steps).length || !(step.toString() in steps)){
            console.log("Step not found", step);
            return;
        }
        console.log("Selecting step", step)

        selectedStep = step;
        properties = steps[selectedStep];
        slider.value = selectedStep.toString();
        stepSelector.value = selectedStep.toString();
        adjustSlider();

        propertySelector.innerHTML = '';
        for (let i = 0; i < properties.length; i++) {
            let option = document.createElement("option");
            option.value = properties[i];
            option.text = properties[i];
            propertySelector.add(option);
        }

        if (properties.includes(selectedProperty)) {
            selectProperty(selectedProperty);
        } else {
            selectProperty(properties[0]);
        }
    }

    function selectProperty(property) {
        if (!properties.includes(property)) {
            console.log("Property not found", property);
            return;
        }
        console.log("Selecting property", property)

        selectedProperty = property;
        propertySelector.value = selectedProperty;

        let xhr = new XMLHttpRequest();
        xhr.open("GET", `http://localhost:8000/api/get_data?episode=${selectedEpisode}&step=${selectedStep}&propertyName=${selectedProperty}`, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                let response = xhr.responseText;
                let property = JSON.parse(response);

                if (property.dimensions.length === 3) {
                    drawTable(property["data"]);
                }
            }
        }
        xhr.send();
    }

    function drawTable(arrays){
        container.innerHTML = '';
        for (let i = 0; i < arrays.length; i++) {
            let row = container.insertRow(i);

            for (let j = 0; j < arrays[i].length; j++) {
                let cell = row.insertCell(j);

                let red = arrays[i][j][0];
                let green = arrays[i][j][1];
                let blue = arrays[i][j][2];

                cell.style.backgroundColor = "rgb(" + red + ", " + green + ", " + blue + ")";
                cell.style.border = "1px solid lightgray";
            }
        }
    }

</script>

<h1>Lux AI 2</h1>
<div>Hello there!</div>
<div>
    <label for="episodeSelector">Episode:</label>
    <select id="episodeSelector" name="episodeSelector"></select>
    <label for="stepSelector">Step:</label>
    <select id="stepSelector" name="stepSelector"></select>
    <label for="propertySelector">Property:</label>
    <select id="propertySelector" name="propertySelector"></select>
</div>
<div id="slidecontainer">
    <button id="decreaseState" type="button">-</button>
    <label for="stateSlider"></label><input type="range" min="0" max="0" value="0" class="slider" id="stateSlider">
    <button id="increaseState" type="button">+</button>
</div>
<span>State:</span>
<span id="currentState" style="font-weight:bold;color:red">1</span>
<div id="messages"></div>
<table id="container">
</table>

<style>
    #container {
        border-collapse: collapse;
    }

    /* And this to your table's `td` elements. */
    #container td {
        padding: 0;
        margin: 0;
        width: 10px;
        height: 10px;
    }

    #slidecontainer {
        display: flex;
        flex-direction: row;
    }
</style>