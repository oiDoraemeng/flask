
function searchOrder() {
    var orderNumber = document.getElementById('orderNumber').value;
    // 验证输入是否为空
    if (orderNumber.trim() === '') {
        alert('请输入用户名后再查询订单');
        return;
    }
    // 发送Ajax请求
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/order?number=' + orderNumber, true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            // JSON.parse()方法将从服务器返回的JSON格式的字符串转换为JavaScript对象或数组
            // JSON.stringify()是将JavaScript对象orderInfo转换为JSON格式的字符串表示形式。

            var orderData = JSON.parse(xhr.responseText);
            var orderString = JSON.stringify(orderData)
            // 将订单信息展示在页面上
            // document.getElementById('orderResult').textContent = '订单信息：' + orderString;

            // 计算订单数量
            var orderCount = orderData.length;

            // 计算不同物品类名的数量
            var itemCategoryCount = new Set(orderData.map(item => item.物品类名)).size;

            // 统计每日订单数量
            var ordersByDate = {};
            orderData.forEach(item => {
                if (ordersByDate[item.日期]) {
                    ordersByDate[item.日期]++;
                } else {
                    ordersByDate[item.日期] = 1;
                }
            });

            var ordersByDateAndItem = {};

            // 遍历订单数据，按照日期和产品名统计订单数量
            orderData.forEach(item => {
                if (!ordersByDateAndItem[item.日期]) {
                    ordersByDateAndItem[item.日期] = {};
                }
                if (!ordersByDateAndItem[item.日期][item.商品名]) {
                    ordersByDateAndItem[item.日期][item.商品名] = 1;
                } else {
                    ordersByDateAndItem[item.日期][item.商品名]++;
                }
            });

            // 计算每周的订单量
            var weeklyOrdersData = {};
            orderData.forEach(item => {
                var date = new Date(item.日期);  // 假设订单日期字段为"日期"
                var year = date.getFullYear();
                var week = getWeekNumber(date);  // 获取当前日期所在的周数
                var key = year + '-W' + week;  // 用年份和周数作为键
                if (!weeklyOrdersData[key]) {
                    weeklyOrdersData[key] = 1;
                } else {
                    weeklyOrdersData[key]++;
                }
            });

            // 获取当前日期所在的周数的函数
            function getWeekNumber(d) {
                d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
                d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
                var yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
                var weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
                return weekNo;
            }


            // 将数据转换为数组以便用于Chart.js
            var dates = Object.keys(weeklyOrdersData);
            var orderCounts = Object.values(weeklyOrdersData);


            var ctx = document.getElementById('weeklyOrdersChart').getContext('2d');
            var weeklyOrdersChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: '每周订单量',
                        data: orderCounts,
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                        lineTension: 0.1
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'week'
                            }
                        },
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: '每周订单量'
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false
                        }
                    }
                }
            });
            // // 提取日期和产品名数据
            // var dates = Object.keys(ordersByDateAndItem);
            // var itemIds = Array.from(new Set([].concat(...Object.values(ordersByDateAndItem).map(obj => Object.keys(obj)))));
            //
            // var data = {
            //     labels: dates,
            //     datasets: itemIds.map(itemId => ({
            //         label: itemId,
            //         data: dates.map(date => ordersByDateAndItem[date][itemId] || 0),
            //         backgroundColor: 'rgba(255, 99, 132, 0.2)',
            //         borderColor: 'rgba(255, 99, 132, 1)',
            //         borderWidth: 1
            //     }))
            // };
            //
            // // 创建柱状图
            // var ctx = document.getElementById('myChart').getContext('2d');
            // var myChart = new Chart(ctx, {
            //     type: 'bar',
            //     data: data,
            //     options: {
            //         scales: {
            //             y: {
            //                 beginAtZero: true
            //             }
            //         }
            //     }
            // });
            // 在页面上展示统计信息
            var statsDiv = document.getElementById('orderStats');
            statsDiv.innerHTML = '<p>订单数量：' + orderCount + '</p>' +
                '<p>不同物品类数量：' + itemCategoryCount + '</p>' +
                '<p>每日订单详情：</p>';
            for (var date in ordersByDateAndItem) {
                statsDiv.innerHTML += '<p>' + date + ': ' +
                    '订单数量-' + ordersByDate[date] +
                    '订单详情-' + JSON.stringify(ordersByDateAndItem[date]) + '</p>';
            }
        } else {
            document.getElementById('orderResult').textContent = '查询失败';
            在``
        }
    };
    xhr.send();
};

// function submitForm() {
//     var name = document.getElementById("nameInput").value;
//     var xhr = new XMLHttpRequest();
//     xhr.open("GET", "http://localhost:5000/score/" + name, true);
//     // 当请求状态改变时触发该函数
//     xhr.onreadystatechange = function () {
//         if (xhr.readyState === 4 && xhr.status === 200) {
//             var response = JSON.parse(xhr.responseText);
//             if (response.success) {
//                 alert("查找成功");
//             } else {
//                 alert("未找到该学生");
//             }
//         }
//     };
//     // 发送请求
//     xhr.send();
// }