/* =====================================================================
 * FireStore — 読者のシミュレーター設定（localStorage）
 * サイト公開数値の SSOT は config.js。DEFAULTS は SiteConfig から同期する。
 * ===================================================================== */
(function (global) {
  "use strict";

  var STORAGE_KEY = "fatherCafe.fireParams.v1";

  function defaultsFromSite() {
    var c = global.SiteConfig;
    if (!c || !c.finance) return null;
    var f = c.finance;
    return {
      currentAge: c.profile && c.profile.age ? c.profile.age : 43,
      currentAssets: f.totalAssets,
      fireTarget: f.fireTarget,
      fireAge: f.fireAge,
      annualExpense: f.annualExpense,
      coastIncome: f.coastIncomePlan != null ? f.coastIncomePlan : f.coastIncomeMin,
      fireTargetDate: f.fireTargetDate,
      bucketA: f.buckets.A.amount,
      bucketB: f.buckets.B.amount,
      bucketC: f.buckets.C.amount
    };
  }

  var FALLBACK = {
    currentAge: 43,
    currentAssets: 9520,
    fireTarget: 13500,
    fireAge: 50,
    annualExpense: 360,
    coastIncome: 120,
    fireTargetDate: "2032-12-27",
    bucketA: 650,
    bucketB: 1210,
    bucketC: 7660
  };

  function getDefaults() {
    return defaultsFromSite() || FALLBACK;
  }

  function load() {
    try {
      var raw = global.localStorage.getItem(STORAGE_KEY);
      var saved = raw ? JSON.parse(raw) : {};
      if (typeof saved !== "object" || saved === null) saved = {};
      return Object.assign({}, getDefaults(), saved);
    } catch (e) {
      console.warn("FireStore: load failed, using defaults", e);
      return Object.assign({}, getDefaults());
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

  global.FireStore = { load: load, save: save, reset: reset, derive: derive, getDefaults: getDefaults };
})(window);
