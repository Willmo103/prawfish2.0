document.addEventListener("DOMContentLoaded", function () {
  const searchTypeSelect = document.getElementById("search_type");
  const redditorInput = document.getElementById("redditor");
  const subredditInput = document.getElementById("subreddit");
  const submissionIdInput = document.getElementById("submission_id");

  var popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-toggle="popover"]')
  );
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

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
