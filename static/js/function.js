function validateLoginForm() {
    let name = document.forms["login-form"]["name"].value;
    let password = document.forms["login-form"]["password"].value;
    if (name == "" || password == "") {
        alert("欄位請勿空白");
        return false;
    }
}
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
function processData() {
    let author = $("input[name=author]").val();
    let title = $("input[name=title]").val();
    let content = $("textarea[name=content]").val();
    if (author == "" || title == "" || content == "") {
        alert("欄位請勿空白");
        return false;
    } else if (author.length > 50 || title.length > 80 || content.length > 3000) {
        alert("字數過多，字數限制為：類別50字，標題80字，內容3000字");
        return false;
    }
    $("form[name='add-news-form']").hide();
    $(".news-data-div").show();
    let file_field = $(".delete-file").length;
    let news_data = new FormData();
    $(".delete-file").each(function () {
        news_data.append("file_id", $(this).data("id"));
    });
    news_data.append("author", author);
    news_data.append("title", title);
    news_data.append("edit", edit);
    $("input[name=author], input[name=title], textarea[name=content], input[type='file']").val("");
    $("#FileUpload + label").html("附件");
    let content_db = is_premium
        ? content.replace(/\n/g, "<br/>")
        : tagToPlainText(content).replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;");
    news_data.append("content", content_db);
    return {
        author: author,
        title: title,
        file_field: file_field,
        news_data: news_data,
        content: content,
    };
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
        <div class="grid-item" id="temp_datetime">
            <div class="loadingio-spinner-ellipsis-w2l1qr6gk3n">
                <div class="ldio-80g99pgzdvx">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                </div>
            </div>
        </div>
        <div class="grid-item">` +
            tagToPlainText(title) +
            `</div>
        <div class="grid-item news-content">` +
            tagToPlainText(content) +
            `</div>
        <div class="grid-item">` +
            file_field +
            `</div>
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
        list = [file_field.toString(), content, title, "", author];
        $("#" + edit).parent(".edit-grid").prevUntil(".btn-grid").each(function (index, element) {
            if (index == 3) {
                $(element).attr("id", "temp_datetime");
                $(element).html(`
                <div class="loadingio-spinner-ellipsis-w2l1qr6gk3n">
                    <div class="ldio-80g99pgzdvx">
                    <div></div>
                    <div></div>
                    <div></div>
                    <div></div>
                    <div></div>
                    </div>
                </div>`);
                return;
            }
            $(element).html(tagToPlainText(list[index]));
        });
    }
}
