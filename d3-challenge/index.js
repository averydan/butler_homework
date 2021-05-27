let svgWidth = 960
let svgHeight = 600

let margin = {
  top: 20,
  right: 50,
  bottom: 100,
  left: 50
}

let width = svgWidth - margin.left - margin.right
let height = svgHeight - margin.top - margin.bottom

let svg = d3.select("#plot")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight)

let runningChart = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`)

d3.csv("./assets/data/data.csv").then(function(csvData) {

    csvData.forEach(function(data) {
      data.poverty = +data.poverty
      data.obesity = +data.obesity
    })

    let xLinearScale = d3.scaleLinear()
      .domain([20, 36])
      .range([0, width])

    let yLinearScale = d3.scaleLinear()
      .domain([8, 22])
      .range([height, 0])

    let xAxis = d3.axisBottom(xLinearScale)
    let yAxis = d3.axisLeft(yLinearScale)

    runningChart.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(xAxis)

    runningChart.append("g")
      .call(yAxis)

    let plotPoints = runningChart.selectAll("circle")
    .data(csvData)
    .enter()
    .append("circle")
    .attr("cx", d => xLinearScale(d.obesity))
    .attr("cy", d => yLinearScale(d.poverty))
    .attr("r", "15")
    .attr("fill", "blue")

    let plotPointText = runningChart.selectAll(".label")
    .data(csvData)
    .enter()
    .append("text")
    .text(function(d) {return (d.abbr)})
    .attr("x", d => xLinearScale(d.obesity)-11)
    .attr("y", d => yLinearScale(d.poverty)+5)
    .style('fill','white')

    let toolTip = d3.tip()
      .attr("class", "tooltip")
      .offset([80, -60])
      .html(function(d) {
        return (`State: ${d.abbr}<br>% Obese: ${d.obesity}<br>% Impoverished: ${d.poverty}`)
      })

    runningChart.call(toolTip)
    plotPointText.on("mouseover", function(data) {
      toolTip.show(data, this)
    })
      .on("mouseout", function(data) {
        toolTip.hide(data)
      })

    runningChart.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x", 0 - (height*.75))
      .attr("dy", "1em")
      .attr("class", "axisText")
      .text("Percentage of Impoverished Population")

    runningChart.append("text")
      .attr("transform", `translate(${width / 2}, ${height + margin.top + 30})`)
      .attr("class", "axisText")
      .text("Percentage of Obese Population")
  })