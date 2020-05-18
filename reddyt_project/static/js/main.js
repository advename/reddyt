addEventListener("load", function() {
  // Init
});

const voteBtn = document.querySelectorAll(".post-vote");

voteBtn.forEach(btn => {
  btn.addEventListener("click", handleVoteClick);
});

function handleVoteClick(e) {
  const postId = this.dataset.postid;
  let vote = null;
  if (this.classList.contains("upvote")) {
    vote = true;
  } else {
    vote = false;
  }
  sendVoteClick(postId, vote);
  changeVoteDisplay(postId, vote);
}

function sendVoteClick(postId, vote) {
  fetch("http://127.0.0.1:8000/api/v1/discussion/vote/", {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": getCookieValue("csrftoken")
    },
    method: "POST",
    credentials: "include",
    body: JSON.stringify({ vote: vote, post_id: postId })
  })
    .then(res => res.json())
    .then(json => {
      console.log(json); // output the JSON response
    });
}

function changeVoteDisplay(postId, vote) {
  const voteElem = document.querySelector(
    `.discussion.post-${postId} .left .votes`
  );
  const currentVotes = Number(voteElem.textContent);
  const changer = vote ? 1 : -1;
  const newVotes = currentVotes + changer;
  console.log(currentVotes);
  voteElem.textContent = newVotes;
}

/**
 * Get the value of a stored cookie
 * @param {string} a The name of the cookie to retreive
 */
function getCookieValue(a) {
  var b = document.cookie.match("(^|[^;]+)\\s*" + a + "\\s*=\\s*([^;]+)");
  return b ? b.pop() : "";
}
