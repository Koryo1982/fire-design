/* =====================================================================
 * config.js — father cafe SSOT (Single Source of Truth)
 * 管理者の公開データ・サイト定数・共通ナビ/フッターのレンダリング。
 * 依存なし。window.SiteConfig / window.SiteUI を公開する。
 * 読者のパーソナルデータは保持しない（それは localStorage / FireStore の役割）。
 * ===================================================================== */
(function (global) {
  "use strict";

  var BASE = "/fire-design";

  /* ---------- 管理者の公開データ（SSOT） ----------
   * 月次更新時はこのファイルだけ編集すれば全ページが追従する。
   * 1. finance / updatedAt / report を更新
   * 2. 新しい月次レポート Markdown を financeLive: true で作成
   * 過去レポートはスナップショットのため financeLive を付けない。
   * ------------------------------------------------ */
  var SiteConfig = {
    base: BASE,
    brand: "father cafe",
    tagline: "FIRE×父親の実録",
    updatedAt: "2026年7月",

    profile: {
      age: 43,
      birthYear: 1982,
      job: "会社員（岐阜県・持ち家ローン完済）",
      family: "夫婦＋大学生の子2人（法学系・理工系）",
      x: "https://x.com/father_cafe",
      xHandle: "@father_cafe",
      note: "https://note.com/father_cafe"
    },

    report: {
      number: 3,
      month: "2026年7月",
      published: "7月31日",
      href: BASE + "/monthly-report/2026/07/31/monthly-report-003/",
      tileTitle: "2026年7月号（#003）"
    },

    finance: {
      totalAssets: 9520,        // 総資産（万円）
      monthOverMonth: 73,       // 前月比（万円）
      fireTarget: 13500,        // 決行ライン（万円）
      fireConsiderLine: 12500,  // 検討ライン（万円）
      fireAge: 50,              // 目標FIRE年齢
      fireTargetDate: "2032-12-27",
      annualExpense: 360,       // 基本の年間生活費（万円）
      coastIncomeMin: 108,      // Coast収入 下限（万円/年）
      coastIncomeMax: 216,      // Coast収入 上限（万円/年）
      buckets: {
        A: { amount: 650,  label: "生活防衛", desc: "現金・短期債", color: "#93c5fd" },
        B: { amount: 1210, label: "安定",     desc: "債券・バランス", color: "#c4b5fd" },
        C: { amount: 7660, label: "成長",     desc: "株式インデックス", color: "#deff9a" }
      }
    },

    nav: [
      { id: "home",      label: "ホーム",       href: BASE + "/" },
      { id: "about",     label: "About",        href: BASE + "/about.html" },
      { id: "design",    label: "FIRE設計図",   href: BASE + "/design/" },
      { id: "simulator", label: "シミュレーター", href: BASE + "/simulator/" },
      { id: "report",    label: "月次レポート",  href: BASE + "/monthly-report/2026/07/31/monthly-report-003/" }
    ]
  };

  /* ナビの月次レポートリンクを report.href と常に同期 */
  (function syncReportNav(c) {
    if (!c.report || !c.report.href) return;
    for (var i = 0; i < c.nav.length; i++) {
      if (c.nav[i].id === "report") { c.nav[i].href = c.report.href; break; }
    }
  })(SiteConfig);

  /* ---------- 派生値の計算 ---------- */
  SiteConfig.derived = (function (f) {
    try {
      var progress = f.fireTarget > 0 ? (f.totalAssets / f.fireTarget) * 100 : 0;
      var totalBuckets = f.buckets.A.amount + f.buckets.B.amount + f.buckets.C.amount;
      var days = null;
      var target = new Date(f.fireTargetDate + "T00:00:00+09:00");
      if (!isNaN(target.getTime())) {
        days = Math.max(0, Math.ceil((target - new Date()) / 86400000));
      }
      return {
        progressPct: Math.min(100, progress),
        progressLabel: progress.toFixed(1),
        remaining: Math.max(0, f.fireTarget - f.totalAssets),
        daysToFire: days,
        totalBuckets: totalBuckets
      };
    } catch (e) {
      console.error("config.js: derived calculation failed", e);
      return { progressPct: 0, progressLabel: "0.0", remaining: 0, daysToFire: null, totalBuckets: 0 };
    }
  })(SiteConfig.finance);

  /* ---------- 共通UIレンダラー ---------- */
  var SiteUI = {
    /** 数値を3桁区切り文字列に */
    fmt: function (n) {
      try { return Math.round(n).toLocaleString("ja-JP"); }
      catch (e) { return String(n); }
    },

    /** 共通ヘッダー（ナビ）を #site-header に描画 */
    renderNav: function (activeId) {
      try {
        var mount = document.getElementById("site-header");
        if (!mount) return;
        var links = SiteConfig.nav.map(function (item) {
          var cls = item.id === activeId ? ' class="active"' : "";
          return '<a href="' + item.href + '"' + cls + ">" + item.label + "</a>";
        }).join("");
        mount.innerHTML =
          '<div class="bento-header-inner">' +
            '<a class="bento-logo" href="' + SiteConfig.base + '/">' + SiteConfig.brand + '<span class="logo-dot">.</span></a>' +
            '<nav class="bento-nav">' + links + "</nav>" +
          "</div>";
      } catch (e) {
        console.error("config.js: renderNav failed", e);
      }
    },

    /** 共通フッターを #site-footer に描画 */
    renderFooter: function () {
      try {
        var mount = document.getElementById("site-footer");
        if (!mount) return;
        mount.innerHTML =
          "<p>" + SiteConfig.brand + " — " + SiteConfig.tagline +
          ' ／ <a href="' + SiteConfig.profile.x + '">X ' + SiteConfig.profile.xHandle + "</a>" +
          ' ／ <a href="' + SiteConfig.profile.note + '">note</a></p>' +
          "<p>本サイトの数値は個人の記録であり、投資助言ではありません。</p>";
      } catch (e) {
        console.error("config.js: renderFooter failed", e);
      }
    },

    /** スクロール連動フェードイン（IntersectionObserver、非対応環境は即表示） */
    initFadeIn: function () {
      try {
        var targets = document.querySelectorAll(".fade-in");
        if (!("IntersectionObserver" in global)) {
          targets.forEach(function (el) { el.classList.add("visible"); });
          return;
        }
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("visible");
              io.unobserve(entry.target);
            }
          });
        }, { threshold: 0.08 });
        targets.forEach(function (el) { io.observe(el); });
      } catch (e) {
        console.warn("config.js: initFadeIn failed", e);
        document.querySelectorAll(".fade-in").forEach(function (el) { el.classList.add("visible"); });
      }
    },

    /** Xシェア（Web Share API優先、フォールバックはintentリンク） */
    share: function (text, url) {
      var shareUrl = url || global.location.href;
      try {
        if (navigator.share) {
          navigator.share({ text: text, url: shareUrl }).catch(function (e) {
            if (e && e.name !== "AbortError") console.warn("share failed", e);
          });
          return;
        }
      } catch (e) {
        console.warn("Web Share API unavailable", e);
      }
      try {
        var intent = "https://twitter.com/intent/tweet?text=" +
          encodeURIComponent(text) + "&url=" + encodeURIComponent(shareUrl);
        global.open(intent, "_blank", "noopener");
      } catch (e) {
        console.error("share fallback failed", e);
      }
    },

    /** SSOT の財務値マップ（data-finance 属性用） */
    financeValues: function () {
      var f = SiteConfig.finance;
      var d = SiteConfig.derived;
      var r = SiteConfig.report || {};
      var fmt = this.fmt;
      var mom = f.monthOverMonth;
      var momText = mom == null ? "—" : ((mom >= 0 ? "+" : "") + fmt(mom));
      return {
        totalAssets: fmt(f.totalAssets),
        totalAssetsMan: fmt(f.totalAssets) + "万円",
        fireTarget: fmt(f.fireTarget),
        fireTargetMan: fmt(f.fireTarget) + "万円",
        fireConsiderLine: fmt(f.fireConsiderLine),
        fireConsiderLineMan: fmt(f.fireConsiderLine) + "万円",
        progressLabel: d.progressLabel,
        progressPct: d.progressLabel + "%",
        remaining: fmt(d.remaining),
        remainingMan: fmt(d.remaining) + "万円",
        updatedAt: SiteConfig.updatedAt,
        updatedAtPoint: SiteConfig.updatedAt + "時点",
        bucketA: fmt(f.buckets.A.amount),
        bucketB: fmt(f.buckets.B.amount),
        bucketC: fmt(f.buckets.C.amount),
        monthOverMonth: momText,
        monthOverMonthMan: momText + "万円",
        reportMonth: r.month || SiteConfig.updatedAt,
        reportNumber: r.number != null ? String(r.number) : "—",
        reportPublished: r.published || "—",
        reportProgress: d.progressLabel + "%",
        annualExpense: fmt(f.annualExpense)
      };
    },

    /** [data-finance="key"] 要素に SSOT 値を注入 */
    applyFinanceBindings: function (root) {
      try {
        var scope = root || document;
        var map = this.financeValues();
        scope.querySelectorAll("[data-finance]").forEach(function (el) {
          var key = el.getAttribute("data-finance");
          if (map[key] !== undefined) el.textContent = map[key];
        });
        scope.querySelectorAll("[data-finance-bar]").forEach(function (el) {
          el.style.width = SiteConfig.derived.progressPct + "%";
        });
      } catch (e) {
        console.error("config.js: applyFinanceBindings failed", e);
      }
    },

    /** 最新月次レポートへのリンクを同期 */
    syncReportLinks: function () {
      try {
        var href = SiteConfig.report && SiteConfig.report.href;
        if (!href) return;
        document.querySelectorAll("[data-report-link]").forEach(function (el) {
          el.setAttribute("href", href);
        });
        var title = SiteConfig.report.tileTitle;
        document.querySelectorAll("[data-report-title]").forEach(function (el) {
          if (title) el.textContent = title;
        });
      } catch (e) {
        console.warn("config.js: syncReportLinks failed", e);
      }
    },

    /** FIRE設計図ページの動的描画 */
    bindDesignPage: function () {
      try {
        this.applyFinanceBindings();
        var f = SiteConfig.finance;
        var d = SiteConfig.derived;
        var fmt = this.fmt;
        var bar = document.getElementById("dAllocBar");
        if (bar && d.totalBuckets > 0) {
          var keys = ["A", "B", "C"];
          var children = bar.children;
          for (var i = 0; i < keys.length; i++) {
            var pct = f.buckets[keys[i]].amount / d.totalBuckets * 100;
            children[i].style.width = pct.toFixed(1) + "%";
            if (pct >= 8) children[i].textContent = Math.round(pct) + "%";
          }
        }
        this.syncReportLinks();
      } catch (e) {
        console.error("config.js: bindDesignPage failed", e);
      }
    },

    /** ページ共通初期化 */
    init: function (activeId, opts) {
      opts = opts || {};
      this.renderNav(activeId);
      this.renderFooter();
      this.initFadeIn();
      this.syncReportLinks();
      if (activeId === "design") this.bindDesignPage();
      if (opts.financeLive) this.applyFinanceBindings();
    }
  };

  global.SiteConfig = SiteConfig;
  global.SiteUI = SiteUI;
})(window);
