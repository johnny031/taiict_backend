let edit = "";
$(".show-add-card").on("click", function () {
  $("form[name='add-news-form']").show();
  $(".news-data-div").hide();
})
$(document).on("click", ".edit-btn", function () {
  if (!check_data($(this).attr("id"))) {
    return false;
  }
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
  if (!check_data($(this).attr("id"))) {
    return false;
  }
  if (!confirm("確定刪除此則最新消息？")) {
    return false;
  }
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
  if (!data) {
    return false;
  }
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
function validateLoginForm() {
  let name = document.forms["login-form"]["name"].value;
  let password = document.forms["login-form"]["password"].value;
  if (name == "" || password == "") {
    alert("欄位請勿空白");
    return false;
  }
}
$(".close").on("click", function () {
  $(".alert-message").hide();
});
function tagToPlainText(code) {
  let text = code
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
  return text;
}
function plainTextToTag(text) {
  let tag = text
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">");
  return tag;
}
//change label text when image selected
$("#FileUpload").on("change", function () {
  let fileExtension = ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'doc', 'xlsx', 'pptx', 'ppt'];
  let file_size = 0;
  for (let i = 0; i < this.files.length; i++) {
    file_size += this.files[i].size
  }
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

function processData() {
  let author = $("input[name=author]").val();
  let title = $("input[name=title]").val();
  let content = $("textarea[name=content]").val();
  let fileObj = document.getElementById("FileUpload").files;
  if (author == "" || title == "" || content == "") {
    alert("欄位請勿空白");
    return false;
  } else if (author.length > 50 || title.length > 80 || content.length > 3000) {
    alert("字數過多");
    return false;
  }
  $("form[name='add-news-form']").hide();
  $(".news-data-div").show();
  let file_field = fileObj.length;
  let news_data = new FormData();
  for (let i = 0; i < fileObj.length; i++) {
    news_data.append("file", fileObj[i]);
  }
  news_data.append("author", author);
  news_data.append("title", title);
  news_data.append("edit", edit);
  $("input[name=author], input[name=title], textarea[name=content], input[type='file']").val("");
  $("#FileUpload + label").html("附件")
  let is_premium = username === "Mary";
  let content_db = is_premium
    ? content.replace(/\n/g, "<br/>")
    : tagToPlainText(content).replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;");
  news_data.append("content", content_db);
  return {
    author: author, title: title, file_field: file_field
    , news_data: news_data, content: content
  }
}
function check_data(id) {
  let idIsNum = /^\d+$/.test(id);
  if (!idIsNum) {
    alert("資料尚未就緒，請稍候");
    return false;
  } else {
    return true;
  }
}
function updateHtml(author, title, file_field, content) {
  if (edit == "") {
    $(".grid-container").append(
      `
      <div class="grid-item">` +
      tagToPlainText(author) +
      `</div>
      <div class="grid-item" id="temp_datetime">0000/00/00 00:00:00</div>
      <div class="grid-item">` +
      tagToPlainText(title) +
      `</div>
      <div class="grid-item news-content">` +
      tagToPlainText(content) +
      `</div>
      <div class="grid-item">`+ file_field + `</div>
      <div class="grid-item edit-grid">
        <button class="edit-btn" id="edit_temp_id">
          <span><i class="fas fa-pen"></i></span>
        </button>
      </div>
      <div class="grid-item btn-grid">
        <button class="delete-btn" id="temp_id">
          <span><i class="fas fa-trash"></i></span>
        </button>
      </div>
      `
    );
  } else {
    list = [file_field, content, title, "", author]
    $("#" + edit).parent(".edit-grid").prevUntil(".btn-grid").each(function (index, element) {
      if (index == 0 && file_field == 0) return;
      if (index == 3) {
        $(element).attr("id", "temp_datetime");
        return;
      }
      $(element).html(tagToPlainText(list[index]));
    });
  }
}