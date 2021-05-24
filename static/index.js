let edit = "";
$(".show-add-card").on("click", function () {
  $("form[name='add-news-form']").show();
  $(".news-data-div").hide();
})
$(document).on("click", ".edit-btn", function () {
  if (!check_data($(this).attr("id"))) return false;
  edit = $(this).attr("id");
  let data = [];
  $(this).parent(".edit-grid").prevUntil(".btn-grid").each(function () {
    data.push(plainTextToTag($(this).html()));
  });
  $("form[name='add-news-form']").show();
  $(".news-data-div").hide();
  $(".add-news-title").html("編輯最新消息")
  $("input[name=author]").val(data[4]);
  $("input[name=title]").val(data[2]);
  $("textarea[name=content]").val(data[1]);
  $("#FileUpload + label").html("重新上傳");
  $(".add-news-btn").html("更新");
})
$(document).on("click", ".delete-btn", function () {
  if (!check_data($(this).attr("id"))) return false;
  if (!confirm("確定刪除此則最新消息？")) return false;
  fetch("/json-data", {
    method: "POST",
    body: JSON.stringify({ newsId: $(this).attr("id") }),
  }).then((_res) => {
    // window.location.href = "/news-list";
  });
  $(this).parent(".btn-grid").prevUntil(".btn-grid").remove();
  $(this).parent(".btn-grid").remove();
});
$(".add-news-btn").on("click", function () {
  let data = processData();
  if (!data) return false;
  const { author, title, file_field, news_data, content } = data;
  updateHtml(author, title, file_field, content);
  $.ajax({
    type: "POST",
    url: "/add-news",
    data: news_data,
    dataType: "json",
    contentType: false,
    cache: false,
    processData: false,
  }).then((_res) => {
    $.ajax({
      method: "GET",
      url: "/add-news",
      success: function (data) {
        if (edit == "") {
          $("#temp_id").attr("id", data[0]);
          $("#edit_temp_id").attr("id", data[0]);
        }
        $("#temp_datetime").html(data[1]);
        $("#temp_datetime").removeAttr("id");
      },
    });
  });
  edit = "";
  $(".add-news-title").html("新增最新消息")
  $("#FileUpload + label").html("附件");
  $(".add-news-btn").html("新增")
});
$("#FileUpload").on("change", function () {
  let fileExtension = ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'doc', 'xlsx', 'pptx', 'ppt'];
  let file_size = 0;
  for (let i = 0; i < this.files.length; i++) file_size += this.files[i].size;
  if (file_size > 500 * 1024) { // 500KB
    alert("附件已超出容量限制500KB")
    $(this).val("");
    $(this).next().text("附件");
  } else if ($.inArray($(this).val().split('.').pop().toLowerCase(), fileExtension) == -1) {
    alert("不支援的檔案格式，只支援：" + fileExtension.join(', '));
    $(this).val("");
    $(this).next().text("附件");
  }
  if ($(this).val() != "") {
    $(this).next().text(this.files.length + "個檔案");
  }
});
$(".close").on("click", function () {
  $(".alert-message").hide();
});