function deleteNews(newsId) {
  if (!confirm("確定刪除此則最新消息？")) {
    return false;
  }
  fetch("/json-data", {
    method: "POST",
    body: JSON.stringify({ newsId: newsId }),
  }).then((_res) => {
    window.location.href = "/news-list";
  });
}
function validateAddNewsForm() {
  let author = document.forms["add-news-form"]["author"].value;
  let title = document.forms["add-news-form"]["title"].value;
  let content = document.forms["add-news-form"]["content"].value;
  if (author == "" || title == "" || content == "") {
    alert("欄位請勿空白");
    return false;
  }
}
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
