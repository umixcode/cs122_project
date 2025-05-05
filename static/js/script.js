// crypto analysis ui logic
document.addEventListener('DOMContentLoaded', () => {
    // wait for the page to load
    const cryptoSelect = document.getElementById('crypto-select-home');
    const viewButton = document.getElementById('view-button');
    const chartContainer = document.getElementById('chart-container');
    const analysisResultsContainer = document.getElementById('analysis-results'); // get the new div
    let priceChart = null; // store the chart object here

    viewButton.addEventListener('click', () => {
        const selectedCoinId = cryptoSelect.value;

        // make sure a coin is chosen
        if (selectedCoinId === '--select--') {
            alert('please select a cryptocurrency.'); // lowercase alert
            if (priceChart) {
                priceChart.destroy();
                priceChart = null;
            }
            chartContainer.innerHTML = '<p>select a coin to view its trend.</p>';
            analysisResultsContainer.innerHTML = ''; // clear analysis results too
            return; // don't proceed without a coin
        }

        // log selected coin
        console.log(`fetching data for: ${selectedCoinId}`);
        chartContainer.innerHTML = `<p>loading chart for ${selectedCoinId}...</p>`; // show loading text
        analysisResultsContainer.innerHTML = ''; // clear previous analysis results

        // fetch data from our flask api
        fetch(`/api/chart_data/${selectedCoinId}`)
            .then(response => {
                if (!response.ok) {
                    // check if the request failed
                    throw new Error(`http error! status: ${response.status}`);
                }
                return response.json(); // get the json data from the response
            })
            .then(data => {
                // log received data
                console.log('data received:', data);
                if (data.error) {
                    // show error from the api
                    chartContainer.innerHTML = `<p>error: ${data.error}</p>`;
                    analysisResultsContainer.innerHTML = ''; // clear analysis on error
                    return;
                }
                // draw the chart and show analysis
                renderChartAndAnalysis(data);

            })
            .catch(error => {
                // handle network or fetch errors
                console.error('error fetching chart data:', error);
                chartContainer.innerHTML = `<p>error loading chart data. please check the console or try again.</p>`;
                analysisResultsContainer.innerHTML = ''; // clear analysis on error
                // remove chart if fetching failed
                if (priceChart) {
                    priceChart.destroy();
                    priceChart = null;
                }
            });
    });

    // display initial message
    chartContainer.innerHTML = '<p>select a coin and click "show trend" to view its price chart.</p>';


    // creates/updates the price chart and adds analysis
    function renderChartAndAnalysis(data) {
        // log data for chart
        console.log('rendering chart/analysis with data:', data);

        // --- data validation ---
        // expects data like { timestamps: [...], prices: [...] }
        if (!data || !data.timestamps || !data.prices || data.prices.length === 0) {
             console.error("invalid or empty data received from api:", data);
             chartContainer.innerHTML = '<p>could not load chart: invalid or empty data received.</p>';
             analysisResultsContainer.innerHTML = ''; // clear analysis
             // remove old chart if validation fails
             if (priceChart) {
                priceChart.destroy();
                priceChart = null;
             }
             return;
        }

        // --- render chart ---
        // remove the old chart first
        if (priceChart) {
            priceChart.destroy();
        }
        // add the canvas element for the chart
        chartContainer.innerHTML = '<canvas id="pricechartcanvas"></canvas>'; // lowercase id
        const ctx = document.getElementById('pricechartcanvas').getContext('2d');

        // prepare data for chart.js
        const labels = data.timestamps.map(ts => {
             // format timestamps as dates
             const date = new Date(ts * 1000);
             // use tolocaledatestring for locale-aware formatting (e.g., mm/dd/yy or dd/mm/yy)
             return date.toLocaleDateString(undefined, { year: '2-digit', month: 'numeric', day: 'numeric' });
        });
        const prices = data.prices;
        const coinName = cryptoSelect.options[cryptoSelect.selectedIndex].text; // get selected coin name

        // create the line chart
        // using global 'Chart' object from chart.js library
        priceChart = new Chart(ctx, {
            type: 'line', // line chart for price trend
            data: {
                labels: labels, // dates for x-axis
                datasets: [{
                    label: `${coinName} price (usd)`, // label for the dataset (coin name)
                    data: prices, // prices for y-axis
                    borderColor: 'rgb(75, 192, 192)', // set line color
                    tension: 0.1 // slight curve for the line
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: false // allow y-axis to adjust based on data range
                    }
                },
                responsive: true, // let chart resize with window
                maintainAspectRatio: true // keep the chart's shape
            }
        });

        // --- calculate and display analysis ---
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);
        const sumPrices = prices.reduce((sum, price) => sum + price, 0);
        const avgPrice = sumPrices / prices.length;

        // format prices to 2 decimal places (or more for smaller values if needed)
        // const formatCurrency = (value) => value.toLocaleString('en-us', { style: 'currency', currency: 'usd' });
        // using simpler formatting to avoid potential locale issues
         const formatCurrency = (value) => `$${value.toFixed(2)}`;


        analysisResultsContainer.innerHTML = `
            <h3>analysis for ${coinName} (last ${prices.length} data points)</h3>
            <p>minimum price: ${formatCurrency(minPrice)}</p>
            <p>maximum price: ${formatCurrency(maxPrice)}</p>
            <p>average price: ${formatCurrency(avgPrice)}</p>
        `;
    }
}); 