/* APLearn サイト内検索（build_site.py が作る _site_assets/search/*.json を読む）
 *
 * - インデックスは見出しごとの [ページ番号, アンカー, 見出し, 本文]。用語集は1語ずつ
 * - 比較は「小文字化＋カタカナをひらがなに」した文字列で行う（本文は生成時に NFKC 済み。
 *   どちらの変換も文字数が変わらないので、見つけた位置をそのまま元の本文の抜粋に使える）
 * - スペース区切りは AND。見出しに含まれる語ほど上に並べる
 */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var BASE = "./_site_assets/search/";
  var PAGE_SIZE = 30;
  var shards = [];          // [{name, label, pages, items, norm: [[見出し, 本文, ページ名]]}]
  var enabled = {};         // 範囲 name → true/false
  var shown = PAGE_SIZE, lastHits = [], timer = null;

  function fold(s) {
    return s.normalize("NFKC").toLowerCase().replace(/[ァ-ヶ]/g, function (c) {
      return String.fromCharCode(c.charCodeAt(0) - 0x60);
    });
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function terms(q) { return fold(q).split(/\s+/).filter(Boolean); }

  // 抜粋：最初に見つかった語の前後を切り出し、すべての語を <mark> で囲む
  function snippet(text, ntext, ts) {
    var first = -1;
    ts.forEach(function (t) { var i = ntext.indexOf(t); if (i >= 0 && (first < 0 || i < first)) first = i; });
    var start = Math.max(0, first < 0 ? 0 : first - 40), end = Math.min(text.length, start + 140);
    // 絵文字など（サロゲートペア）の途中で切らない
    if (start > 0 && /[\udc00-\udfff]/.test(text.charAt(start))) start -= 1;
    if (end < text.length && /[\ud800-\udbff]/.test(text.charAt(end - 1))) end += 1;
    var ranges = [];
    ts.forEach(function (t) {
      var i = ntext.indexOf(t, start);
      while (i >= 0 && i < end) { ranges.push([i, Math.min(i + t.length, end)]); i = ntext.indexOf(t, i + t.length); }
    });
    ranges.sort(function (a, b) { return a[0] - b[0]; });
    var out = start > 0 ? "…" : "", pos = start;
    ranges.forEach(function (r) {
      if (r[0] < pos) return;
      out += esc(text.slice(pos, r[0])) + "<mark>" + esc(text.slice(r[0], r[1])) + "</mark>";
      pos = r[1];
    });
    return out + esc(text.slice(pos, end)) + (end < text.length ? "…" : "");
  }
  function mark(text, ts) {
    var n = fold(text), out = "", pos = 0, i, best, bt;
    for (;;) {
      best = -1; bt = "";
      ts.forEach(function (t) { var j = n.indexOf(t, pos); if (j >= 0 && (best < 0 || j < best)) { best = j; bt = t; } });
      if (best < 0) break;
      out += esc(text.slice(pos, best)) + "<mark>" + esc(text.slice(best, best + bt.length)) + "</mark>";
      pos = best + bt.length;
    }
    return out + esc(text.slice(pos));
  }

  function search(q) {
    var ts = terms(q), hits = [];
    if (!ts.length) return hits;
    var wordRe = ts.map(function (t) {
      return /^[a-z0-9]+$/.test(t) ? new RegExp("(^|[^a-z0-9])" + t + "($|[^a-z0-9])") : null;
    });
    shards.forEach(function (sh) {
      if (!enabled[sh.name]) return;
      for (var k = 0; k < sh.items.length; k++) {
        var nn = sh.norm[k], score = 0, ok = true;
        for (var j = 0; j < ts.length; j++) {
          var t = ts[j], inHead = nn[0].indexOf(t) >= 0, inBody = nn[1].indexOf(t) >= 0, inPage = nn[2].indexOf(t) >= 0;
          if (!inHead && !inBody && !inPage) { ok = false; break; }
          var w = wordRe[j];  // 英数字の語は、前後が英数字でない「単語としての一致」を優先（RTO で RTOS を上にしない）
          var headWord = inHead && (!w || w.test(nn[0])), bodyWord = inBody && (!w || w.test(nn[1]));
          score += (nn[0] === t ? 60 : 0) + (headWord ? 25 : inHead ? 4 : 0) + (inPage ? 5 : 0) + (bodyWord ? 3 : inBody ? 1 : 0);
          if (headWord && nn[0].indexOf(t) === 0) score += 20;  // 見出しが検索語で始まる（用語集の「RTO（目標復旧時間）」など）
          if (w && !headWord && !bodyWord) score -= 40;  // 英数字の語が、別の語の一部（RTOS、IPv6 など）としてしか出てこない
        }
        if (ok) hits.push({ sh: sh, k: k, score: score - Math.min(nn[1].length, 4000) / 4000 });
      }
    });
    hits.sort(function (a, b) { return b.score - a.score; });
    return hits;
  }

  function render() {
    var q = $("search-q").value, ts = terms(q), list = $("search-results");
    var loaded = shards.length, total = Object.keys(enabled).length;
    if (!ts.length) {
      list.innerHTML = ""; $("search-more").hidden = true;
      $("search-status").textContent = loaded < total ? "検索の準備をしています…（" + loaded + " / " + total + "）" : "検索語を入力してください。";
      return;
    }
    var hits = lastHits;
    $("search-status").textContent = hits.length + " 件" + (loaded < total ? "（読み込み中の範囲があります）" : "");
    list.innerHTML = hits.slice(0, shown).map(function (h) {
      var it = h.sh.items[h.k], pg = h.sh.pages[it[0]];
      var url = "./" + pg[0] + (it[1] ? "#" + encodeURIComponent(it[1]) : "");
      var head = it[2] && it[2] !== pg[1] ? mark(it[2], ts) : "";
      return '<li><a href="' + esc(url) + '"><span class="sr-page">' + esc(h.sh.label) + " ／ " + mark(pg[1], ts) + "</span>" +
        (head ? '<span class="sr-head">' + head + "</span>" : "") + "</a>" +
        '<span class="sr-text">' + snippet(it[3], h.sh.norm[h.k][1], ts) + "</span></li>";
    }).join("");
    $("search-more").hidden = hits.length <= shown;
  }
  function run() {
    shown = PAGE_SIZE;
    lastHits = search($("search-q").value);
    render();
    var q = $("search-q").value.trim();
    try { history.replaceState(null, "", q ? "?q=" + encodeURIComponent(q) : location.pathname); } catch (e) { /* file:// など */ }
  }

  function areaButtons() {
    $("search-areas").innerHTML = Object.keys(enabled).map(function (name) {
      var lab = (shardLabels[name] || name);
      return '<label><input type="checkbox" data-area="' + esc(name) + '"' + (enabled[name] ? " checked" : "") + "> " + esc(lab) + "</label>";
    }).join("");
  }
  var shardLabels = {};

  function load() {
    fetch(BASE + "shards.json").then(function (r) { return r.json(); }).then(function (list) {
      list.forEach(function (s) { enabled[s[0]] = true; shardLabels[s[0]] = s[1]; });
      areaButtons();
      render();
      list.forEach(function (s) {
        fetch(BASE + s[0] + ".json").then(function (r) { return r.json(); }).then(function (d) {
          var pnorm = d.pages.map(function (p) { return fold(p[1]); });
          d.name = s[0];
          d.norm = d.items.map(function (it) { return [fold(it[2]), fold(it[3]), pnorm[it[0]]]; });
          shards.push(d);
          run();
        }).catch(function () { $("search-status").textContent = "検索データの読み込みに失敗しました（" + s[1] + "）。"; });
      });
    }).catch(function () {
      $("search-status").textContent = "検索データを読み込めませんでした。Web 版（https://segu-g.github.io/APLearn/）か、ローカルの http サーバーで開いてください。";
    });
  }

  $("search-q").addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(run, 150); });
  $("search-more").addEventListener("click", function () { shown += PAGE_SIZE; render(); });
  $("search-areas").addEventListener("change", function (e) {
    var a = e.target.getAttribute("data-area");
    if (a) { enabled[a] = e.target.checked; run(); }
  });
  var q0 = new URLSearchParams(location.search).get("q");
  if (q0) $("search-q").value = q0;
  $("search-q").focus();
  load();
})();
