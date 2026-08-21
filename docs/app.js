const command = "yuchen-assistant";

const stage = document.querySelector("#stage");
const adNarration = document.querySelector("#ad-narration");
const adNarrationHeadline = document.querySelector("#ad-narration-headline");
const adNarrationDetail = document.querySelector("#ad-narration-detail");
const cursor = document.querySelector("#cursor");
const terminalWindow = document.querySelector("#terminal-window");
const typedCommand = document.querySelector("#typed-command");
const commandCaret = document.querySelector("#command-caret");
const bootStatus = document.querySelector("#boot-status");
const assistantWindow = document.querySelector("#assistant-window");
const assistantBody = document.querySelector(".assistant-body");
const assistantScroll = document.querySelector("#assistant-content");
const preparationPanel = document.querySelector("#preparation-panel");
const preparationTitle = document.querySelector("#preparation-title");
const preparationNote = document.querySelector("#preparation-note");
const preparationRoutes = document.querySelector("#preparation-routes");
const toolPreview = document.querySelector("#tool-preview");
const toolPreviewTitle = document.querySelector("#tool-preview-title");
const dayHeading = document.querySelector("#day-heading");
const importantCard = document.querySelector("#important-card");
const scheduleCard = document.querySelector("#schedule-card");
const reportSections = document.querySelector("#report-sections");
const reportSectionItems = [...document.querySelectorAll(".report-section")];
const conversationWindow = document.querySelector("#conversation-window");
const conversationScroll = document.querySelector("#conversation-scroll");
const userRequestBubble = document.querySelector("#user-request-bubble");
const conversationSteps = [...document.querySelectorAll(".trace-step")];
const replyDraft = document.querySelector("#reply-draft");
const chatComposer = document.querySelector("#chat-composer");
const chatInput = document.querySelector("#chat-input");
const stockDetailWindow = document.querySelector("#stock-detail-window");
const stockScroll = document.querySelector("#stock-scroll");
const stockTrigger = document.querySelector(".stock-section .report-trigger");
const stockSection = document.querySelector(".stock-section");
const desktop = document.querySelector(".desktop");
const chainLinks = [...document.querySelectorAll(".chain-link")];
const scanRows = [...document.querySelectorAll(".scan-row, .scan-total")];
const gateRows = [...document.querySelectorAll(".gate-row")];
const memoryReceipts = [...document.querySelectorAll(".memory-receipt")];
const memoryBlock = document.querySelector(".memory-block");
const closingAction = document.querySelector(".closing-action");
const chromeAddress = document.querySelector("#chrome-address");
const investmentSteps = [...document.querySelectorAll(".invest-step")];
const investmentOutput = document.querySelector(".invest-output");
const sourceActivityTitle = document.querySelector("#source-activity-title");
const sourceActivityList = document.querySelector("#source-activity-list");

const reportPreparationSteps = [
  [10500, "Planning meals around your day", ["Calendar", "Spending", "Card offers"], "Matching options to your location, plans, preferences, and useful offers."],
  [12700, "Triaging work and inbox", ["Outlook · Chrome", "Teams · Chrome", "Project memory"], "Finding messages and company updates that need action today."],
  [14900, "Reviewing your portfolio", ["Holdings", "Market news", "Risk context"], "Connecting current positions with relevant news and possible actions."],
  [17100, "Filtering AI and research", ["AI news", "New papers", "Research memory"], "Removing noise and keeping developments that matter to your work."],
  [19300, "Matching useful offers", ["Card offers", "Coupons", "Spending plan"], "Keeping only deals that fit what you may actually buy today."],
  [21500, "Checking secondhand activity", ["Marketplace", "Buyer messages", "Price changes"], "Surfacing listing changes that need your attention."],
];
const reportSourceActivities = [
  {
    previewTitle: "Google · Calendar · Card offers",
    query: 'Google: "restaurants in Bellevue"',
    operations: [
      ["📍", "Google Maps", 'Search "restaurants in Bellevue"', "24 options"],
      ["📅", "Calendar", "Check today's lunch window and location", "12–1 PM"],
      ["💳", "Card offers", "Match dining credits and cashback", "3 offers"],
      ["🧠", "Food memory", "Filter by saved preferences", "2 picks"],
    ],
  },
  {
    previewTitle: "Outlook · Teams · Project memory",
    query: "Unread work messages and project updates",
    operations: [
      ["✉️", "Outlook · Chrome", "Open unread work inbox", "7 unread"],
      ["💬", "Teams · Chrome", "Check mentions and manager messages", "2 important"],
      ["🧪", "BenchPress memory", "Load current project context", "next version"],
      ["⚡", "Priority model", "Rank by deadline and relationship", "5 updates"],
    ],
  },
  null,
  {
    previewTitle: "Scholar · arXiv · Community",
    query: "AI agent research worth reading today",
    operations: [
      ["🎓", "Google Scholar", 'Search "LLM agent memory"', "38 new"],
      ["📄", "arXiv", "Scan new cs.AI and cs.CL papers", "126 papers"],
      ["🌐", "Hacker News + X", "Check active technical discussions", "54 signals"],
      ["🧠", "Research memory", "Match BenchPress and agent interests", "3 reads"],
    ],
  },
  {
    previewTitle: "Amex · Chase · Shopping",
    query: "Offers that match today's spending",
    operations: [
      ["💳", "Amex Offers", "Load activated and newly available offers", "6 matches"],
      ["🏦", "Chase Offers", "Check cashback expiring soon", "3 expiring"],
      ["🛍️", "Google Shopping", "Compare prices for saved needs", "12 prices"],
      ["🧠", "Spending memory", "Remove low-priority purchases", "2 useful"],
    ],
  },
  {
    previewTitle: "Marketplace · Messenger · Pricing",
    query: "Listing, buyer, and local price changes",
    operations: [
      ["🏷️", "Facebook Marketplace", "Open the seller dashboard in Chrome", "4 listings"],
      ["💬", "Messenger · Chrome", "Check new buyer messages", "1 reply"],
      ["📈", "Listing history", "Compare views and saves", "−18% views"],
      ["🔎", "Local pricing", "Check comparable listings nearby", "lower $10"],
    ],
  },
];
const chatRequest = "Check Marcus's latest Teams message and help me reply.";
const teamsAddress = "teams.microsoft.com/v2/";
const conversationStepTimes = [53500, 55500, 57500, 65000, 69000];

let timers = [];
let typingTimer = null;

function schedule(callback, delay) {
  const timer = window.setTimeout(callback, delay);
  timers.push(timer);
}

function showAdNarration(headline, detail) {
  adNarration.classList.remove("changing");
  adNarrationHeadline.textContent = headline;
  adNarrationDetail.textContent = detail;
  void adNarration.offsetWidth;
  adNarration.classList.add("visible", "changing");
}

function showPreparation(title, routes, note) {
  preparationTitle.textContent = title;
  preparationNote.textContent = note;
  preparationRoutes.replaceChildren(...routes.map((route) => {
    const chip = document.createElement("span");
    chip.textContent = route;
    return chip;
  }));
}

function showToolPreview(tool, title, phase = "") {
  toolPreview.dataset.tool = tool;
  toolPreview.dataset.phase = phase;
  toolPreviewTitle.textContent = title;
}

function showSourceActivity(activity) {
  showToolPreview("sources", activity.previewTitle);
  sourceActivityTitle.textContent = activity.query;
  sourceActivityList.replaceChildren(...activity.operations.map(([icon, source, action, result]) => {
    const operation = document.createElement("article");
    operation.className = "source-operation";

    const mark = document.createElement("span");
    mark.textContent = icon;

    const copy = document.createElement("div");
    const sourceName = document.createElement("b");
    sourceName.textContent = source;
    const actionText = document.createElement("p");
    actionText.textContent = action;
    copy.append(sourceName, actionText);

    const status = document.createElement("small");
    status.textContent = result;
    operation.append(mark, copy, status);
    return operation;
  }));

  [...sourceActivityList.children].forEach((operation, index) => {
    schedule(() => operation.classList.add("visible"), 120 + index * 220);
  });
}

function scrollHomeTo(element) {
  const target = element.getBoundingClientRect();
  const body = assistantScroll.getBoundingClientRect();
  assistantScroll.scrollTo({
    top: assistantScroll.scrollTop + target.top - body.top - body.height * 0.55,
    behavior: "smooth",
  });
}

function scrollDetailTo(element) {
  const target = element.getBoundingClientRect();
  const body = stockScroll.getBoundingClientRect();
  stockScroll.scrollTo({
    top: stockScroll.scrollTop + target.top - body.top - body.height * 0.24,
    behavior: "smooth",
  });
}

function resetAnimation() {
  timers.forEach((timer) => window.clearTimeout(timer));
  timers = [];
  if (typingTimer !== null) {
    window.clearInterval(typingTimer);
    typingTimer = null;
  }

  cursor.setAttribute("class", "cursor");
  cursor.style.left = "";
  cursor.style.top = "";
  terminalWindow.className = "terminal-window";
  typedCommand.textContent = "";
  commandCaret.className = "command-caret";
  bootStatus.className = "boot-status";
  assistantWindow.className = "assistant-window";
  assistantBody.className = "assistant-body";
  adNarration.className = "ad-narration";
  preparationPanel.className = "preparation-panel";
  showPreparation(
    "Searching your inbox",
    ["Gmail · API", "Outlook · Chrome"],
    "Automatically choosing the best available access method for each account.",
  );
  showToolPreview("gmail", "Gmail API");
  dayHeading.className = "day-heading";
  importantCard.className = "important-card";
  scheduleCard.className = "schedule-card";
  reportSections.className = "report-sections";
  reportSectionItems.forEach((section) => section.classList.remove("visible"));
  conversationWindow.className = "conversation-window";
  userRequestBubble.className = "user-request-bubble";
  conversationSteps.forEach((step) => step.classList.remove("visible"));
  replyDraft.className = "reply-draft";
  chatComposer.className = "chat-composer";
  chatInput.textContent = "";
  chromeAddress.textContent = "";
  stockDetailWindow.className = "stock-detail-window";
  stockSection.classList.remove("opening");
  chainLinks.forEach((link) => link.classList.remove("visible"));
  scanRows.forEach((row) => row.classList.remove("visible"));
  gateRows.forEach((row) => row.classList.remove("visible"));
  memoryReceipts.forEach((receipt) => receipt.classList.remove("visible"));
  investmentSteps.forEach((step) => step.classList.remove("visible"));
  investmentOutput.scrollTop = 0;
  sourceActivityList.replaceChildren();
  closingAction.classList.remove("visible");
  assistantScroll.scrollTop = 0;
  conversationScroll.scrollTop = 0;
  stockScroll.scrollTop = 0;
}

function typeCommand() {
  let index = 0;
  commandCaret.classList.add("typing");
  typingTimer = window.setInterval(() => {
    typedCommand.textContent = command.slice(0, index + 1);
    index += 1;
    if (index >= command.length) {
      window.clearInterval(typingTimer);
      typingTimer = null;
      commandCaret.classList.remove("typing");
      commandCaret.classList.add("enter");
    }
  }, 45);
}

function typeChatRequest() {
  let index = 0;
  typingTimer = window.setInterval(() => {
    chatInput.textContent = chatRequest.slice(0, index + 1);
    index += 1;
    if (index >= chatRequest.length) {
      window.clearInterval(typingTimer);
      typingTimer = null;
      chatComposer.classList.add("ready");
    }
  }, 38);
}

function typeTeamsAddress() {
  let index = 0;
  typingTimer = window.setInterval(() => {
    chromeAddress.textContent = teamsAddress.slice(0, index + 1);
    index += 1;
    if (index >= teamsAddress.length) {
      window.clearInterval(typingTimer);
      typingTimer = null;
    }
  }, 85);
}

function playAnimation() {
  resetAnimation();

  schedule(() => cursor.classList.add("hidden"), 180);
  schedule(() => {
    terminalWindow.classList.add("open");
  }, 680);
  schedule(typeCommand, 980);
  schedule(() => bootStatus.classList.add("visible"), 1850);
  schedule(() => {
    terminalWindow.classList.add("complete");
    assistantWindow.classList.add("visible");
  }, 2450);
  schedule(() => preparationPanel.classList.add("visible"), 2850);
  schedule(() => {
    showAdNarration(
      "Your day. Optimized.",
      "Turns your messages, calendars, and commitments into a prioritized day.",
    );
  }, 3000);
  schedule(() => dayHeading.classList.add("visible"), 4500);
  schedule(() => importantCard.classList.add("visible"), 5500);
  schedule(() => {
    showPreparation(
      "Combining your calendars",
      ["Google Calendar · API", "Outlook Calendar · Chrome"],
      "Merging four calendars and checking conflicts before showing your schedule.",
    );
    showToolPreview("outlook", "Outlook Calendar");
  }, 7500);
  schedule(() => scheduleCard.classList.add("visible"), 8800);
  schedule(() => {
    cursor.setAttribute("class", "cursor to-stock-scroll scrolling");
  }, 9200);
  schedule(() => scrollHomeTo(scheduleCard), 9500);
  reportPreparationSteps.forEach(([start, title, routes, note], index) => {
    schedule(() => {
      showPreparation(title, routes, note);
      if (reportSourceActivities[index]) showSourceActivity(reportSourceActivities[index]);
      if (index === 2) {
        showToolPreview("market", "Terminal · investor-agent MCP");
        investmentSteps.slice(0, 4).forEach((step, stepIndex) => {
          schedule(() => {
            step.classList.add("visible");
            investmentOutput.scrollTo({ top: investmentOutput.scrollHeight, behavior: "smooth" });
          }, 250 + stepIndex * 350);
        });
      }
      if (index === 0) reportSections.classList.add("visible");
    }, start);
    schedule(() => reportSectionItems[index].classList.add("visible"), start + 1000);
    schedule(() => scrollHomeTo(reportSectionItems[index]), start + 1300);
  });
  schedule(() => {
    showPreparation(
      "Your briefing is ready",
      ["8 sources checked", "6 reports prepared"],
      "Every result is ready to open as a focused analysis.",
    );
  }, 23800);
  schedule(() => {
    cursor.classList.add("hidden");
    showAdNarration(
      "Knows your network.",
      "Understands who Marcus is and what this relationship requires.",
    );
    showPreparation(
      "Understanding your request",
      ["people-ops", "Network memory"],
      "Identifying who Marcus is before choosing a channel or drafting a reply.",
    );
    showToolPreview("network", "Personal network");
    assistantBody.classList.add("chat-transition");
    conversationWindow.classList.add("visible");
  }, 48000);
  schedule(typeChatRequest, 49000);
  schedule(() => {
    userRequestBubble.classList.add("visible");
    chatComposer.classList.add("submitted");
    chatInput.textContent = "";
    conversationScroll.scrollTo({ top: conversationScroll.scrollHeight, behavior: "smooth" });
  }, 52000);
  schedule(() => {
    showAdNarration(
      "Knows how to talk.",
      "Chooses the right channel, reads the context, and drafts in your established tone.",
    );
  }, 57500);
  conversationSteps.forEach((step, index) => {
    schedule(() => {
      if (index === 0) {
        showPreparation("Searching your network", ["people-ops", "Network memory"], "Finding Marcus and the relationship context that should shape the response.");
        showToolPreview("network", "Personal network");
      }
      if (index === 2) {
        showPreparation("Opening Google Chrome", ["Chrome · Work profile"], "Teams has no supported message API, so the agent starts your authenticated browser.");
        showToolPreview("chrome", "Google Chrome", "launch");
      }
      if (index === 3) {
        showPreparation("Reading the latest thread", ["Teams · Chrome", "Conversation history"], "Understanding the message, BenchPress context, and your established communication style.");
        showToolPreview("teams", "Microsoft Teams");
      }
      if (index === 4) {
        showPreparation("Drafting the reply", ["workplace-communication"], "Applying a concise, warm, proactive tone appropriate for your manager.");
      }
      step.classList.add("visible");
      conversationScroll.scrollTo({ top: conversationScroll.scrollHeight, behavior: "smooth" });
    }, conversationStepTimes[index]);
  });
  schedule(() => {
    showPreparation("Confirming your work login", ["Chrome · Signed in"], "Using the existing Microsoft work profile without asking you to log in again.");
    showToolPreview("chrome", "Google Chrome", "signed-in");
  }, 60000);
  schedule(() => {
    showPreparation("Navigating to Microsoft Teams", ["Chrome address bar"], "Typing the destination directly into the browser.");
    showToolPreview("chrome", "teams.microsoft.com", "address");
    typeTeamsAddress();
  }, 62200);
  schedule(() => {
    showPreparation("Opening Marcus's conversation", ["Teams · Chrome"], "The authenticated Teams workspace is ready, so the agent opens the latest thread.");
    showToolPreview("teams", "Microsoft Teams");
  }, 65000);
  schedule(() => {
    replyDraft.classList.add("visible");
    conversationScroll.scrollTo({ top: conversationScroll.scrollHeight, behavior: "smooth" });
  }, 72500);

  schedule(() => {
    stockDetailWindow.classList.remove("visible");
    assistantBody.classList.remove("stock-transition");
  }, 47000);
  schedule(() => scrollHomeTo(stockTrigger), 26000);
  schedule(() => {
    const target = stockTrigger.getBoundingClientRect();
    const surface = desktop.getBoundingClientRect();
    cursor.setAttribute("class", "cursor");
    cursor.style.left = `${((target.right - surface.left - 24) / surface.width) * 100}%`;
    cursor.style.top = `${((target.top + target.height / 2 - surface.top) / surface.height) * 100}%`;
  }, 26900);
  schedule(() => {
    cursor.classList.add("clicking");
    stockSection.classList.add("opening");
  }, 27700);
  schedule(() => {
    cursor.classList.remove("clicking");
    showAdNarration(
      "The market. Explored for you.",
      "Scans filings, news, prices, and emerging opportunities.",
    );
    showPreparation(
      "Screening today's market",
      ["6 news sweeps", "113 tickers", "SEC EDGAR"],
      "Reading every source first — nothing is recommended until the evidence is in.",
    );
    investmentSteps.forEach((step) => step.classList.remove("visible"));
    showToolPreview("market", "Terminal · investor-agent MCP");
    stockSection.classList.remove("opening");
    assistantBody.classList.add("stock-transition");
    stockDetailWindow.classList.add("visible");
  }, 28100);
  investmentSteps.forEach((step, index) => {
    schedule(() => {
      step.classList.add("visible");
      investmentOutput.scrollTo({ top: investmentOutput.scrollHeight, behavior: "smooth" });
    }, 28400 + index * 700);
  });
  schedule(() => cursor.classList.add("hidden"), 28350);
  schedule(() => {
    cursor.setAttribute("class", "cursor to-stock-scroll scrolling");
    cursor.style.left = "";
    cursor.style.top = "";
  }, 33900);
  schedule(() => {
    showAdNarration(
      "It reads everything first.",
      "Nine sectors, 113 tickers, every morning — before it forms an opinion.",
    );
    showPreparation(
      "Reading every ticker it tracks",
      ["9 sectors", "113 ticker files"],
      "No shortlist — it opens the whole universe before deciding anything.",
    );
    scrollDetailTo(scanRows[0]);
  }, 34000);
  scanRows.forEach((row, index) => {
    schedule(() => row.classList.add("visible"), 34400 + index * 200);
  });
  schedule(() => {
    showPreparation(
      "Narrowing with four questions",
      ["Bottleneck test", "Evidence test"],
      "Each filter has to be passed with a source, not a hunch.",
    );
    scrollDetailTo(gateRows[0]);
  }, 36900);
  gateRows.forEach((row, index) => {
    schedule(() => row.classList.add("visible"), 37400 + index * 750);
  });
  schedule(() => cursor.classList.add("hidden"), 40300);
  schedule(() => {
    showPreparation(
      "Pulling the primary document",
      ["SEC EDGAR", "Form 8-K"],
      "The only candidate left is checked against the filing itself.",
    );
    scrollDetailTo(memoryBlock);
  }, 40600);
  memoryReceipts.forEach((receipt, index) => {
    schedule(() => receipt.classList.add("visible"), 40900 + index * 1300);
  });
  schedule(() => {
    showAdNarration(
      "It will tell you to do nothing.",
      "113 screened, 0 recommended — with the evidence for it and against it.",
    );
    showPreparation("Writing today's verdict", ["Discipline rules", "Nothing invented"], "If nothing qualifies, it says so.");
    scrollDetailTo(closingAction);
  }, 44000);
  schedule(() => closingAction.classList.add("visible"), 44400);
  schedule(playAnimation, 80000);
}

playAnimation();
