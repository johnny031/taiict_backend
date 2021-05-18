function deleteNews(newsId) {
  fetch("/json-data", {
    method: "POST",
    body: JSON.stringify({ newsId: newsId }),
  }).then((_res) => {
    window.location.href = "/news-list";
  });
}
