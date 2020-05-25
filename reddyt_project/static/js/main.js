addEventListener("load", function() {
  // Init
  unreadNotificationHandler();

  // Force Unread notification count GET request to the API by using the notif_ref=1 query parameter.
  if (getURLParamValue("notif_ref") == "true") {
    fetchUnreadNotification();
  }
});

const currentURL =
  location.protocol +
  "//" +
  location.hostname +
  (location.port ? ":" + location.port : "");
const apiURL = `${currentURL}/api/v1/`;

const wsScheme = window.location.protocol == "https:" ? "wss" : "ws"; // check if https page, if true, use secure websockets transport
const wsURL =
  wsScheme +
  "://" +
  location.hostname +
  (location.port ? ":" + location.port : "") +
  "/ws/";
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
  fetch(apiURL + "discussion/vote/", {
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

/**
 * Web sockets setup "Django Channels"
 */

const socket = new WebSocket(wsURL + "notifications/");

socket.addEventListener("open", function(event) {
  console.log("WebSockets connection created.");
});

socket.addEventListener("close", function(event) {
  console.error("WebSockets socket closed unexpectedly");
});

// Listen for messages
socket.addEventListener("message", function(event) {
  message = JSON.parse(event.data);
  console.log("Message from server ", message);

  // Listen for updates in unreaded notification counts
  if ("unread_count" in message) {
    console.log(message.unread_count);
    setUnreadNotification(message.unread_count);
  }
});

// // Send websocket message on Click
// document.querySelector(".submit-comment").addEventListener("click", () => {
//   console.log("Click");
//   socket.send(
//     JSON.stringify({
//       message: "Hello Hakuna Matata"
//     })
//   );
// });

/**
 * Notification circle displaying the amount of notifications
 */
const notifSpan = document.querySelector("#notification-counter");
const unreadStorageName = "unread_notif";

function unreadNotificationHandler() {
  if (!existsUnreadNotificationStorage()) {
    fetchUnreadNotification();
  } else {
    displayUnreadNotificationStatus();
  }
}

function setUnreadNotification(val) {
  localStorage.setItem(unreadStorageName, val);
  displayUnreadNotificationStatus();
}

function displayUnreadNotificationStatus() {
  if (!existsUnreadNotificationStorage) {
    return fetchUnreadNotification();
  }
  let val = Number(localStorage.getItem(unreadStorageName));
  if (val) {
    notifSpan.textContent = val;
    notifSpan.style.display = "flex";
  }
}

function fetchUnreadNotification() {
  fetch(apiURL + "notification/unread/", {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    credentials: "include"
  })
    .then(res => {
      if (res.ok) {
        return res.json();
      } else {
        throw res;
      }
    })
    .then(data => {
      setUnreadNotification(data.unread_notif);
    })
    .catch(err => {
      err.json().then(data => {
        console.log(data);
      });
    });
}

function existsUnreadNotificationStorage() {
  if (localStorage.getItem(unreadStorageName) === null) {
    return false;
  } else {
    return true;
  }
}

/**
 * Helper functions
 */

// Get Cookie, Source: https://stackoverflow.com/a/25490531/3673659
function getCookieValue(a) {
  var b = document.cookie.match("(^|[^;]+)\\s*" + a + "\\s*=\\s*([^;]+)");
  return b ? b.pop() : "";
}

// Get URL parameter query values, Source: https://stackoverflow.com/a/979995/3673659, but modified version
function getURLParamValue(query) {
  var parameters = location.search.substr(1);
  var vars = parameters.split("&");
  var query_string = {};
  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split("=");
    var key = decodeURIComponent(pair[0]);
    var value = decodeURIComponent(pair[1]);
    // If first entry with this name
    if (typeof query_string[key] === "undefined") {
      query_string[key] = decodeURIComponent(value);
      // If second entry with this name
    } else if (typeof query_string[key] === "string") {
      var arr = [query_string[key], decodeURIComponent(value)];
      query_string[key] = arr;
      // If third or later entry with this name
    } else {
      query_string[key].push(decodeURIComponent(value));
    }
  }
  return query_string[query];
}
