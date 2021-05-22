$(document).on("click", ".delete-btn", function () {
  let idIsNum = /^\d+$/.test($(this).attr("id"));
  if (!idIsNum) {
    alert("資料尚未就緒，請稍候");
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

  let file_field = fileObj.length;
  let news_data = new FormData();
  for (let i = 0; i < fileObj.length; i++) {
    news_data.append("file", fileObj[i]);
  }
  news_data.append("author", author);
  news_data.append("title", title);
  $("input[name=author], input[name=title], textarea[name=content], input[type='file']").val("");
  $("#FileUpload + label").html("附件")

  let is_premium = username === "Mary";
  let content_db = is_premium
    ? content.replace(/\n/g, "<br/>")
    : tagToPlainText(content).replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;");
  let content_js = tagToPlainText(content);
  news_data.append("content", content_db);

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
    content_js +
    `</div>
  <div class="grid-item">`+ file_field + `</div>
  <div class="grid-item btn-grid">
    <button class="delete-btn" id="temp_id">
      <span>&times;</span>
    </button>
  </div>
  `
  );
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
        $("#temp_id").attr("id", data[0]);
        $("#temp_datetime").html(data[1]);
        $("#temp_datetime").removeAttr("id");
      },
    });
  });
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