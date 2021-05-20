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
  let is_premium = username === "Mary";
  let author = $("input[name=author]").val();
  let title = $("input[name=title]").val();
  let content = $("textarea[name=content]").val();
  let content_db = is_premium
    ? content.replace(/\n/g, "<br/>")
    : tagToPlainText(content).replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;");
  let content_js = tagToPlainText(content);
  if (author == "" || title == "" || content == "") {
    alert("欄位請勿空白");
    return false;
  }
  $("input[name=author], input[name=title], textarea[name=content]").val("");
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
  <div class="grid-item btn-grid">
    <button class="delete-btn" id="temp_id">
      <span>&times;</span>
    </button>
  </div>
  `
  );
  fetch("/add-news", {
    method: "POST",
    body: JSON.stringify({
      author: author,
      title: title,
      content: content_db,
    }),
  }).then((_res) => {
    $.ajax({
      method: "GET",
      url: "/add-news",
      success: function (data) {
        $("#temp_id").attr("id", data[0][0]);
        $("#temp_datetime").html(data[0][1]);
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
