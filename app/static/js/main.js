const button = document.getElementById('submit');

//create bar chart
function makeChart(matched){
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Gill Color', 'Spore Print Color', 'Population', 'Gill Size'],
        datasets: [{
            label: '# of Matches',
            data: [matched[0], matched[1], matched[2], matched[3]],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }

    });
}


//create line chart
function makeChart2(edible, poisonous) {
    const ctx = document.getElementById('myChart2').getContext('2d');
    const myLineChart2 = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Gill Color', 'Spore Print Color', 'Population', 'Gill Size'],
        datasets: [{
					label: 'Edible',
                    backgroundColor: '#336633',
					borderColor: '#336633',
					data: [edible[0], edible[1], edible[2], edible[3]],
					fill: false,
				}, {
					label: 'Poisonous',
                    backgroundColor: '#df0a15',
					borderColor: '#df0a15',
					fill: false,
					data: [poisonous[0], poisonous[1], poisonous[2], poisonous[3]],
				}]
    },
    options: {}
});
}

//create pie chart
function makeChart3(edible, poisonous) {
    const totalEdible = edible.reduce((a, b) => a + b, 0);
    const totalPoisonous = poisonous.reduce((a, b) => a + b, 0);
    const ctx = document.getElementById('myChart3').getContext('2d');
    const myLineChart3 = new Chart(ctx, {
    type: 'pie',
    data: {
            datasets: [{
                data: [
                    totalEdible,
                    totalPoisonous,
                ],
                backgroundColor: [
                    '#336633',
                    '#df0a15',
                ],
                label: 'Dataset 1'
            }],
            labels: [
                'Edible',
                'Poisonous'
            ]
			},
			options: {
				responsive: true
			}
});
}


//predict button main function
button.addEventListener('click', async event => {
    const gillColor = parseInt(document.getElementById('gill-color').value);
    const sporePrintColor = parseInt(document.getElementById('spore-print-color').value);
    const population = parseInt(document.getElementById('population').value);
    const gillSize = parseInt(document.getElementById('gill-size').value);
    const data = { gillColor, sporePrintColor, population, gillSize };
    let isError = false;

    //create post request
    const options = {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };
    const response = await fetch('classify', options);
    const json = await response.json();

    //parse response data
    const result = json.result;
    const matched = json.matched;
    const edible = json.edible;
    const poisonous = json.poisonous;

    const prediction = document.getElementById('prediction');

    //display results
    if(result === 'Poisonous'){
        prediction.className = "alert alert-danger";
        prediction.textContent = "This mushroom is poisonous!";
    }

    if(result === 'Edible'){
        prediction.className = "alert alert-success";
        prediction.textContent = "This mushroom is edible!";
    }

    if(result === 'Error'){
        prediction.className = "alert alert-warning";
        prediction.textContent = "There was an error - please try again";
        isError = true;
    }

    if(!isError) {
    document.getElementById('charts').style.display='block';
    }

    //display charts
    makeChart(matched);
    makeChart2(edible, poisonous);
    makeChart3(edible, poisonous);

  });

//page listeners
document.getElementById('gill-color').addEventListener("change", reset);
document.getElementById('spore-print-color').addEventListener("change", reset);
document.getElementById('population').addEventListener("change", reset);
document.getElementById('gill-size').addEventListener("change", reset);

//reset results when values change
function reset() {
    document.getElementById('charts').style.display='none';
    const prediction = document.getElementById('prediction');
    prediction.className = "alert";
    prediction.textContent = "Click the button to see your results!";
    const chartCanvas = document.getElementById('chart-canvas');
    chartCanvas.innerHTML = '<canvas id="myChart"></canvas>'
    const chartCanvas2 = document.getElementById('chart-canvas2');
    chartCanvas2.innerHTML = '<canvas id="myChart2"></canvas>'
    const chartCanvas3 = document.getElementById('chart-canvas3');
    chartCanvas3.innerHTML = '<canvas id="myChart3"></canvas>'
}