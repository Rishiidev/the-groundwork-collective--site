// forge-bespoke / The Groundwork Collective / cro/quote-builder.js
// 4-question scope -> WhatsApp pre-fill with the answers.
// No dependencies. Loads as deferred script on /index.html.

(function () {
  "use strict";

  var WA_BASE = "https://wa.me/919819894011";
  var LABELS = {
    learn: {
      "drawing": "drawing",
      "visual-art": "visual art (painting / mixed media)",
      "music": "music",
      "expression": "personal expression / creative direction",
      "other": "something else"
    },
    level: {
      "beginner": "complete beginner",
      "some-practice": "some practice",
      "returning": "returning after a break",
      "intermediate": "intermediate"
    },
    goal: {
      "personal": "personal practice",
      "portfolio": "portfolio",
      "career": "career change",
      "healing": "healing / expression",
      "explore": "just exploring"
    },
    start: {
      "this-month": "this month",
      "3-months": "next 3 months",
      "just-looking": "just looking"
    }
  };

  function buildMessage(answers) {
    return [
      "Hi — found The Groundwork Collective online.",
      "",
      "I'd like to discuss a possible track:",
      "- I want to learn: " + LABELS.learn[answers.learn],
      "- Where I am: " + LABELS.level[answers.level],
      "- My goal: " + LABELS.goal[answers.goal],
      "- I'd like to start: " + LABELS.start[answers.start],
      "",
      "Could we set up a discovery call?"
    ].join("\n");
  }

  function init() {
    var form = document.getElementById("quote-builder-form");
    if (!form) return;
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = new FormData(form);
      var answers = {
        learn: data.get("learn"),
        level: data.get("level"),
        goal: data.get("goal"),
        start: data.get("start")
      };
      var missing = [];
      for (var key in answers) {
        if (!answers[key]) missing.push(key);
      }
      if (missing.length) {
        var firstMissing = form.querySelector("[name=\"" + missing[0] + "\"]");
        if (firstMissing) firstMissing.focus();
        return;
      }
      var msg = buildMessage(answers);
      var url = WA_BASE + "?text=" + encodeURIComponent(msg);
      window.open(url, "_blank", "noopener");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
