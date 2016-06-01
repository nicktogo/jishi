function getPage(e) {
    if (e != undefined) {
        e.preventDefault();
    }
    var tbody = $('#tbody');
    var before = $('#before').val();
    var data = {"before": before};
    if (before == undefined) {
        data = {"before": "0"};
    } else {
        data = {"before": before};
    }
    $.ajax({
        method: 'POST',
        url: '/user/userownproject',
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            var newTbodyHtml = '';
            var last_created_time = '';
            $(data).each(function () {
                newTbodyHtml += '<tr>';
                newTbodyHtml += '<td data-title="编号">' + this.id + '</td>';
                newTbodyHtml += '<td data-title="项目">' + '<a href="/project/' + this._id + '"' + ' target="_blank"> ';
                newTbodyHtml += this.name;
                newTbodyHtml += '</a>';
                newTbodyHtml += '</td>';
                newTbodyHtml += '<td data-title="状态">招募中</td>';
                newTbodyHtml +=
                    '<td data-title="操作">' +
                    '<button type="button" class="btn btn-raised btn-default" style="margin: auto">修改</button>' +
                    '</td>';
                newTbodyHtml += '</tr>';
                last_created_time = this.created_time;
            });
            newTbodyHtml +=
                '<tr><td id="before" hidden>' + last_created_time + '</td></tr>';
            tbody.html(newTbodyHtml);
            // TODO generate pagination...
        }
    })
}

$(document).ready(function () {
    getPage();
});

