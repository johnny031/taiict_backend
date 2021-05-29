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
  $(".add-news-btn").html("更新");
  if (data[0] === "0") return false;
  $.ajax({
    method: "POST",
    url: "/delete-file",
    data: { "edit": edit },
    tryCount: 0,
    beforeSend: function () {
      $('.loader').show();
      $('.add-news-btn, .cancel-btn').prop('disabled', true);
    },
    success: function (data) {
      for (let i = 0; i < data.length; i++) {
        $(".file-list").append(`
          <li>
            <a href="download/`+ data[i][0] + `" target="_blank" download="` + data[i][1] + `">` + data[i][1] + `</a>
            <button class="delete-file" data-id="`+ data[i][0] + `"><i class="fas fa-times"></i></button>
          </li>
        `);
      }
    },
    error: function () {
      this.tryCount++;
      if (this.tryCount <= 3) {
        $.ajax(this);
        return;
      }
      return;
    },
    complete: function () {
      $('.loader').hide();
      $('.add-news-btn, .cancel-btn').prop('disabled', false);
    },
  });
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
  let ready = true;
  $(".delete-file").each(function () {
    if ($(this).data("id") === undefined) {
      alert("資料尚未就緒，請稍候");
      ready = false;
      return false;
    }
  })
  if (!ready) return false;
  let data = processData();
  if (!data) return false;
  const { author, title, file_field, news_data, content } = data;
  updateHtml(author, title, file_field, content);
  $.ajax({
    type: "POST",
    url: "/add-news",
    data: news_data,
    tryCount: 0,
    dataType: "json",
    contentType: false,
    cache: false,
    processData: false,
    beforeSend: function () {
      $('.overlay').show();
    },
    success: function (data) {
      if (edit == "") {
        $("#temp_id").attr("id", data[0]);
        $("#edit_temp_id").attr("id", data[0]);
      }
      $("#temp_datetime").html(data[1]);
      $("#temp_datetime").removeAttr("id");
    },
    error: function () {
      this.tryCount++;
      if (this.tryCount <= 3) {
        $.ajax(this);
        return;
      }
      return;
    },
    complete: function () {
      $('.overlay').hide();
    },
  });
  edit = "";
  $(".add-news-title").html("新增最新消息")
  $(".add-news-btn").html("新增")
  $(".file-list").empty();
});
$("#FileUpload").on("change", function () {
  let fileExtension = ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt'];
  for (let i = 0; i < this.files.length; i++) {
    if (this.files[i].size > 500 * 1024) {
      alert("附件已超出單一檔案容量限制500KB")
      $(this).val("");
      return false;
    } else if ($.inArray(this.files[i].name.split('.').pop().toLowerCase(), fileExtension) == -1) {
      alert("不支援的檔案格式，只支援：" + fileExtension.join(', '));
      $(this).val("");
      return false;
    } else if (this.files[i].name.length > 50) {
      alert("檔案名稱過長，上限為50字");
      $(this).val("");
      return false;
    }
  }
  let news_data = new FormData();
  for (let i = 0; i < this.files.length; i++) {
    news_data.append("file", this.files[i]);
    $(".file-list").append(`
    <li>
      <a target="_blank" download="`+ this.files[i].name + `">` + this.files[i].name + `</a>
      <button class="delete-file temp_class"><i class="fas fa-times"></i></button>
    </li>`)
  }
  $.ajax({
    type: "POST",
    url: "/upload",
    data: news_data,
    tryCount: 0,
    dataType: "json",
    contentType: false,
    cache: false,
    processData: false,
    beforeSend: function () {
      $('.loader').show();
    },
    success: function (data) {
      $(".temp_class").each(function (index) {
        $(this).data("id", data[index]);
        $(this).parent("li").children("a").attr("href", "download/" + data[index]);
        $(this).removeClass("temp_class");
      })
    },
    error: function () {
      this.tryCount++;
      if (this.tryCount <= 3) {
        $.ajax(this);
        return;
      }
      return;
    },
    complete: function () {
      $('.loader').hide();
    },
  })
});
$(document).on("click", ".delete-file", function () {
  if ($(this).data("id") === undefined) {
    alert("資料尚未就緒，請稍候");
    return false;
  }
  let filename = $(this).parent("li").children("a").html();
  if (!confirm("確定刪除 " + filename + " 嗎？")) return false;
  let file_id = $(this).data("id");
  $.ajax({
    method: "POST",
    url: "/delete-file",
    data: { "file_id": file_id },
  });
  $(this).parent("li").remove();
})
$(".cancel-btn").on("click", function () {
  $("form[name='add-news-form']").hide();
  $(".news-data-div").show();
  $("input[name='author'], input[name='title'], textarea[name='content'], input[type='file']").val("");
  $(".file-list").empty();
})
$(".close").on("click", function () {
  $(".alert-message").hide();
});