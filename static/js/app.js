let zomatoData = {};
let deliveryChart, cuisineChart, costChart;

// Load JSON data
fetch('../static/data/zomato_data.json')
    .then(response => response.json())
    .then(data => {
        zomatoData = data;
        populateCuisineFilter();
        initCharts();
    })
    .catch(error => console.error('Error loading JSON:', error));

// Populate cuisine filter dropdown
function populateCuisineFilter() {
    const cuisineFilter = document.getElementById('cuisineFilter');
    const cuisines = [...new Set(zomatoData.raw.map(item => item['listed_in(type)']))].sort();
    cuisines.forEach(cuisine => {
        const option = document.createElement('option');
        option.value = cuisine;
        option.textContent = cuisine;
        cuisineFilter.appendChild(option);
    });
}

// Initialize charts
function initCharts() {
    // Delivery Chart (Bar)
    const deliveryCtx = document.getElementById('deliveryChart').getContext('2d');
    deliveryChart = new Chart(deliveryCtx, {
        type: 'bar',
        data: {
            labels: zomatoData.delivery.labels,
            datasets: [{
                label: 'Percentage of Restaurants',
                data: zomatoData.delivery.values,
                backgroundColor: ['#36a2eb', '#ff6384'],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, title: { display: true, text: 'Percentage (%)' } }
            },
            plugins: { legend: { display: false } }
        }
    });

    // Cuisine Chart (Bar)
    const cuisineCtx = document.getElementById('cuisineChart').getContext('2d');
    cuisineChart = new Chart(cuisineCtx, {
        type: 'bar',
        data: {
            labels: zomatoData.cuisine.labels,
            datasets: [{
                label: 'Number of Restaurants',
                data: zomatoData.cuisine.values,
                backgroundColor: '#36a2eb',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            scales: {
                x: { title: { display: true, text: 'Count' } }
            }
        }
    });

    // Cost Chart (Histogram)
    const costCtx = document.getElementById('costChart').getContext('2d');
    costChart = new Chart(costCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Frequency',
                data: [],
                backgroundColor: '#ff6384',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Cost for Two (INR)' } },
                y: { title: { display: true, text: 'Frequency' } }
            }
        }
    });
    updateCharts(); // Initial update with all data
}

// Filter data based on user inputs
function filterData() {
    const cuisineFilter = document.getElementById('cuisineFilter').value;
    const deliveryFilter = document.getElementById('deliveryFilter').value;
    const costMin = parseFloat(document.getElementById('costMin').value) || 0;
    const costMax = parseFloat(document.getElementById('costMax').value) || Infinity;

    return zomatoData.raw.filter(item => {
        const cuisineMatch = cuisineFilter === 'all' || item['listed_in(type)'] === cuisineFilter;
        const deliveryMatch = deliveryFilter === 'all' || item['online_order'] === deliveryFilter;
        const cost = item['approx_cost(for two people)'];
        const costMatch = cost >= costMin && cost <= costMax;
        return cuisineMatch && deliveryMatch && costMatch;
    });
}

// Update all charts based on filtered data
function updateCharts() {
    const filteredData = filterData();

    // Update Delivery Chart
    const deliveryCounts = {};
    filteredData.forEach(item => {
        const key = item['online_order'];
        deliveryCounts[key] = (deliveryCounts[key] || 0) + 1;
    });
    const total = filteredData.length;
    const deliveryLabels = Object.keys(deliveryCounts);
    const deliveryValues = deliveryLabels.map(key => (deliveryCounts[key] / total * 100).toFixed(2));
    deliveryChart.data.labels = deliveryLabels;
    deliveryChart.data.datasets[0].data = deliveryValues;
    deliveryChart.update();

    // Update Cuisine Chart
    const cuisineCounts = {};
    filteredData.forEach(item => {
        const key = item['listed_in(type)'];
        cuisineCounts[key] = (cuisineCounts[key] || 0) + 1;
    });
    const cuisineLabels = Object.keys(cuisineCounts).sort();
    const cuisineValues = cuisineLabels.map(key => cuisineCounts[key]);
    cuisineChart.data.labels = cuisineLabels;
    cuisineChart.data.datasets[0].data = cuisineValues;
    cuisineChart.update();

    // Update Cost Chart
    const costData = filteredData.map(item => item['approx_cost(for two people)']);
    const min = costData.length ? Math.min(...costData) : 0;
    const max = costData.length ? Math.max(...costData) : 1000;
    const binCount = 20;
    const binWidth = max > min ? (max - min) / binCount : 1;
    const bins = Array(binCount).fill(0);
    const labels = Array(binCount).fill(0).map((_, i) => 
        Math.round(min + i * binWidth) + '-' + Math.round(min + (i + 1) * binWidth)
    );
    costData.forEach(cost => {
        if (cost >= min && cost <= max) {
            const binIndex = Math.min(Math.floor((cost - min) / binWidth), binCount - 1);
            bins[binIndex]++;
        }
    });
    costChart.data.labels = labels;
    costChart.data.datasets[0].data = bins;
    costChart.update();
}