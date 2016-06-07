/**
 * Created by Nick on 2016/6/2.
 */
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
        url: '/message/page',
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            var newTbodyHtml = '';
            $(data.messages).each(function () {
                alert(this.project_id)
                alert(this.user.name);
                newTbodyHtml += '<tr>';
                newTbodyHtml += '<td data-title="项目名称">' + '<a href="/project/' + this.project_id + '"' + ' target="_blank"> ';
                newTbodyHtml += this.projectname;
                newTbodyHtml += '</a>';
                newTbodyHtml += '</td>';
                newTbodyHtml += '<td data-title="消息发出者">' + this.user.name + '</td>';
                newTbodyHtml += '<td data-title="所有人">' + this.puser.name + '</td>';
                newTbodyHtml += '<td data-title="消息类型" class="mes_type">' + this.message_type + '</td>';
                newTbodyHtml += '<td data-title="创建时间">' + this.created_time + '</td>'
                switch(this.message_type)
                {
                case 0:
                        if(this.isSolved == 0&&this.project_owner==this.user_name)
                        {
                        newTbodyHtml +=
                            '<td data-title="操作">' +
                            '<button id="apply_btn" type="button" class="btn btn-raised btn-danger" onclick="permit(this)" style="margin: auto">通过</button>' +
                            '</td>';
                        }
                        else{
                        newTbodyHtml +=
                            '<td data-title="操作">' +
                            '<button id="apply_btn" type="button" class="btn btn-raised btn-danger" onclick="permit(this)" disabled="disabled" style="margin: auto">通过</button>' +
                            '</td>';
                        }
                        break;
                case 1:
                        newTbodyHtml +=
                            '<td data-title="操作">' +
                            '<button type="button" class="btn btn-raised btn-danger" onclick="permit(this)" disabled="disabled" style="margin: auto">已同意</button>' +
                            '</td>';
                        break;
                case 2:
                        newTbodyHtml +=
                            '<td data-title="操作">' +
                            '<button type="button" class="btn btn-raised btn-danger" onclick="permit(this)" disabled="disabled" style="margin: auto">已踢出</button>' +
                            '</td>';
                        break;
                case 3:
                        newTbodyHtml +=
                            '<td data-title="操作">' +
                            '<button type="button" class="btn btn-raised btn-danger" onclick="permit(this)" disabled="disabled" style="margin: auto">已退出</button>' +
                            '</td>';
                        break;
                }
                newTbodyHtml += '<input class="message_id" type="hidden" value="' + this._id +'">';
                newTbodyHtml += '</tr>';
            });
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

                var types = ["申请", "同意", "退出", "被踢出"];
                $('.mes_type').each(function (elem) {
                    console.log($(this).text());
                    $(this).text(types[parseInt($(this).text())]);
                });
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

function permit(btn) {
    var message_id = $(btn).parent().next('.message_id').val();
    var data = {'message_id': message_id}
    $.ajax({
        url: "/project/permit",
        data: JSON.stringify(data),
        contentType: 'application/json',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            $(btn).attr({"disabled": "disabled"});
        },
        error: function (data) {
            console.log(data)
        }
    })

}

function search(btn) {
    var input = $("#search_message").val()
    alert(input)
    var data = {'input': input}
    $.ajax({
        url: "/message/search",
        data: JSON.stringify(data),
        contentType: 'application/json',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            alert(data['input'] + "创建成功!")
        },
        error: function (data) {
            console.log(data)
        }
    })

}
