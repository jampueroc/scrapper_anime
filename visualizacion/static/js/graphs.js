var chart = c3.generate({
    bindto: '#generos',
    size: {
        height: 1000
    },
    data: {
        url: url_json_percent,
        mimeType: 'json',
        type: 'bar',
        labels: {
            format: function (v, id, i, j) {
                return Math.round(v * 1000) / 10 + "%";
            },
            tick: {
                rotate: 75,
                multiline: false
            }
        }
    },
    bar: {
        width: {
            ratio: 1 // this makes bar width 50% of length between ticks
        }
    },


    axis: {
        y: {
            label: {
                text: '% del total',
                position: 'outer-middle'
            },
            tick: {
                format: d3.format(",%") // ADD
            }
        },
        x: {
            type: 'category',
            categories: ['Géneros de Anime'],
            height: 130
        }
    },
    legend: {
        position: 'right'
    },
    tooltip: {
        show: false
    }
});

var chart = c3.generate({
    bindto: '#nulls',
    size: {
        height: 1000
    },
    data: {
        url: url_json_null,
        mimeType: 'json',
        type: 'bar',
        labels: {
            tick: {
                rotate: 75,
                multiline: false
            }
        }
    },
    bar: {
        width: {
            ratio: 1 // this makes bar width 50% of length between ticks
        }
    },


    axis: {
        y: {
            label: {
                text: 'Total por atributos',
                position: 'outer-middle'
            }
        },
        x: {
            type: 'category',
            categories: ['Atributos del modelo  de Anime'],
            height: 130
        }
    },
    legend: {
        position: 'right'
    },
    tooltip: {
        show: false
    }
});
