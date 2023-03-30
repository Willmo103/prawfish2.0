def perform_search(params, reddit_instance):
    search_type = params.get("search_type")
    query = params.get("query")
    sort = params.get("sort")
    syntax = params.get("syntax")
    time_filter = params.get("time_filter")
    limit = params.get("limit")

    if search_type == "subreddit":
        subreddit_name = params.get("subreddit")
        subreddit = reddit_instance.subreddit(subreddit_name)
        search_results = subreddit.search(
            query, sort=sort, syntax=syntax, time_filter=time_filter, limit=limit
        )
    elif search_type == "redditor":
        redditor_name = params.get("redditor")
        redditor = reddit_instance.redditor(redditor_name)
        search_results = redditor.search(
            query, sort=sort, time_filter=time_filter, limit=limit
        )
    elif search_type == "submission":
        submission_id = params.get("submission_id")
        submission = reddit_instance.submission(id=submission_id)
        search_results = submission.search(
            query, sort=sort, syntax=syntax, time_filter=time_filter, limit=limit
        )
    elif search_type == "comments":
        submission_id = params.get("submission_id")
        submission = reddit_instance.submission(id=submission_id)
        search_results = submission.comments.search(
            query, sort=sort, time_filter=time_filter, limit=limit
        )
    else:
        return None
