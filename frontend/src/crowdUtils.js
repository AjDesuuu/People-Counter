export function getCrowdLevel(density) {
  if (density < 5) {
    return { key: "LOW", label: "🟢 LOW CROWD" };
  }
  if (density < 15) {
    return { key: "MODERATE", label: "🟡 MODERATE CROWD" };
  }
  if (density < 30) {
    return { key: "HIGH", label: "🟠 HIGH CROWD" };
  }
  return { key: "VERY_HIGH", label: "🔴 VERY HIGH CROWD" };
}

export function getRecommendations(personCount, density) {
  const crowdLevel = getCrowdLevel(density);
  const items = [];

  if (crowdLevel.key === "LOW") {
    items.push("✅ Perfect time to visit. Minimal wait times expected.");
    items.push("🎢 Most attractions should have short queues.");
    items.push("📸 Great moment for clear photos.");
  } else if (crowdLevel.key === "MODERATE") {
    items.push("⚠️ Moderate crowding. Plan your route before moving.");
    items.push("🎫 Use priority lanes for popular rides if available.");
    items.push("🍽️ Food lines may be slightly longer than usual.");
  } else if (crowdLevel.key === "HIGH") {
    items.push("⚠️ High crowd levels detected in this scene.");
    items.push("🏃 Start with less popular attractions first.");
    items.push("🎭 Consider shows or indoor attractions while queues drop.");
  } else {
    items.push("🚨 Very high crowding. Consider moving to another zone.");
    items.push("💡 Take a break in rest or dining areas.");
    items.push("🕐 Revisit this area during off-peak hours.");
  }

  if (personCount > 50) {
    items.push(`👥 ${personCount} people detected. This area is very busy.`);
  } else if (personCount > 20) {
    items.push(`👥 ${personCount} people detected. Expect noticeable queues.`);
  } else if (personCount > 10) {
    items.push(`👥 ${personCount} people detected. Moderate activity level.`);
  } else {
    items.push(`👥 ${personCount} people detected. Comfortable crowd level.`);
  }

  return {
    crowdLevel,
    items,
  };
}
