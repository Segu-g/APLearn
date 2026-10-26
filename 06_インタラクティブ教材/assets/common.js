/* APLearn インタラクティブ教材 共通スクリプト
 * 使い方: <body data-root="../"> のように、index.html までの相対パスを data-root に書く。
 * <script src="(root)assets/common.js"></script> を body の末尾で読み込むとヘッダが入る。
 */
(function () {
  const STORE_PREFIX = "aplearn:";

  // localStorage はプライベートモード等で使えないことがあるので必ず try/catch で包む
  const store = {
    get(key, fallback) {
      try {
        const v = localStorage.getItem(STORE_PREFIX + key);
        return v === null ? fallback : JSON.parse(v);
      } catch (e) { return fallback; }
    },
    set(key, value) {
      try { localStorage.setItem(STORE_PREFIX + key, JSON.stringify(value)); } catch (e) { /* 保存できなくても動作は続ける */ }
    },
  };

  function applyTheme(theme) {
    if (theme === "light" || theme === "dark") document.documentElement.setAttribute("data-theme", theme);
    else document.documentElement.removeAttribute("data-theme");
  }

  function buildHeader() {
    const root = document.body.dataset.root || "./";
    const title = document.body.dataset.title || document.title;
    const header = document.createElement("header");
    header.className = "site-header";
    header.innerHTML =
      '<div class="inner">' +
      '<a class="brand" href="' + root + 'index.html">APLearn</a>' +
      '<span class="crumb"></span>' +
      '<span class="spacer"></span>' +
      '<button class="theme-toggle" type="button" aria-label="表示テーマを切り替え"></button>' +
      "</div>";
    header.querySelector(".crumb").textContent = title === "APLearn" ? "" : "› " + title;
    document.body.prepend(header);

    const btn = header.querySelector(".theme-toggle");
    const labels = { auto: "テーマ: 自動", light: "テーマ: ライト", dark: "テーマ: ダーク" };
    let theme = store.get("theme", "auto");
    applyTheme(theme);
    btn.textContent = labels[theme];
    btn.addEventListener("click", () => {
      theme = theme === "auto" ? "light" : theme === "light" ? "dark" : "auto";
      store.set("theme", theme);
      applyTheme(theme);
      btn.textContent = labels[theme];
    });
  }

  // 配列をシャッフルした新しい配列を返す
  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  // HTML エスケープ
  function esc(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  window.APL = { store, shuffle, esc };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", buildHeader);
  else buildHeader();
})();
