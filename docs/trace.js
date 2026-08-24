/* Hover interaction for the trace figures. See docs/figure-spec.md, section 4. */
(function () {
  var esc = function (t) {
    return t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  };

  Array.prototype.forEach.call(document.querySelectorAll(".trace"), function (fig) {
    var tip = fig.querySelector(".trace-tip");
    var hops = Array.prototype.slice.call(fig.querySelectorAll(".thop"));
    var rows = Array.prototype.slice.call(fig.querySelectorAll(".trow"));
    if (!tip || !hops.length) return;

    var clear = function () {
      hops.forEach(function (h) { h.classList.remove("dim", "on"); });
      rows.forEach(function (r) { r.classList.remove("on", "end"); });
      tip.classList.remove("show");
    };

    var show = function (hop) {
      hops.forEach(function (o) { o.classList.toggle("dim", o !== hop); });
      hop.classList.add("on");

      var want = hop.getAttribute("data-rows").split(",");
      var ends = hop.getAttribute("data-ends").split(",");
      rows.forEach(function (r) {
        var i = r.getAttribute("data-row");
        r.classList.toggle("on", want.indexOf(i) !== -1);
        r.classList.toggle("end", ends.indexOf(i) !== -1);
      });

      tip.innerHTML =
        '<div class="hd"><span class="n">' + hop.getAttribute("data-step") +
        "</span>" + esc(hop.getAttribute("data-src")) +
        ' <span class="ar">&#8594;</span> ' + esc(hop.getAttribute("data-dst")) +
        '</div><div class="why">' + hop.getAttribute("data-why") + "</div>";
      tip.classList.add("show");

      // The tooltip sits to the right of the step number and is allowed to spill
      // past the figure's own edge into the page margin. It is never flipped back
      // over the tree; when the viewport runs out it stops at the right edge.
      var b = hop.querySelector(".tbadge").getBoundingClientRect();
      var c = fig.getBoundingClientRect();
      var t = tip.getBoundingClientRect();
      var PAD = 14;
      var edge = document.documentElement.clientWidth - 16;
      var x = b.right + PAD;
      if (x + t.width > edge) x = edge - t.width;
      if (x < 16) x = 16;
      var y = b.top + b.height / 2 - t.height / 2;
      y = Math.max(c.top + PAD, Math.min(y, c.bottom - PAD - t.height));
      tip.style.left = Math.round(x - c.left) + "px";
      tip.style.top = Math.round(y - c.top) + "px";
    };

    hops.forEach(function (hop) {
      hop.addEventListener("mouseenter", function () { show(hop); });
      hop.addEventListener("mouseleave", clear);
      hop.addEventListener("focus", function () { show(hop); });
      hop.addEventListener("blur", clear);
      hop.setAttribute("tabindex", "0");
    });
  });
})();
