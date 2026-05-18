---
layout: default
title: FIREシミュレーター
permalink: /fire-design/simulator/
---

> [ホーム](/fire-design/) ｜ [FIRE設計図](/fire-design/design/) ｜ [About](/fire-design/about/)

# FIREシミュレーター

現在の資産・毎月の積立・想定利回りを入力すると、Coast FIRE達成までの見通しを計算します。

---

<div style="background:#1a1a2e;border:1px solid #444;border-radius:8px;padding:24px;max-width:600px;margin:0 auto;">

<div style="margin-bottom:16px;">
  <label style="display:block;margin-bottom:4px;color:#f0c040;">現在の総資産（万円）</label>
  <input id="currentAssets" type="number" value="10009" style="width:100%;padding:8px;border-radius:4px;border:1px solid #666;background:#2a2a3e;color:#fff;font-size:16px;">
</div>

<div style="margin-bottom:16px;">
  <label style="display:block;margin-bottom:4px;color:#f0c040;">毎月の積立額（万円）</label>
  <input id="monthlyContrib" type="number" value="0" style="width:100%;padding:8px;border-radius:4px;border:1px solid #666;background:#2a2a3e;color:#fff;font-size:16px;">
</div>

<div style="margin-bottom:16px;">
  <label style="display:block;margin-bottom:4px;color:#f0c040;">年間想定利回り（%）</label>
  <input id="annualReturn" type="number" value="5" step="0.1" style="width:100%;padding:8px;border-radius:4px;border:1px solid #666;background:#2a2a3e;color:#fff;font-size:16px;">
</div>

<div style="margin-bottom:16px;">
  <label style="display:block;margin-bottom:4px;color:#f0c040;">FIRE目標資産額（万円）</label>
  <input id="fireTarget" type="number" value="13500" style="width:100%;padding:8px;border-radius:4px;border:1px solid #666;background:#2a2a3e;color:#fff;font-size:16px;">
</div>

<button onclick="calcFire()" style="width:100%;padding:12px;background:#f0c040;color:#000;border:none;border-radius:4px;font-size:16px;font-weight:bold;cursor:pointer;">計算する</button>

<div id="result" style="margin-top:24px;"></div>

</div>

<script>
function calcFire() {
  var current = parseFloat(document.getElementById('currentAssets').value) || 0;
  var monthly = parseFloat(document.getElementById('monthlyContrib').value) || 0;
  var rate = parseFloat(document.getElementById('annualReturn').value) / 100 || 0.05;
  var target = parseFloat(document.getElementById('fireTarget').value) || 13500;
  var monthlyRate = rate / 12;
  var months = 0;
  var assets = current;
  var maxMonths = 600;

  while (assets < target && months < maxMonths) {
    assets = assets * (1 + monthlyRate) + monthly;
    months++;
  }

  var resultDiv = document.getElementById('result');
  var progressPct = Math.min((current / target * 100).toFixed(1), 100);

  if (months >= maxMonths) {
    resultDiv.innerHTML = '<div style="color:#ff6b6b;padding:16px;background:#2a1a1a;border-radius:4px;">' +
      '<p style="margin:0 0 8px;font-size:18px;font-weight:bold;">⚠️ 50年以内には達成できない見込みです</p>' +
      '<p style="margin:0;color:#aaa;">積立額の増加か利回りの見直しを検討してください。</p>' +
      '</div>';
  } else {
    var years = Math.floor(months / 12);
    var remainMonths = months % 12;
    var finalAssets = Math.round(assets);
    resultDiv.innerHTML = '<div style="color:#4ecdc4;padding:16px;background:#1a2a2a;border-radius:4px;">' +
      '<p style="margin:0 0 8px;font-size:18px;font-weight:bold;">🎯 FIRE達成まで ' + years + '年' + remainMonths + 'ヶ月</p>' +
      '<p style="margin:0 0 4px;">達成時の資産額：約 ' + finalAssets.toLocaleString() + ' 万円</p>' +
      '<p style="margin:0 0 12px;">現在の達成率：<strong>' + progressPct + '%</strong></p>' +
      '<div style="background:#333;border-radius:4px;height:16px;overflow:hidden;">' +
      '<div style="background:#f0c040;height:100%;width:' + progressPct + '%;transition:width 0.5s;"></div>' +
      '</div>' +
      '</div>';
  }
}
// 初期表示
calcFire();
</script>

---

## 計算の前提

- 複利計算（月次）で試算しています
- 税金・手数料は考慮していません
- Coast FIREの考え方：目標資産に達したら積立停止し、複利成長に任せる

## 私の現在地（2025年5月）

| 項目 | 数値 |
|---|---|
| 現在の総資産 | 約1億円（1億9万円） |
| FIRE目標 | 1億3,500万円 |
| 達成率 | **69.4%** |
| 想定利回り | 5%（インデックス長期平均） |

---

> [ホーム](/fire-design/) ｜ [FIRE設計図](/fire-design/design/) ｜ [About](/fire-design/about/)
