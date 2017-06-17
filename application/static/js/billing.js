/**
 * Created by mengy on 2017/5/15.
 */
$(document).ready(function () {
    var billChart = echarts.init(document.getElementById('billChart'));
    function getBillChartData() {
        var x_data = [], y_data = [];
        $.ajax({
            method: 'GET',
            url: '/api/invoices',
            data: {
                'isRecurrent': $('#isRecurrentSelect').val(),
                'linkedAccountId': $('#linkedAccountIdSelect').val(),
                'billingDate': $('#billDateSelect').val()
            },
            async: false,
            success: function (data) {
                if(data){
                    for(var i in data){
                        x_data.push(data[i]['productCode']);
                        y_data.push(data[i]['totalCost']);
                    }
                }
            },
            beforeSend: function () {
                billChart.showLoading();
            },
            complete: function () {
                billChart.hideLoading();
            }
        });
        return [x_data, y_data]
    }
    function showBillChart() {
        var billChartData = getBillChartData();
        var option = {
            title: {
                text: ''
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'line'
                }
            },
            legend: {
                data: ['金额（元）']
            },
            toolbox: {
                show: true,
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    dataView: {readOnly: true},
                    magicType: {type: ['bar', 'line']},
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                name: 'productCode',
                type: 'category',
                boundaryGap: true,
                data: billChartData[0]
            },
            yAxis: {
                name: 'totalCost',
                type: 'value',
                axisLabel: {
                    formatter: '{value} ￥'
                },
                data: []
            },
            series: [{
                name: '金额（元）',
                type: 'bar',
                data: billChartData[1],
                markLine: {
                    data: [
                        {type: 'average', name: '平均花费'}
                    ]
                }
            }],
            color: [
                '#d48265', '#91c7ae', '#749f83',
                '#ca8622', '#bda29a', '#6e7074',
                '#546570', '#c4ccd3', '#c23531',
                '#2f4554', '#61a0a8'
            ]
        };
        billChart.setOption(option);
    }

    showBillChart();
    $('.select').on('change', function () {
        showBillChart();
    });
});
