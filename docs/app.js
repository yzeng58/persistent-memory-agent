const scenes = {
  morning: {
    summary: "7 workflows coordinated",
    activity: [
      {
        skill: "calendar-ops",
        text: "Checked four calendars and resolved today's timeline.",
      },
      {
        skill: "email-ops",
        text: "Triaged Gmail and Outlook; drafted two replies.",
      },
      {
        skill: "reporting-ops",
        text: "Created a follow-up reminder from an unanswered email.",
      },
      {
        skill: "investment-ops",
        text: "Reviewed portfolio changes and current market context.",
      },
      {
        skill: "social-scout",
        text: "Filtered AI news down to three relevant developments.",
      },
      {
        skill: "spending-ops",
        text: "Matched today's plans with card offers and spending targets.",
      },
      {
        skill: "beauty-search",
        text: "Kept personal style and care recommendations in context.",
      },
    ],
    workspace: `
      <div class="workspace-heading reveal" style="--delay: 0ms">
        <div>
          <p class="workspace-kicker">Thursday / August 20</p>
          <h3>Good morning, Yuchen.</h3>
          <p>Your day is organized. Three items need your attention.</p>
        </div>
        <div class="ready-badge">
          <span></span>
          Ready before your first prompt
        </div>
      </div>

      <div class="morning-grid">
        <article class="dashboard-card schedule-card reveal" style="--delay: 90ms">
          <div class="card-heading">
            <span class="card-icon calendar-icon">CAL</span>
            <div>
              <p>Today's schedule</p>
              <small>4 calendars combined</small>
            </div>
          </div>
          <div class="timeline-item">
            <time>11:30</time>
            <div>
              <strong>BenchPress sync</strong>
              <span>Next version prepared</span>
            </div>
          </div>
          <div class="timeline-item">
            <time>13:30</time>
            <div>
              <strong>Research review</strong>
              <span>Reading list attached</span>
            </div>
          </div>
          <div class="timeline-item">
            <time>16:00</time>
            <div>
              <strong>Focus block</strong>
              <span>Protected from new meetings</span>
            </div>
          </div>
        </article>

        <article class="dashboard-card reveal" style="--delay: 160ms">
          <div class="card-heading">
            <span class="card-icon mail-icon">MAIL</span>
            <div>
              <p>Inbox and commitments</p>
              <small>Gmail + Outlook</small>
            </div>
          </div>
          <div class="metric-row">
            <strong>14</strong>
            <span>new messages triaged</span>
          </div>
          <ul class="clean-list">
            <li><b>2</b> replies drafted</li>
            <li><b>1</b> reminder created automatically</li>
            <li><b>0</b> urgent deadlines missed</li>
          </ul>
        </article>

        <article class="dashboard-card reveal" style="--delay: 230ms">
          <div class="card-heading">
            <span class="card-icon market-icon">AI</span>
            <div>
              <p>Markets and AI</p>
              <small>Only relevant changes</small>
            </div>
          </div>
          <div class="signal-item">
            <span>Portfolio</span>
            <strong>No urgent action</strong>
          </div>
          <div class="signal-item">
            <span>AI news</span>
            <strong>3 stories worth reading</strong>
          </div>
          <div class="signal-item">
            <span>Research</span>
            <strong>1 paper added to queue</strong>
          </div>
        </article>

        <article class="dashboard-card reveal" style="--delay: 300ms">
          <div class="card-heading">
            <span class="card-icon spend-icon">USD</span>
            <div>
              <p>Spend and eat</p>
              <small>Offers + budget + preferences</small>
            </div>
          </div>
          <div class="offer-banner">
            <span>Card offer found</span>
            <strong>10% back on dining</strong>
          </div>
          <div class="food-row">
            <div class="food-avatar">F</div>
            <div>
              <span>Lunch suggestion</span>
              <strong>Salmon bowl nearby</strong>
              <small>High protein / within today's target</small>
            </div>
          </div>
        </article>
      </div>

      <div class="prepared-actions reveal" style="--delay: 380ms">
        <p>Prepared for you</p>
        <div>
          <span>Review 2 email drafts</span>
          <span>Ask to move BenchPress sync to 10am</span>
          <span>Save dining offer</span>
        </div>
      </div>
    `,
  },
  manager: {
    summary: "6 decisions made before drafting",
    activity: [
      {
        skill: "people-ops",
        text: "Looked up Dimitris: manager and BenchPress collaborator.",
      },
      {
        skill: "workplace-communication",
        text: "Selected a concise, warm, proactive tone.",
      },
      {
        skill: "calendar-ops",
        text: "Confirmed 10:00am is open; the change still needs agreement.",
      },
      {
        skill: "teams-ops",
        text: "Selected Microsoft Teams as the established channel.",
      },
      {
        skill: "browser",
        text: "Routed through authenticated Chrome DevTools for Teams.",
      },
      {
        skill: "confirmation-gate",
        text: "Stopped before Send and prepared the exact draft for review.",
      },
    ],
    workspace: `
      <div class="workspace-heading reveal" style="--delay: 0ms">
        <div>
          <p class="workspace-kicker">Cross-app execution</p>
          <h3>One request. The agent resolves the workflow.</h3>
          <p>Identity, relationship, tone, schedule, channel, and tool all matter.</p>
        </div>
        <div class="ready-badge route-badge">
          <span></span>
          No generic advice
        </div>
      </div>

      <div class="user-request reveal" style="--delay: 80ms">
        <div class="request-avatar">YZ</div>
        <p>
          Message Dimitris that I have the next BenchPress version ready, and
          ask whether we can move our meeting to 10am.
        </p>
      </div>

      <div class="route-grid">
        <article class="route-card reveal" style="--delay: 150ms">
          <span class="route-number">01</span>
          <p>Who is this?</p>
          <strong>Dimitris</strong>
          <small>Manager + BenchPress collaborator</small>
          <code>people-ops</code>
        </article>
        <article class="route-card reveal" style="--delay: 220ms">
          <span class="route-number">02</span>
          <p>How should it sound?</p>
          <strong>Concise and proactive</strong>
          <small>Warm, direct, no over-explaining</small>
          <code>workplace-communication</code>
        </article>
        <article class="route-card reveal" style="--delay: 290ms">
          <span class="route-number">03</span>
          <p>Is 10am possible?</p>
          <strong>10am is available</strong>
          <small>Shared change requires confirmation</small>
          <code>calendar-ops</code>
        </article>
        <article class="route-card reveal" style="--delay: 360ms">
          <span class="route-number">04</span>
          <p>Where should it go?</p>
          <strong>Microsoft Teams</strong>
          <small>Authenticated Chrome profile required</small>
          <code>teams-ops -> Chrome DevTools</code>
        </article>
      </div>

      <article class="draft-card reveal" style="--delay: 440ms">
        <div class="draft-topline">
          <div>
            <span>Draft ready in Microsoft Teams</span>
            <strong>To: Dimitris</strong>
          </div>
          <span class="draft-status">Waiting for approval</span>
        </div>
        <div class="draft-message">
          Hi Dimitris - could we move our BenchPress sync to 10am? I
          have the next version ready, so we can review it and use the rest of
          the time for anything else you would like to discuss.
        </div>
        <div class="draft-actions">
          <button class="approve-button" type="button">Approve and send</button>
          <button class="edit-button" type="button">Edit draft</button>
        </div>
      </article>
    `,
  },
};

const workspace = document.querySelector("#workspace");
const activityFeed = document.querySelector("#activity-feed");
const activitySummary = document.querySelector("#activity-summary");
const sceneButtons = document.querySelectorAll(".scene-button");
let activityTimers = [];

function clearActivityTimers() {
  for (const timer of activityTimers) {
    window.clearTimeout(timer);
  }
  activityTimers = [];
}

function animateActivity(items, summary) {
  clearActivityTimers();
  activityFeed.innerHTML = "";
  activitySummary.textContent = "Routing workflows...";

  items.forEach((item, index) => {
    const timer = window.setTimeout(() => {
      const row = document.createElement("div");
      row.className = "activity-item";
      row.innerHTML = `
        <div class="activity-status"><span></span></div>
        <div>
          <strong>${item.skill}</strong>
          <p>${item.text}</p>
        </div>
      `;
      activityFeed.appendChild(row);
      window.requestAnimationFrame(() => row.classList.add("visible"));

      const completeTimer = window.setTimeout(() => {
        row.classList.add("complete");
      }, 260);
      activityTimers.push(completeTimer);

      if (index === items.length - 1) {
        const summaryTimer = window.setTimeout(() => {
          activitySummary.textContent = summary;
        }, 360);
        activityTimers.push(summaryTimer);
      }
    }, index * 430);
    activityTimers.push(timer);
  });
}

function renderScene(sceneName) {
  const scene = scenes[sceneName];
  workspace.innerHTML = scene.workspace;
  sceneButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.scene === sceneName);
  });
  animateActivity(scene.activity, scene.summary);
}

sceneButtons.forEach((button) => {
  button.addEventListener("click", () => renderScene(button.dataset.scene));
});

workspace.addEventListener("click", (event) => {
  if (event.target.matches(".approve-button")) {
    const status = workspace.querySelector(".draft-status");
    status.textContent = "Demo only - nothing sent";
    event.target.textContent = "Approval captured";
    event.target.disabled = true;
  }
  if (event.target.matches(".edit-button")) {
    const message = workspace.querySelector(".draft-message");
    message.contentEditable = "true";
    message.focus();
    event.target.textContent = "Editing";
  }
});

renderScene("morning");
