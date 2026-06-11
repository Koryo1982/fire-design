/* =====================================================================
 * FireStore — ページ間パラメータ共有モジュール（localStorage）
 * 設計図・シミュレーター・ダッシュボードで「基本生活費」「目標額」等を共有する。
 * 依存なし・グローバルに window.FireStore を公開。
 * ===================================================================== */
(function (global) {
  "use strict";

  var STORAGE_KEY = "fatherCafe.fireParams.v1";

  // サイト全体の既定値（設計図の公開数値と同期させる）
  var DEFAULTS = {
    currentAge: 43,        // 現在年齢
    currentAssets: 9373,   // 総資産（万円）
    fireTarget: 13500,     // 決行ライン（万円）
    fireAge: 50,           // 目標FIRE年齢
    annualExpense: 360,    // 基本の年間生活費（万円）
    coastIncome: 108,      // Coast収入の下限想定（万円/年）
    fireTargetDate: "2032-12-27", // 50歳の誕生日
    bucketA: 636,          // 生活防衛バケツ（万円）
    bucketB: 1200,         // 安定バケツ（万円）
    bucketC: 8173          // 成長バケツ（万円）
  };

  function load() {
    try {
      var raw = global.localStorage.getItem(STORAGE_KEY);
      var saved = raw ? JSON.parse(raw) : {};
      if (typeof saved !== "object" || saved === null) saved = {};
      return Object.assign({}, DEFAULTS, saved);
    } catch (e) {
      console.warn("FireStore: load failed, using defaults", e);
      return Object.assign({}, DEFAULTS);
    }
  }

  function save(patch) {
    try {
      var raw = global.localStorage.getItem(STORAGE_KEY);
      var saved = raw ? JSON.parse(raw) : {};
      if (typeof saved !== "object" || saved === null) saved = {};
      var next = Object.assign({}, saved, patch);
      global.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch (e) {
      console.warn("FireStore: save failed", e);
    }
    return load();
  }

  function reset() {
    try {
      global.localStorage.removeItem(STORAGE_KEY);
    } catch (e) {
      console.warn("FireStore: reset failed", e);
    }
    return load();
  }

  /** 達成率（%）・残額・FIRE目標日までの日数などの派生値を計算 */
  function derive(params) {
    var p = params || load();
    var progress = p.fireTarget > 0 ? (p.currentAssets / p.fireTarget) * 100 : 0;
    var remaining = Math.max(0, p.fireTarget - p.currentAssets);
    var daysToFire = null;
    try {
      var target = new Date(p.fireTargetDate + "T00:00:00+09:00");
      daysToFire = Math.max(0, Math.ceil((target - new Date()) / 86400000));
    } catch (e) {
      console.warn("FireStore: date parse failed", e);
    }
    return {
      progressPct: Math.min(100, progress),
      progressLabel: progress.toFixed(1),
      remaining: remaining,
      daysToFire: daysToFire,
      totalBuckets: p.bucketA + p.bucketB + p.bucketC
    };
  }

  global.FireStore = { load: load, save: save, reset: reset, derive: derive, DEFAULTS: DEFAULTS };
})(window);
