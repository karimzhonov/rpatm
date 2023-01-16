<template>
    <VueApexCharts type="bar" :options="chartOptions" :series="series"/>
</template>
<script>
import VueApexCharts from "vue3-apexcharts";

export default {
    name: 'Bar',
    props: ['series', 'labels'],
    components: {VueApexCharts},
    data() {
        const all_colors = ["#EE391F", "#EE391F", "#EE391F", "#EE391F", "#EE391F", "#FAA10B", "#FAB807", "#F1E000", "#A4D12A", "#27B973"]
        const colors = []
        const xaxis_colors = []
        for (let dataset of this.series) {
            for (let v of dataset.data) {
                v = Math.round(v * 10)
                colors.push(all_colors[v - 1])
                xaxis_colors.push('var(--surface-900)')
            }
        }

        return {
            chartOptions: {
                chart: {
                    toolbar: {
                        show: false
                    },
                    height: 150,
                    type: 'bar',
                },
                colors: colors,
                plotOptions: {
                    bar: {
                        columnWidth: '65%',
                        distributed: true,
                        borderRadius: 10,
                        dataLabels: {
                            position: 'top', // top, center, bottom
                        },
                    }
                },
                dataLabels: {
                    enabled: true,
                    offsetY: -20,
                    formatter: function (val, opts) {
                        val = `${val}000000`
                        return val.slice(0, 5);
                    },
                    style: {
                        fontSize: '14px',
                        fontFamily: 'Helvetica, Arial, sans-serif',
                        fontWeight: 'bold',
                        colors: ["var(--surface-900)"]
                    },
                },
                legend: {
                    show: false
                },
            xaxis: {
                categories: this.labels,
                labels: {
                    style: {
                        fontSize: '14px',
                        fontFamily: 'Helvetica, Arial, sans-serif',
                        fontWeight: 'bold',
                        colors: xaxis_colors,
                    }
                }
            },
            yaxis: {
              axisBorder: {
                show: true
              },
              axisTicks: {
                show: true,
              },
              labels: {
                show: true,
                style: {
                        fontSize: '14px',
                        fontFamily: 'Helvetica, Arial, sans-serif',
                        fontWeight: 'bold',
                        colors: ["var(--surface-900)"]
                    },
              },
              max: 1,
            },
          },
        }
    }

}
</script>