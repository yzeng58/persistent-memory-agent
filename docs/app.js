const turns = [
  {
    text: "I live in Seattle and prefer meetings after 10am.",
    writes: [
      {
        subject: "user",
        predicate: "home_city",
        value: "Seattle",
        kind: "profile",
        importance: 0.8,
      },
      {
        subject: "user",
        predicate: "meeting_time",
        value: "after 10:00 local time",
        kind: "preference",
        importance: 0.9,
      },
    ],
  },
  {
    text: "I am exploring research roles focused on memory and persistent agents.",
    writes: [
      {
        subject: "user",
        predicate: "career_focus",
        value: "memory and persistent-agent research roles",
        kind: "project",
        importance: 1.0,
      },
    ],
  },
  {
    text: "I moved to San Francisco last month.",
    writes: [
      {
        subject: "user",
        predicate: "home_city",
        value: "San Francisco",
        kind: "profile",
        importance: 0.8,
      },
    ],
  },
  {
    text: "When discussing opportunities, lead with my context-management work.",
    writes: [
      {
        subject: "user",
        predicate: "opportunity_positioning",
        value: "lead with context-management work",
        kind: "procedure",
        importance: 0.95,
      },
    ],
  },
];

let processedTurns = 0;
let nextMemoryId = 1;
let memories = [];
const maxContextChars = 520;
const tokenAliases = {
  agents: "agent",
  calls: "meeting",
  conversation: "meeting",
  conversations: "meeting",
  opportunities: "career",
  opportunity: "career",
  researcher: "research",
  researchers: "research",
  roles: "career",
  role: "career",
  schedule: "meeting",
  scheduling: "meeting",
};
const stopwords = new Set([
  "a",
  "about",
  "an",
  "and",
  "for",
  "i",
  "in",
  "my",
  "of",
  "the",
  "to",
  "with",
]);

const conversation = document.querySelector("#conversation");
const memoryLedger = document.querySelector("#memory-ledger");
const retrievalResults = document.querySelector("#retrieval-results");
const turnCounter = document.querySelector("#turn-counter");
const nextButton = document.querySelector("#next-button");
const resetButton = document.querySelector("#reset-button");
const retrieveButton = document.querySelector("#retrieve-button");
const queryInput = document.querySelector("#query-input");

function escapeHtml(value) {
  return value.replace(
    /[&<>"']/g,
    (character) =>
      ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
      })[character],
  );
}

function processNextTurn() {
  if (processedTurns >= turns.length) {
    return;
  }

  const turn = turns[processedTurns];
  const eventId = processedTurns + 1;
  for (const write of turn.writes) {
    const active = memories.find(
      (memory) =>
        memory.subject === write.subject &&
        memory.predicate === write.predicate &&
        memory.kind === write.kind &&
        memory.status === "active",
    );
    if (active && active.value !== write.value) {
      active.status = "superseded";
      active.validTo = eventId;
    }
    if (!active || active.value !== write.value) {
      memories.push({
        ...write,
        id: nextMemoryId,
        sourceEventId: eventId,
        supersedesId: active ? active.id : null,
        status: "active",
        confidence: 1.0,
      });
      nextMemoryId += 1;
    }
  }

  processedTurns += 1;
  render();
  retrieve();
}

function resetDemo() {
  processedTurns = 0;
  nextMemoryId = 1;
  memories = [];
  render();
}

function render() {
  turnCounter.textContent = `${processedTurns} / ${turns.length} turns`;
  nextButton.disabled = processedTurns >= turns.length;

  if (processedTurns === 0) {
    conversation.className = "conversation empty-state";
    conversation.textContent =
      "Process a turn to begin the synthetic conversation.";
    memoryLedger.className = "memory-ledger empty-state";
    memoryLedger.textContent = "Durable memory writes will appear here.";
    retrievalResults.className = "retrieval-results empty-state";
    retrievalResults.textContent =
      "Process conversation turns, then retrieve a bounded memory context.";
    return;
  }

  conversation.className = "conversation";
  conversation.innerHTML = turns
    .slice(0, processedTurns)
    .map(
      (turn, index) => `
        <div class="message">
          <div class="message-label">Event ${index + 1} / user</div>
          <p>${escapeHtml(turn.text)}</p>
        </div>
      `,
    )
    .join("");

  memoryLedger.className = "memory-ledger";
  const latestIdByKey = new Map();
  for (const memory of memories) {
    const key = `${memory.subject}.${memory.predicate}.${memory.kind}`;
    latestIdByKey.set(key, Math.max(latestIdByKey.get(key) || 0, memory.id));
  }
  memoryLedger.innerHTML = [...memories]
    .sort((left, right) => {
      const leftKey = `${left.subject}.${left.predicate}.${left.kind}`;
      const rightKey = `${right.subject}.${right.predicate}.${right.kind}`;
      return (
        latestIdByKey.get(rightKey) - latestIdByKey.get(leftKey) ||
        right.id - left.id
      );
    })
    .map(
      (memory) => `
        <div class="memory-card ${memory.status}">
          <div class="memory-topline">
            <span class="memory-key">${escapeHtml(
              `${memory.subject}.${memory.predicate}`,
            )}</span>
            <span class="status ${memory.status}">${memory.status}</span>
          </div>
          <p class="memory-value">${escapeHtml(memory.value)}</p>
          <div class="memory-meta">
            ${escapeHtml(memory.kind)} / source event ${memory.sourceEventId}
            ${
              memory.supersedesId
                ? `/ supersedes memory ${memory.supersedesId}`
                : ""
            }
          </div>
        </div>
      `,
    )
    .join("");
}

function tokenize(text) {
  const rawTokens =
    text.toLowerCase().replaceAll("_", " ").match(/[a-z0-9_]+/g) || [];
  return new Set(
    rawTokens
      .filter((token) => !stopwords.has(token))
      .map((token) => tokenAliases[token] || token),
  );
}

function retrieve() {
  if (processedTurns === 0) {
    return;
  }

  const query = queryInput.value.trim();
  const queryTokens = tokenize(query);
  const activeMemories = memories.filter((memory) => memory.status === "active");
  const ranked = activeMemories
    .map((memory) => {
      const memoryTokens = tokenize(
        `${memory.subject} ${memory.predicate} ${memory.value} ${memory.kind}`,
      );
      const overlap = [...queryTokens].filter((token) =>
        memoryTokens.has(token),
      ).length;
      const lexicalScore = queryTokens.size ? overlap / queryTokens.size : 0;
      const age = Math.max(processedTurns - memory.sourceEventId, 0);
      const recencyScore = Math.exp(-age / 30);
      const score =
        0.55 * lexicalScore +
        0.2 * memory.importance +
        0.15 * memory.confidence +
        0.1 * recencyScore;
      return { memory, score, lexicalScore };
    })
    .filter(({ lexicalScore }) => lexicalScore > 0)
    .sort((left, right) => right.score - left.score)
    .slice(0, 8);

  const contextLines = [];
  let contextLength = 0;
  for (const { memory } of ranked) {
    const line =
      `[${memory.kind}] ${memory.subject}.${memory.predicate} = ` +
      `${memory.value} (source event ${memory.sourceEventId}, ` +
      `confidence ${memory.confidence.toFixed(2)})`;
    const addedLength = line.length + (contextLines.length ? 1 : 0);
    if (contextLength + addedLength > maxContextChars) {
      break;
    }
    contextLines.push(line);
    contextLength += addedLength;
  }
  const context = contextLines.join("\n");

  retrievalResults.className = "retrieval-results";
  retrievalResults.innerHTML = `
    ${
      ranked.length
        ? ranked
      .map(
        ({ memory, score }) => `
          <div class="retrieved-memory">
            <div class="score">${score.toFixed(2)}</div>
            <p>
              <strong>${escapeHtml(
                `${memory.subject}.${memory.predicate}`,
              )}</strong><br>
              ${escapeHtml(memory.value)}
            </p>
          </div>
        `,
      )
      .join("")
        : '<p>No active memory passed the relevance gate.</p>'
    }
    ${
      context
        ? `<div class="context-block">${escapeHtml(context)}</div>`
        : ""
    }
  `;
}

nextButton.addEventListener("click", processNextTurn);
resetButton.addEventListener("click", resetDemo);
retrieveButton.addEventListener("click", retrieve);
queryInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    retrieve();
  }
});

render();
