/* ==========================================================================
   Sentiment Dashboard — Chart.js wiring
   Reads the payload rendered by Django's `json_script` filter:

     {{ chart_payload|json_script:"chart-payload" }}

   Expected shape:
   {
     "a": {"name": "Product A", "positive": 68, "negative": 11, "neutral": 21},
     "b": {"name": "Product B", "positive": 40, "negative": 22, "neutral": 38}  // or null
   }
   ========================================================================== */

(function () {
  const payloadEl = document.getElementById("chart-payload");
  if (!payloadEl) return;

  const payload = JSON.parse(payloadEl.textContent);
  const a = payload.a || { positive: 0, negative: 0, neutral: 0 };
  const b = payload.b || null;

  const COLORS = {
    positive: "#16c6b8",
    negative: "#3e5ff0",
    neutral: "#f5a93b",
    track: "#e9ecf7",
  };

  Chart.defaults.font.family = "'Poppins', 'Segoe UI', sans-serif";

  /* ------------------------------------------------------------------ */
  /* 1. Product A gauge (left card)                                     */
  /* ------------------------------------------------------------------ */
  const meterACtx = document.getElementById("meterChartA");
  if (meterACtx) {
    new Chart(meterACtx, {
      type: "doughnut",
      data: {
        labels: ["Positive", "Negative", "Neutral"],
        datasets: [
          {
            data: [a.positive, a.negative, a.neutral],
            backgroundColor: [COLORS.positive, COLORS.negative, COLORS.neutral],
            borderWidth: 0,
            borderRadius: 10,
            spacing: 3,
          },
        ],
      },
      options: {
        cutout: "78%",
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.label}: ${ctx.parsed}%`,
            },
          },
        },
      },
    });
  }

  /* ------------------------------------------------------------------ */
  /* 2. Grouped bar chart — Product A vs Product B                      */
  /* ------------------------------------------------------------------ */
  const barCtx = document.getElementById("comparisonBarChart");
  if (barCtx) {
    const datasets = [
      {
        label: a.name || "Product A",
        data: [a.positive, a.negative, a.neutral],
        backgroundColor: COLORS.positive,
        borderRadius: 8,
        maxBarThickness: 34,
      },
    ];

    if (b) {
      datasets.push({
        label: b.name || "Product B",
        data: [b.positive, b.negative, b.neutral],
        backgroundColor: COLORS.negative,
        borderRadius: 8,
        maxBarThickness: 34,
      });
    }

    new Chart(barCtx, {
      type: "bar",
      data: {
        labels: ["Positive", "Negative", "Neutral"],
        datasets,
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#1e2545", font: { weight: "600" } },
          },
          y: {
            beginAtZero: true,
            max: 100,
            grid: { color: "rgba(30,37,69,0.06)" },
            ticks: { color: "#7c81a0", stepSize: 25 },
          },
        },
        plugins: {
          legend: {
            display: !!b,
            position: "top",
            align: "end",
            labels: { boxWidth: 10, boxHeight: 10, usePointStyle: true, pointStyle: "circle" },
          },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y}%`,
            },
          },
        },
      },
    });
  }

  /* ------------------------------------------------------------------ */
  /* 3. Product B distribution donut (only when B exists)               */
  /* ------------------------------------------------------------------ */
  const meterBCtx = document.getElementById("meterChartB");
  if (meterBCtx && b) {
    new Chart(meterBCtx, {
      type: "doughnut",
      data: {
        labels: ["Positive", "Negative", "Neutral"],
        datasets: [
          {
            data: [b.positive, b.negative, b.neutral],
            backgroundColor: [COLORS.positive, COLORS.negative, COLORS.neutral],
            borderWidth: 0,
            borderRadius: 10,
            spacing: 3,
          },
        ],
      },
      options: {
        cutout: "72%",
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.label}: ${ctx.parsed}%`,
            },
          },
        },
      },
    });
  }
})();