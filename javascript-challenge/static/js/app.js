let tableData = data
let tbody = d3.select("tbody")

let form = d3.select("form")
form.on("submit", onSubmit)

function onSubmit() {
  d3.event.preventDefault()
  let inputValue = d3.select("#datetime").property("value")
  let filteredData = tableData.filter(datetime => datetime.datetime === inputValue)
  let tbody = d3.select("tbody")
  tbody.html("")
  filteredData.forEach(function(sighting) {
    let row = tbody.append("tr")
    Object.entries(sighting).forEach(function([key, value]) {
      let cell = row.append("td")
      cell.text(value)
    })
    d3.event.preventDefault()
  })
}

function init() {
  tableData.forEach(function(sighting) {
    let row = tbody.append("tr")
    Object.entries(sighting).forEach(function([key, value]) {
      let cell = row.append("td")
      cell.text(value)
    })
  })
}

