let idSelect = d3.select("#selDataset")
let demographicsTable = d3.select("#sample-metadata")

function plotGraphs(id) {
    d3.json("./data/samples.json").then((data => {
        if (id == null) {
            data.names.forEach((name => {
                let option = idSelect.append("option");
                option.text(name);
            })); 
            let randomInit = randomElement = data.names[Math.floor(Math.random() * data.names.length)];
            plotGraphs(randomInit);
            document.getElementById('selDataset').value = randomInit
            return;
        }
        let individualSample = data.samples.filter(sample => sample.id == id)[0];
        let otuIds = individualSample['otu_ids']
        let sampleValues = individualSample['sample_values']
        let otuLabels = individualSample['otu_labels']
        sampleValues.sort(function(a, b){return b - a})
        otuIds.sort(function(a, b){return b - a})
        demographicsTable.html("");

        let metaBio = data.metadata.filter(participant => participant.id == id)[0];
        metaBio['sample_count'] = sampleValues.length
        Object.entries(metaBio).forEach((key)=>{
            demographicsTable.append("li").text(key[0] + " : " + key[1]);
        })

        let topOtuIds = otuIds.slice(0, 10)
        let labels = otuLabels.slice(0, 10)
        let topSampleValues = sampleValues.slice(0, 10)
        let formattedIDs = topOtuIds.map(otuID => "OTU " + otuID);

        let barData = {
            x: topSampleValues,
            y: formattedIDs,
            text: labels,
            type: 'bar',
            orientation: 'h',
            marker: {
                color: 'light grey'
            }
        };
        barData['x'].reverse()
        barData = [barData];
        let barLayout = {
            height: 500,
            width: 600,
            title: {
                text: `<b>Subject ${id}'s Top Ten OTUs</b>`,
                font: {
                    size: 18,
                    color: 'black'
                }
            },
            xaxis: {
                title: "<b>Sample values<b>",
                color: 'black'
            },
            yaxis: {
                tickfont: { size: 14 }
            }
        }
        Plotly.newPlot("bar", barData, barLayout);

        let bubbleData = {
            x: topOtuIds,
            y: topSampleValues,
            text: otuLabels,
            mode: 'markers',
            marker: {
                size: sampleValues,
                color: otuIds
            },
            text: otuLabels
        };
        bubbleData = [bubbleData];
        
        let bubbleLayout = {
            height: 500,
            width: 1000,
            xaxis: {
                title: "<b>OTU Id</b>",
                color: 'black'
            },
            yaxis: {
                title: "<b>Sample Values</b>",
                color: 'black'
            },
            showlegend: false,
        };
        Plotly.newPlot('bubble', bubbleData, bubbleLayout);
    }));
}; 