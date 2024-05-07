
var layer;
layui.use('layer', function () {
    layer = layui.layer;
});

function main() {
    if (typeof (layer) != "object" || !layer) {
        setTimeout("main()", 400);
        return;
    }
    var myCalendar = new SimpleCalendar('#overhaul_calendar', {
        width: '100%',
        height: '500px',
        language: 'CH', //语言
        showLunarCalendar: false, //阴历
        showHoliday: false, //休假-暂时禁用
        showFestival: true, //节日
        showLunarFestival: true, //农历节日
        showSolarTerm: true, //节气
        showMark: true, //标记
        realTime: true, //具体时间
        timeRange: {
            startYear: 2020,
            endYear: 2021
        },
        mark: {},
        markColor: ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],//记事各个颜色
        main: function (year, month) {
            // alert("[获取数据]" + year + "--->" + month);
            var index = -1;
            if (layer) index = layer.msg('正在查询数据......', {icon: 16, shade: 0.6});
            //@-这里获取数据：
            console.log(year + "--->" + month);

            //模拟获取数据start
            var resultObj = {}, status = ['TMS', 'OMS', 'PMS', '风控平台'];
            var sys_name = ['TMS发布任务数：', 'OMS发布任务数：', 'PMS发布任务数：', '风控平台发布任务数：']
            var assss = [[3,3,2,3,1,1,2,1,1,2,3,3,2,2,4,5,6,3,2,4,2,4,1,1,2,3,4,2],
                [10,12,22,25,15,20,15,15,20,15,15,20,15,15,20,15,15,20,15,15,20,15,15,20,15,15,20,15],
                [11,15,20,15,15,20,15,15,20,15,15,20,15,15,20,15,15,20,15,15,20,15,15,20,15,15,20,15],
                [40,68,44,72,50,12,22,25,15,20,15,15,20,15,15,20,15,15,20,15,15,40,68,44,72,40,68,44]];
            for (var i = 1; i <= 5; i++) {
                var array = [];
                var date = year + "-" + month + "-" + (i < 10 ? '0' + i : i);
                console.log(date);
                for (var num = 0; num <= i % 4; num++)
                    array.push({
                        title: '数据来源',
                        name: sys_name[num],
                        ratio: assss[num][i],
                        status: num,
                        statusText: status[num]
                    });
                resultObj[date] = i == 27 ? [] : array;
            }
             console.log(resultObj);
            if (layer) layer.close(index);
            return resultObj;
        },
        timeupdate: false,//显示当前的时间HH:mm
        theme: {
            changeAble: false,
            weeks: {
                backgroundColor: '#FBEC9C',
                fontColor: '#4A4A4A',
                fontSize: '20px',
            },
            days: {
                backgroundColor: '#ffffff',
                fontColor: '#565555',
                fontSize: '24px'
            },
            todaycolor: 'orange',
            activeSelectColor: 'orange',
        }
    });
}
main();
