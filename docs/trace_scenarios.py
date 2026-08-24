# -*- coding: utf-8 -*-
"""One entry per figure. Rules: docs/figure-spec.md.

Every tree below was cut from a real `ls` of the config root, and every
annotation was written after reading the real file. Real names are `<name>/`.
"""
ELLIPSIS = "\u2026"


def d(name, kids=None, key=None):
    if isinstance(kids, str):
        raise TypeError("d(%r): kids must be a list; pass key as d(name, None, key)" % name)
    return (name, kids, key)


def f(name, key=None):
    return (name, None, key)


ELL = f(ELLIPSIS)


# ============================================================ 2.1  one email ==
EMAIL = {
 "id": "email",
 "replaces": "Routing map for a single email request",
 "aria": "File tree traced by a single email request",
 "prompt": "email my collaborator about the draft",
 "tree": [
   f("config.json"),
   f("copilot-instructions.md", "instr"),
   f("projects.md"),
   d("references/", [
     f("ai-mcp-skills-tips.md"),
     f("coupons.md"),
     d("personal/", [
       d("finance/"), d("identity_documents/"), d("living/"),
       d("network/", [
         d("family/"), d("friends/"),
         f("README.md", "netrd"),
         d("relationships/"),
         d("work/", [
           d("<name>/", [f("README.md", "person")]),
           ELL])]),
       ELL]),
     f("voice-typos.md")]),
   f("settings.json"),
   d("skills/", [
     d("account-ops/", [d("assets/"), f("SKILL.md", "acct")]),
     d("email-ops/", [
       d("assets/"), d("credentials/"),
       d("references/", [
         d("gmail/"), d("outlook/"), d("outreach/"),
         f("sender-routing.md", "send"), f("writing-guide.md", "write"), ELL]),
       f("SKILL.md", "eops")]),
     d("experiment-ops/"),
     d("negotiation/"),
     d("people-ops/", [f("SKILL.md", "pops")]),
     d("travel-ops/"),
     d("workplace-communication/", [
       d("references/", [
         f("difficult-conversations.md"), f("recipient-guide.md", "recip"),
         f("reddit-boss-communication.md"), f("reorg-analysis.md"), ELL]),
       f("SKILL.md", "wcskill")]),
     ELL]),
   f("vault.json", "vault"),
   ELL,
 ],
 "steps": [
  ("instr", "eops",
   "This is the one file that is always read first, before anything else happens. Most "
   "of it is a routing table: a list of situations on the left, and for each one the "
   "module that handles it on the right. One row says that anything to do with reading, "
   "writing, searching or sending email is handled by email-ops. This is an email, so "
   "that row matches and nothing else in the file matters right now."),
  ("eops", "send",
   "email-ops/SKILL.md is the how-to for email: reading, searching, drafting, attaching "
   "files, actually sending. It is written as a decision tree. One branch says that "
   "before an email can go out, it has to be decided which of my accounts it comes from "
   "&#8212; and that this file does not decide it. It points at sender-routing.md."),
  ("send", "acct",
   "sender-routing.md is a short table of my email accounts and what each one is for: "
   "work mail from the work account, academic mail from the academic one, sign-ups and "
   "shopping from a throwaway. There is also a rule that if a thread with this person "
   "already exists, keep replying from whatever account it started on. A work "
   "collaborator lands on the work account. That settles the address &#8212; not the "
   "login for it."),
  ("acct", "vault",
   "account-ops/SKILL.md is the rulebook for accounts and logins, and its first rule is "
   "that no password is ever written into a skill file, a note, or a scratch file. "
   "Every credential in the whole system lives in one encrypted store. This file only "
   "explains how to read from that store and how to add to it, so the login for the "
   "work account gets fetched from there."),
  ("vault", "pops",
   "Everything needed to send is now in hand. What is still missing is the person it "
   "goes to. The instruction file has a rule for that as well: the moment a human being "
   "is mentioned, even in passing, people-ops gets consulted before anything is done "
   "with them &#8212; so a name is never treated as a stranger by mistake."),
  ("pops", "netrd",
   "people-ops/SKILL.md is the rulebook for anything involving a person: whether this "
   "person already has a file, where to look them up, what to write down afterwards, "
   "where their attachments go. It holds no information about anybody &#8212; only "
   "rules. The rule that applies here is the lookup one, and it says the index of "
   "everyone lives at references/personal/network/README.md."),
  ("netrd", "person",
   "network/README.md is that index: one table, one line per person, with their "
   "relationship to me, a one-sentence description, and the folder where the rest of "
   "them is kept. People are grouped by how I know them &#8212; work, friends, family. "
   "The collaborator is in the work group, and their line points at their own folder."),
  ("person", "wcskill",
   "Their folder is where the actual detail lives: email address, role, what they are "
   "working on, and notes from everything we have exchanged before. What is not in "
   "there is how to talk to them. That is on purpose &#8212; tone follows the working "
   "relationship, not the individual, and a separate module owns it."),
  ("wcskill", "recip",
   "workplace-communication/SKILL.md covers anything that touches a work relationship: "
   "raising a problem with a manager, disagreeing with a peer, reading a reorg "
   "announcement. It is a decision tree too, and the branch for an ordinary message "
   "says to work out who is receiving it first, then read references/recipient-guide.md."),
  ("recip", "write",
   "recipient-guide.md is a tone table: one row per kind of recipient &#8212; manager, "
   "skip-level, a teammate I am close to, an ordinary colleague, a professor or someone "
   "outside the company &#8212; and for each one how to open, how to sign off, how "
   "formal to be. That fixes what the email should sound like. It does not fix the "
   "mechanics, which is what the email writing guide is for: it knows the mail client "
   "inserts my signature by itself, so no sign-off is ever typed by hand."),
 ],
 "caption":
   "One email, and the eleven files it opens, in the order it opens them. Hover a "
   "numbered step to see which two files it connects and why that edge exists. Nothing "
   "here is found by searching: every file is named by the one before it. A grey "
   "&#8230; means the folder holds more than the figure shows.",
}




# ========================================================= 2.2  one flight ==
FLIGHT = {
 "id": "flight",
 "replaces": "Routing map for booking a flight",
 "aria": "File tree traced by a flight booking",
 "prompt": "book me a flight to the conference",
 "tree": [
   f("copilot-instructions.md", "instr"),
   d("references/", [
     f("ai-mcp-skills-tips.md"),
     f("coupons.md"),
     d("personal/", [
       d("finance/", [
         f("payment.gpg"), f("payment.README.md"),
         f("README.md", "fin"), ELL]),
       d("identity_documents/", [
         f("passport.pdf", "pass"), f("signature.png"), f("visa.pdf"), ELL]),
       d("living/"),
       d("network/"),
       d("travel/", [
         f("packing.md"),
         f("README.md", "trd"),
         d("trips/", [
           d("<date>-<trip>/", [f("README.md", "trip")]),
           f("README.md")])]),
       ELL]),
     f("voice-typos.md")]),
   d("skills/", [
     d("account-ops/", [d("assets/"), f("SKILL.md", "acct")]),
     d("email-ops/"),
     d("negotiation/"),
     d("people-ops/"),
     d("purchase-ops/", [f("SKILL.md", "purch")]),
     d("travel-ops/", [
       d("flights/", [
         f("money-saving.md", "money"), f("output.md"), f("README.md", "fread")]),
       f("manage-reservation.md"), f("packing.md"), d("parents/"),
       f("SKILL.md", "tops")]),
     ELL]),
   f("vault.json"),
   ELL,
 ],
 "steps": [
  ("instr", "tops",
   "The instruction file is read first every time. Its routing table has named rows for "
   "email, calendar, code and a few other things &#8212; but there is no row for travel. "
   "What catches this request is the very first row, which says that if any module "
   "declares it handles this kind of request, that module is opened and followed, and "
   "working from memory instead is not allowed. travel-ops declares flights, airfare and "
   "booking as its own."),
  ("tops", "fread",
   "travel-ops/SKILL.md is twenty-six lines and holds no facts at all. It opens by "
   "stating that anything specific to me &#8212; my accounts, my documents, my money "
   "&#8212; belongs in my personal files and must never be written into this module. "
   "The rest is five branches by request type. Flight search, award tickets and booking "
   "all go to one procedure file."),
  ("fread", "money",
   "flights/README.md is the actual search procedure, in five numbered steps: work out "
   "the search parameters, search live inventory, compare, gate on confirmation, write "
   "the result down. It also carries an odd-looking rule &#8212; if the destination is "
   "not a hub, check airports within a hundred and fifty miles too. Step two says to run "
   "the points side of the search at the same time as the cash side."),
  ("money", "trd",
   "money-saving.md is the points-versus-cash comparison, and it has an actual formula "
   "in it: what a point is worth in this particular redemption, with thresholds for when "
   "paying with points is clearly worth it and when it is not. Its first step is to load "
   "the facts it needs, and it is explicit that those facts are not stored here &#8212; "
   "it also forbids guessing a balance from an old snapshot."),
  ("trd", "fin",
   "travel/README.md is my own travel file, and most of it is one table headed "
   "&#8220;single source of truth&#8221;: one row per kind of travel fact, and the one "
   "place that fact is allowed to live. Card benefits and points rules are one of those "
   "rows, and they point out of travel entirely, into the finance folder."),
  ("trd", "acct",
   "Another row in the same table covers airline and hotel membership numbers, logins "
   "and two-factor. Those are not travel facts, they are account facts, so the row "
   "points at the accounts module rather than keeping a copy here. This is the rule that "
   "stops my frequent-flyer number existing in three files that disagree."),
  ("trd", "pass",
   "A third row covers my own passport and travel documents. Note that it is my own "
   "&#8212; the row directly under it says that anyone else&#8217;s documents live in "
   "that person&#8217;s own folder, not in mine. Booking a flight for someone else "
   "therefore reads from their file, and nothing has to be copied across."),
  ("fread", "purch",
   "Back in the search procedure, step four is a gate rather than an action. Anything "
   "that spends money hands over to the purchases module, which requires the exact "
   "itinerary, traveller and total to be shown and confirmed first. Paying with points "
   "and buying the ticket are two separate confirmations, not one."),
  ("purch", "trip",
   "Once it is booked, the module&#8217;s closing check says to write exactly one record "
   "&#8212; one folder per trip, named by date, holding the itinerary and a row per "
   "traveller with their own booking reference, seat, fare and payment. Exactly one is "
   "the point. Calendar entries are generated from this record and are not a second copy "
   "of it."),
 ],
 "caption":
   "Booking a flight. The travel module holds the procedure and none of the facts &#8212; "
   "it says so in its own first line. My travel file carries a table of where each kind "
   "of fact is allowed to live, and three of the steps above are simply that table being "
   "obeyed. The booking is written back to one place.",
}


# ==================================================== 2.3  second experiment ==
EXPERIMENT = {
 "id": "experiment",
 "replaces": "Routing map for reusing an evaluation",
 "aria": "File tree traced by a second experiment",
 "prompt": "now implement the second experiment",
 "tree": [
   f("config.json"),
   f("copilot-instructions.md", "instr"),
   f("projects.md"),
   d("references/"),
   f("settings.json"),
   d("skills/", [
     d("browser/"),
     d("code-writing/", [
       d("references/", [
         f("bugfix.md"), f("code-architecture.md", "arch")]),
       f("SKILL.md", "cw")]),
     d("email-ops/"),
     d("env-control/"),
     d("experiment-ops/", [
       d("assets/"),
       d("references/", [
         f("experiment.md", "rep"), f("testing.md", "test")]),
       f("SKILL.md", "exp")]),
     ELL]),
   f("vault.json"),
   ELL,
 ],
 "steps": [
  ("instr", "exp",
   "Same first row as always: a module that declares this kind of work gets opened and "
   "followed. experiment-ops declares running experiments, submitting jobs and "
   "evaluation. The instruction file also carries a hard rule a few lines below &#8212; "
   "experiments never run on this laptop &#8212; which is why the module, not the model, "
   "decides what happens next."),
  ("exp", "cw",
   "experiment-ops/SKILL.md is a seven-step pipeline, and the interesting part is what "
   "it refuses to do. Its very first step says that if the request is really a code "
   "change, placement question or bug, hand over to the code module and stop. Writing "
   "the second experiment is a code change, so it hands over &#8212; and says to come "
   "back here to actually run it."),
  ("cw", "arch",
   "code-writing/SKILL.md is the rulebook for touching any code at all. It insists on "
   "settling what a function is for before editing it, and it defaults to writing code "
   "inline &#8212; no new helper, class or file unless there are genuinely two callers "
   "already. For where the code should live, it points at its architecture file."),
  ("arch", "exp",
   "The architecture file is the one that prevents the rewrite. Behaviour belongs to "
   "whichever component already owns that meaning; tests import the real implementation "
   "rather than carrying their own copy; a typo gets fixed at the source instead of "
   "getting a compatibility shim. So the metric from the first experiment is imported, "
   "not written again. Then control returns to the experiment module to run it."),
  ("exp", "test",
   "Before a full run, the experiment module requires a smoke test, and its testing file "
   "is what that means concretely: can the job resume if it dies, do the imports "
   "resolve, are the data paths real, does one single sample get all the way through. "
   "There is a fix-and-recheck loop at the end &#8212; a fix is not done until it has "
   "been verified."),
  ("exp", "rep",
   "The last file is about writing the result down. It fixes what has to be agreed "
   "before a run &#8212; data, model, evaluation, hyperparameters, baseline, cost "
   "&#8212; and the shape of the report after: conclusion first, the full setting "
   "restated, tables rather than prose, metrics explained before the numbers appear. It "
   "ends with the exact format the result is logged in, so the next experiment can find "
   "it."),
 ],
 "caption":
   "The second experiment. The rule that stops the metric being written twice is not in "
   "the experiment module at all &#8212; it is in the code module&#8217;s architecture "
   "file, and it runs before any code is written. The experiment module deliberately "
   "hands over and asks for control back.",
}


# ========================================================== 2.4  save an idea ==
IDEA = {
 "id": "idea",
 "replaces": "Routing map for saving an idea",
 "aria": "File tree traced by saving an idea",
 "prompt": "save this idea for later",
 "tree": [
   f("config.json"),
   f("copilot-instructions.md", "instr"),
   f("projects.md", "proj"),
   d("references/"),
   f("settings.json"),
   d("skills/", [
     d("browser/"),
     d("email-ops/"),
     d("people-ops/"),
     d("system-maintenance/", [
       f("audit-checklist.md"),
       f("file-directory.md", "fdir"),
       f("persist.md", "persist"),
       f("register-project.md"),
       f("SKILL.md", "sm"),
       ELL]),
     ELL]),
   f("vault.json"),
   ELL,
 ],
 "steps": [
  ("instr", "sm",
   "This one does have its own row in the routing table, and the row is unusually "
   "specific: creating, downloading, saving, finding or uploading a file all go to the "
   "maintenance module, and the row even names the file to read once you get there. So "
   "the assistant is not allowed to pick a folder on instinct."),
  ("sm", "fdir",
   "system-maintenance/SKILL.md is the module that owns everything the system does to "
   "itself. Its file branch is two lines long and both are order-of-operations: read the "
   "directory file before choosing any path, and if the path is on a remote machine, "
   "hand off to the environment module instead."),
  ("fdir", "persist",
   "file-directory.md is a decision tree of eight questions &#8212; is this a "
   "credential, does it belong to a project, is it long-term personal information, is it "
   "about someone else, and so on &#8212; followed by a table of about twenty-five kinds "
   "of thing and the single path each one is allowed to live at. Its stated invariant is "
   "that every durable fact has exactly one owner, and the first branch that matches is "
   "the answer. Anywhere else may hold a pointer, never a second copy."),
  ("fdir", "proj",
   "For an idea, the tree lands on the project branch, and the destination is a folder "
   "inside a real project rather than anywhere under the assistant&#8217;s own "
   "configuration. projects.md is the registry that turns a project name into its actual "
   "path on disk, which is how the idea ends up somewhere I would look for it, rather "
   "than somewhere only the assistant knows about."),
  ("persist", "fdir",
   "persist.md is the other half of the rule, and it is the half that is easy to skip. "
   "Writing the file is not enough: unless something already in the system points at it, "
   "nothing will ever open it again. So a pointer gets written too &#8212; and the "
   "directory file itself carries a line at the top saying to update it after every "
   "single file added, moved or deleted, which is what stops the map drifting from the "
   "territory."),
 ],
 "caption":
   "Saving an idea. One module owns every file that gets created, and it produces two "
   "things, not one: the file, and a pointer that makes the file reachable. A file "
   "nothing points at is the same as a file that does not exist.",
}


# ====================================================== 2.5  a gift for others ==
GIFT = {
 "id": "gift",
 "replaces": "Routing map for a purchase made for someone else",
 "aria": "File tree traced by a purchase made for someone else",
 "prompt": "which air fryer should I get my parents",
 "tree": [
   f("copilot-instructions.md", "instr"),
   d("references/", [
     f("ai-mcp-skills-tips.md"),
     f("coupons.md"),
     d("personal/", [
       d("finance/"),
       d("living/"),
       d("network/", [
         d("family/", [
           d("dad/", [d("documents/"), f("README.md", "dad")]),
           d("mom/", [d("documents/"), f("README.md", "mom")])]),
         d("friends/"),
         f("README.md", "netrd"),
         d("relationships/"),
         d("work/")]),
       d("travel/"),
       ELL]),
     f("voice-typos.md")]),
   d("skills/", [
     d("email-ops/"),
     d("negotiation/"),
     d("people-ops/", [f("SKILL.md", "pops")]),
     d("purchase-ops/", [f("SKILL.md", "purch")]),
     d("travel-ops/"),
     ELL]),
   f("vault.json"),
   ELL,
 ],
 "steps": [
  ("instr", "purch",
   "Buying something has no named row either, so it is the general rule that fires: the "
   "purchases module declares checkout and ordering as its own, so it gets opened. That "
   "module turns out to be purely transactional &#8212; classify the transaction, set up "
   "the account and payment, confirm the exact total before submitting, verify "
   "afterwards. It never asks who the thing is for."),
  ("instr", "pops",
   "A second row in the same table fires at the same time, and this is the one that "
   "matters here. It says that if a human being is mentioned at all &#8212; even in "
   "passing, even as one word in a longer sentence &#8212; the people module is "
   "consulted before anything is answered, so that a familiar name is never handled as "
   "though it were a stranger. &#8220;My parents&#8221; is enough to trigger it."),
  ("pops", "netrd",
   "people-ops/SKILL.md holds no information about anybody. It is the rulebook: does "
   "this person already have a file, where to look them up, what to write down "
   "afterwards, where their attachments go. Its lookup rule names the index of everyone "
   "I know."),
  ("netrd", "mom",
   "network/README.md is that index, and the structure it enforces is that everybody "
   "gets their own folder, grouped by how I know them. It also has a rule about growth: "
   "a new name mentioned in conversation gets a row immediately, and once there are two "
   "or more facts about them, the row is promoted to a folder. Nothing here is entered "
   "by hand as a chore."),
  ("netrd", "dad",
   "Both parents have their own folder, and each folder is where facts about that person "
   "live &#8212; what they already own, what they have said they wanted, what has "
   "already been bought for them. Because the facts are filed under the person rather "
   "than under the kind of object, the answer is about their kitchen and not about "
   "kitchens in general."),
 ],
 "caption":
   "An air fryer for my parents. Look at what stays dark: <code>living/</code> is my own "
   "apartment, and it is exactly the file that would produce a confident answer about the "
   "wrong kitchen. Because facts are filed by who they are about, no edge leads there. It "
   "is never opened, so it never has to be ranked or ignored.",
}


# ========================================================= 2.6  a passing fact ==
DEADLINE = {
 "id": "deadline",
 "replaces": "Where an incoming fact is stored",
 "aria": "File tree traced by something I tell the assistant",
 "prompt": "the form is due at the end of the month",
 "tree": [
   f("copilot-instructions.md", "instr"),
   d("references/", [
     f("ai-mcp-skills-tips.md"),
     f("coupons.md"),
     d("personal/", [
       d("finance/"),
       d("identity_documents/", None, "docs"),
       d("living/"),
       d("network/"),
       f("README.md"),
       f("reminders.json", "rem"),
       ELL]),
     f("voice-typos.md")]),
   d("skills/", [
     d("email-ops/"),
     d("people-ops/"),
     d("reporting-ops/", [
       d("assets/", [
         f("crawl-emails.md"), f("get-calendar.md"),
         f("manage-reminders.md", "mrem"), ELL]),
       d("references/"), f("SKILL.md", "rops"), ELL]),
     d("system-maintenance/", [
       f("file-directory.md", "fdir"), f("persist.md"),
       f("SKILL.md", "sm"), ELL]),
     d("travel-ops/"),
     ELL]),
   f("vault.json"),
   ELL,
 ],
 "steps": [
  ("instr", "rops",
   "The routing table has a row for reminders, and it points at the reporting module. "
   "The row carries an instruction as well as a destination: if I ever say to drop "
   "something, its status is changed straight away rather than quietly left alone. A "
   "reminder is not just a note, it is a thing with a state."),
  ("rops", "mrem",
   "reporting-ops/SKILL.md is the module that produces the daily and weekly briefings, "
   "and it does not decide anything about reminders itself &#8212; it delegates that to "
   "one file so the same rules apply whether a reminder arrives in conversation, in "
   "email, or in a briefing."),
  ("mrem", "rem",
   "manage-reminders.md is where the interesting rule lives. Reminders come in kinds: "
   "ongoing ones that always show, dated ones that stay silent until a chosen date "
   "arrives, and yearly ones. So a deadline does not need me to remember it and does not "
   "clutter anything before it is relevant. Finished ones stay on record rather than "
   "being deleted, and an ongoing one with no end date that has sat untouched for three "
   "months gets flagged to be confirmed &#8212; which is how stale things surface "
   "instead of quietly rotting."),
  ("instr", "sm",
   "Not everything I say is time-boxed. Facts that stay true until I change them take "
   "the other row &#8212; the one for saving files &#8212; and that goes to the "
   "maintenance module, which again names the exact file to read before choosing a "
   "location."),
  ("sm", "fdir",
   "file-directory.md is where the durability question is actually answered. It has an "
   "explicit rule that the session&#8217;s scratch folder is not storage: debugging "
   "output and one-off caches may live there, but anything that could be needed later "
   "&#8212; evidence, a receipt, a confirmation, a decision &#8212; has to be moved to a "
   "real home with a pointer left behind. The test is whether a future session would "
   "ever need to see it."),
  ("fdir", "docs",
   "And there is a third answer, which is not to store it. Some rows in the table are "
   "marked never keep a copy &#8212; download the current one when it is needed. Those "
   "are the facts a government office or an employer can change without telling me, so a "
   "saved copy is not memory, it is a stale claim. Choosing not to store something is a "
   "storage decision like any other."),
 ],
 "caption":
   "Where something I say ends up. Three destinations, chosen by how long it stays true: "
   "a dated reminder that stays quiet until its date, a durable file with one canonical "
   "home, or nothing at all. The third is deliberate &#8212; for facts whose real source "
   "can change without telling me, a copy would be worse than no copy.",
}


# ======================================================== 2.7  a rent increase ==
RENT = {
 "id": "rent",
 "replaces": "Routing map for a negotiation question",
 "aria": "File tree traced by a negotiation question",
 "prompt": "how do I push back on the rent increase",
 "tree": [
   f("config.json"),
   f("copilot-instructions.md", "instr"),
   f("projects.md"),
   d("references/"),
   f("settings.json"),
   d("skills/", [
     d("email-ops/"),
     d("negotiation/", [
       d("references/", [
         f("anti-patterns.md", "anti"),
         d("books/", [
           d("getting-to-yes/"),
           d("influence/"),
           d("never-split-the-difference/", [
             d("chapters/", None, "chap"), f("index.md"), f("source.epub")])]),
         f("framework.md", "fw"),
         f("rent.md", "rent"),
         f("salary.md")]),
       f("SKILL.md", "neg")]),
     d("people-ops/"),
     d("purchase-ops/"),
     ELL]),
   f("vault.json"),
   ELL,
 ],
 "steps": [
  ("instr", "neg",
   "No named row for this one either &#8212; the general rule catches it, because the "
   "negotiation module declares haggling, counter-offers, lease renewals and salary "
   "talks as its own. The same rule adds that having a module for something means it "
   "gets read, not recalled: the assistant is not allowed to answer from a general sense "
   "of how negotiation works."),
  ("neg", "rent",
   "negotiation/SKILL.md is about twenty-five lines. It sorts the request into a "
   "situation &#8212; a lease, a salary, or something else &#8212; and a lease sends it "
   "to rent.md. Note the word it uses: supplementary. The situation file adds to the "
   "process, it does not replace it."),
  ("rent", "fw",
   "rent.md is specific in a way general advice never is: pull comparable listings and "
   "the vacancy rate in this building&#8217;s area, then take inventory of the leverage "
   "I actually have &#8212; payment history, flexibility on dates, what it would cost "
   "them to turn the unit over. Then write to the property manager, not a general "
   "inbox, in under a hundred and twenty words. It has a template with blanks, and a "
   "rule that the blanks must be filled with real numbers before anything is sent."),
  ("fw", "chap",
   "framework.md is the part every negotiation goes through regardless of what is being "
   "negotiated: prepare, open, explore, propose, close. What makes it more than a list "
   "of slogans is that each tactic carries a citation to a specific chapter of a "
   "specific book sitting in this folder, split into chapters. So a tactic can be opened "
   "and checked instead of taken on faith, and only the cited chapter gets read."),
  ("neg", "anti",
   "The final step is a check, not an answer. anti-patterns.md is ten specific ways a "
   "draft gives away its own position: offering several fallbacks at once, revealing the "
   "floor, sounding too keen to stay, apologising into weakness, running long, naming a "
   "round number, filling one&#8217;s own silence. The module states that this step is "
   "not optional and loops &#8212; all ten have to pass, and any failure means rewrite "
   "and check again."),
 ],
 "caption":
   "A negotiation question. The route ends in a check rather than an answer: the draft is "
   "tested against a list of known bad moves and rewritten until it passes. The advice "
   "underneath is not the assistant&#8217;s own &#8212; every tactic in the framework "
   "cites the chapter it came from, and those chapters are sitting in the tree.",
}


SCENARIOS = [EMAIL, FLIGHT, EXPERIMENT, IDEA, GIFT, DEADLINE, RENT]
