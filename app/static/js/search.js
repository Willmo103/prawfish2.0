document.addEventListener("DOMContentLoaded", function () {
  const searchTypeSelect = document.getElementById("search_type");
  const redditorInput = document.getElementById("redditor");
  const subredditInput = document.getElementById("subreddit");
  const submissionIdInput = document.getElementById("submission_id");

  function toggleInputs() {
    const searchType = searchTypeSelect.value;
    redditorInput.disabled = searchType !== "redditor";
    subredditInput.disabled = searchType !== "subreddit";
    submissionIdInput.disabled =
      searchType !== "submission" && searchType !== "comments";
  }

  searchTypeSelect.addEventListener("change", toggleInputs);
  toggleInputs();
});
