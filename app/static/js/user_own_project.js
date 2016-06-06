
function getPage(e) {
    var page_no = 1;
    if (e != undefined) {
        console.log(e);
        page_no = e.attr("href").match(/page=([0-9]+)/)[1];
        console.log(page_no);
    }
    var tbody = $('#tbody');
    var pagerUl = $('#pager-ul');
    var data = {"page_no": page_no};
    $.ajax({
        method: 'POST',
        url: '/user/userownproject',
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            var newTbodyHtml = '';
            var last_created_time = '';
            $(data.projects).each(function () {
                newTbodyHtml += '<tr>';
                newTbodyHtml += '<td data-title="编号">' + this.id + '</td>';
                newTbodyHtml += '<td data-title="项目">' + '<a href="/project/' + this._id + '"' + ' target="_blank"> ';
                newTbodyHtml += this.name;
                newTbodyHtml += '</a>';
                newTbodyHtml += '</td>';
                newTbodyHtml += '<td data-title="状态">招募中</td>';
                newTbodyHtml +=
                    '<td data-title="管理">' +
                    '<a  href="/project/edit?project_id='+this._id+ '"class="btn btn-raised btn-default" onclick="" style="margin: auto">修改</a>' +
                    '</td>';
                if(this.status == 0){
                    newTbodyHtml +=
                    '<td data-title="操作">' +
                    '<a  href="/projectstart?project_id='+this._id+ '"class="btn btn-raised btn-success" onclick="" style="margin: auto">开始项目</a>' +
                    '</td>';
                }if(this.status == 1){
                    newTbodyHtml +=
                    '<td data-title="操作">' +
                    '<button disabled="disabled" class="btn btn-primary btn-default" onclick="" style="margin: auto">项目已开始</button>' +
                    '</td>';
                }
                newTbodyHtml += '</tr>';

                last_created_time = this.created_time;
            });
            newTbodyHtml +=
                '<tr><td id="before" hidden>' + last_created_time + '</td></tr>';
            tbody.empty().append(newTbodyHtml);

            var newPagerLiHtml = '';
            var previousPageNum = page_no - 1;
            if (previousPageNum != 0) {
                newPagerLiHtml += '<li>';
                newPagerLiHtml += '<a class="withripple" href="?page=' + previousPageNum + '">' + '前一页' + '</a>';
                newPagerLiHtml += '</li>';
            }
            var page_count = data.page_count;
            for (var i = 1; i <= page_count; i++) {
                newPagerLiHtml += '<li>';
                if (i == page_no) {
                    newPagerLiHtml += '<a class="withripple" style="background-color: #ededed">' + i + '</a>';
                } else {
                    newPagerLiHtml += '<a class="withripple" href="?page=' + i + '">' + i + '</a>';
                }
                newPagerLiHtml += '</li>';
            }
            var nextPageNum = +page_no + 1;
            if (nextPageNum <= page_count) {
                newPagerLiHtml += '<li>';
                newPagerLiHtml += '<a class="withripple" href="?page=' + nextPageNum + '">' + '下一页' + '</a>';
                newPagerLiHtml += '</li>';
            }
            pagerUl.empty().append(newPagerLiHtml);

            $(function () {
                $.material.init();
            });
        }
    })
}

$(document).ready(function () {
    getPage();
});

$('#pager-ul').on('click', '.withripple', function (e) {
    e.preventDefault();
    getPage($(this));
});
