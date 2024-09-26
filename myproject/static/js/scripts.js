document.addEventListener('DOMContentLoaded', function() {
    // Initialize Chart.js
    var ctx = document.getElementById('stockChart').getContext('2d');
    var stockChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],  // To be filled dynamically
            datasets: [
                // Datasets will be added dynamically pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
            ]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Stock Prices Over Months'
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Month'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Price (USD)'
                    }
                }
            }
        }
    });

    // Initialize D3.js
    const d3ChartWidth = 400;
    const d3ChartHeight = 300;
    const svg = d3.select("#d3Chart")
        .append("svg")
        .attr("width", d3ChartWidth)
        .attr("height", d3ChartHeight);

    function renderD3Chart(data) {
        // Clear previous chart
        svg.selectAll("*").remove();

        // Set scales
        const xScale = d3.scaleBand()
            .domain(data.map((d, i) => i))
            .range([0, d3ChartWidth])
            .padding(0.1);

        const yScale = d3.scaleLinear()
            .domain([0, d3.max(data)])
            .range([d3ChartHeight, 0]);

        // Create bars
        svg.selectAll("rect")
            .data(data)
            .enter()
            .append("rect")
            .attr("x", (d, i) => xScale(i))
            .attr("y", d => yScale(d))
            .attr("width", xScale.bandwidth())
            .attr("height", d => d3ChartHeight - yScale(d))
            .attr("fill", "teal");

        // Add X-axis
        svg.append("g")
            .attr("transform", `translate(0, ${d3ChartHeight})`)
            .call(d3.axisBottom(xScale).tickFormat(i => `Item ${i + 1}`));

        // Add Y-axis
        svg.append("g")
            .call(d3.axisLeft(yScale));
    }

    // Fetch data from API
    function fetchData() {
        fetch('/api/nse-option-chain/')
            .then(response => response.json())
            .then(data => {
                // Update Chart.js
                stockChart.data.labels = data.labels;
                stockChart.data.datasets = data.stockPrices.map(stock => ({
                    label: stock.symbol,
                    data: stock.prices,
                    borderColor: getRandomColor(),
                    borderWidth: 2,
                    fill: false
                }));
                stockChart.update();

                // Update D3.js
                renderD3Chart(data.marketOverview);
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Utility function to generate random colors for Chart.js datasets
    function getRandomColor() {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        return `rgba(${r}, ${g}, ${b}, 1)`;
    }

    // Initial data fetch
    fetchData();

    // Optionally, fetch data periodically for live updates
    setInterval(fetchData, 60000);  // Fetch every 60 seconds
});
