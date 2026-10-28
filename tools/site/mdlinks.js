// 公開サイトでは Markdown が HTML に変換されているので、JS で組み立てた「X.md」へのリンクを「X.html」に読み替える。
(function () {
  function fix(a) {
    var href = a.getAttribute("href");
    if (!href || /^([a-z][a-z0-9+.-]*:|\/\/|#)/i.test(href)) return;
    var m = href.match(/^([^#?]*)\.md([?#].*)?$/);
    if (m) a.setAttribute("href", m[1] + ".html" + (m[2] || ""));
  }
  ["pointerdown", "focusin", "click"].forEach(function (ev) {
    document.addEventListener(ev, function (e) {
      var a = e.target.closest && e.target.closest("a[href]");
      if (a) fix(a);
    }, true);
  });
})();
