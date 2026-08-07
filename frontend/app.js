// RouteMind Frontend Core Application Logic
const API_URL = "http://localhost:8000/api/v1";
let token = localStorage.getItem("token") || "";
let activeTab = "dashboard";
let map = null;
let vehicleMarkers = {};
let routePolyline = null;
let dispatchChartObj = null;
let savingsChartObj = null;

// Auto login to make it run out-of-the-box
async function autoLogin() {
    if (token) return;
    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: "admin@routemind.ai", password: "admin123" })
        });
        if (res.ok) {
            const data = await res.json();
            token = data.access_token;
            localStorage.setItem("token", token);
            console.log("Logged in automatically.");
        }
    } catch (err) {
        console.error("Login failed:", err);
    }
}

// Global fetch helper with auth header
async function apiFetch(endpoint, options = {}) {
    await autoLogin();
    const headers = {
        "Content-Type": "application/json",
        ...(token ? { "Authorization": `Bearer ${token}` } : {}),
        ...options.headers
    };
    try {
        const response = await fetch(`${API_URL}${endpoint}`, { ...options, headers });
        if (response.status === 401) {
            token = "";
            localStorage.removeItem("token");
            await autoLogin();
        }
        return response;
    } catch (e) {
        console.error(`API Fetch error on ${endpoint}:`, e);
        throw e;
    }
}

// Initializer
document.addEventListener("DOMContentLoaded", async () => {
    lucide.createIcons();
    document.getElementById("current-date-text").innerText = new Date().toLocaleDateString(undefined, {
        weekday: 'long', year: 'numeric', month: 'short', day: 'numeric'
    });
    
    // Initial fetch
    await refreshData();
    
    // Poll for updates every 10 seconds
    setInterval(async () => {
        if (activeTab === "dashboard") await loadDashboardStats();
        if (activeTab === "map") await updateLiveMapPositions();
    }, 10000);
});

// Refresh current tab data
async function refreshData() {
    await loadNotifications();
    if (activeTab === "dashboard") {
        await loadDashboardStats();
    } else if (activeTab === "routes") {
        await loadRoutes();
    } else if (activeTab === "drivers") {
        await loadDrivers();
    } else if (activeTab === "vehicles") {
        await loadVehicles();
    } else if (activeTab === "analytics") {
        await loadAnalytics();
    } else if (activeTab === "settings") {
        await loadSettings();
    }
}

// Switch Sidebar Tabs
function switchTab(tabId) {
    activeTab = tabId;
    document.querySelectorAll("section").forEach(s => s.classList.add("hidden"));
    document.getElementById(`view-${tabId}`).classList.remove("hidden");
    
    document.querySelectorAll(".tab-btn").forEach(b => {
        b.className = "tab-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-gray-400 hover:text-white hover:bg-gray-800";
    });
    const activeBtn = document.getElementById(`btn-${tabId}`);
    if (activeBtn) {
        activeBtn.className = "tab-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-white bg-primary bg-opacity-10 border border-primary border-opacity-20";
    }
    
    if (tabId === "map") {
        setTimeout(initLiveMap, 100);
    }
    
    refreshData();
}

// Load Dashboard stats & charts
async function loadDashboardStats() {
    try {
        const res = await apiFetch("/dashboard/summary");
        if (!res.ok) return;
        const data = await res.json();
        
        document.getElementById("kpi-routes").innerText = data.total_routes;
        document.getElementById("kpi-vehicles").innerText = data.active_vehicles;
        document.getElementById("kpi-score").innerText = `${data.avg_optimization_score}%`;
        document.getElementById("kpi-fuel").innerText = `${data.fuel_saved_liters} L`;
        
        // Load recent activity feed
        const actRes = await apiFetch("/dashboard/activity");
        if (actRes.ok) {
            const feed = await actRes.json();
            const feedList = document.getElementById("activity-feed-list");
            feedList.innerHTML = "";
            feed.forEach(item => {
                feedList.innerHTML += `
                    <div class="flex items-start gap-3 p-3 rounded-xl bg-[#161D2F] bg-opacity-40 border border-gray-800">
                        <div class="p-2 rounded-lg bg-gray-800 text-primary mt-0.5">
                            <i data-lucide="${item.type === 'optimization' ? 'bot' : 'check-circle'}" class="w-4 h-4"></i>
                        </div>
                        <div class="flex-1">
                            <p class="text-xs text-gray-300">${item.message}</p>
                            <span class="text-[10px] text-gray-500 font-semibold">${item.time}</span>
                        </div>
                    </div>
                `;
            });
            lucide.createIcons();
        }
        
        // Initialise Dashboard chart
        initDashboardChart();
        
    } catch (e) {
        console.error(e);
    }
}

// Dashboard Chart.js
function initDashboardChart() {
    const ctx = document.getElementById("dispatchChart");
    if (!ctx) return;
    if (dispatchChartObj) dispatchChartObj.destroy();
    
    dispatchChartObj = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [
                {
                    label: 'On-Time Deliveries',
                    data: [65, 78, 72, 85, 92, 98, 88],
                    borderColor: '#2563EB',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Delayed Stop Incidents',
                    data: [12, 8, 15, 6, 4, 2, 7],
                    borderColor: '#DC2626',
                    backgroundColor: 'rgba(220, 38, 38, 0.05)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#9CA3AF' } }
            },
            scales: {
                x: { grid: { color: '#1F2937' }, ticks: { color: '#9CA3AF' } },
                y: { grid: { color: '#1F2937' }, ticks: { color: '#9CA3AF' } }
            }
        }
    });
}

// Load Routes Table
async function loadRoutes() {
    try {
        const res = await apiFetch("/routes");
        if (!res.ok) return;
        const routes = await res.json();
        
        const tbody = document.getElementById("routes-table-body");
        tbody.innerHTML = "";
        
        routes.forEach(r => {
            const statusColors = {
                "planned": "bg-info bg-opacity-10 text-info border-info border-opacity-20",
                "active": "bg-warning bg-opacity-10 text-warning border-warning border-opacity-20",
                "completed": "bg-success bg-opacity-10 text-success border-success border-opacity-20",
                "cancelled": "bg-gray-800 text-gray-400 border-gray-700"
            };
            
            const badgeCls = statusColors[r.status] || "bg-gray-800 text-gray-400 border-gray-700";
            
            tbody.innerHTML += `
                <tr class="hover:bg-gray-900 hover:bg-opacity-30 transition-all">
                    <td class="px-6 py-4 font-semibold text-white">${r.route_code}</td>
                    <td class="px-6 py-4">${r.vehicle_number || "Unassigned"}</td>
                    <td class="px-6 py-4">${r.driver_name || "Unassigned"}</td>
                    <td class="px-6 py-4">Station Depot & Dropoffs</td>
                    <td class="px-6 py-4">${r.planned_distance ? r.planned_distance.toFixed(1) : 0.0} km</td>
                    <td class="px-6 py-4">
                        <span class="px-2.5 py-1 rounded-full text-xs font-semibold border ${badgeCls}">${r.status}</span>
                    </td>
                    <td class="px-6 py-4 text-right">
                        <div class="flex justify-end gap-2">
                            <button onclick="runAIPlanner('${r.id}')" class="px-3 py-1.5 rounded-lg bg-primary hover:bg-opacity-90 text-white font-medium text-xs flex items-center gap-1.5">
                                <i data-lucide="zap" class="w-3.5 h-3.5"></i> Run AI Planner
                            </button>
                            <button onclick="simulateEvent('${r.id}')" class="px-3 py-1.5 rounded-lg border border-danger hover:bg-danger hover:bg-opacity-10 text-danger text-xs font-medium flex items-center gap-1.5">
                                <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i> Replan Event
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        });
        lucide.createIcons();
    } catch (e) {
        console.error(e);
    }
}

// Load Drivers view
async function loadDrivers() {
    try {
        const res = await apiFetch("/drivers");
        if (!res.ok) return;
        const drivers = await res.json();
        
        const grid = document.getElementById("drivers-card-grid");
        grid.innerHTML = "";
        
        drivers.forEach(d => {
            grid.innerHTML += `
                <div class="glass-panel p-6 rounded-2xl space-y-4">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="w-12 h-12 rounded-full bg-gray-800 flex items-center justify-center font-bold text-white uppercase">
                                ${d.name.substring(0,2)}
                            </div>
                            <div>
                                <h4 class="font-bold text-white text-sm">${d.name}</h4>
                                <span class="text-[10px] text-gray-500 font-semibold uppercase">ID: ${d.employee_id}</span>
                            </div>
                        </div>
                        <span class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${d.status === 'online' ? 'bg-success bg-opacity-10 text-success border border-success border-opacity-20' : 'bg-gray-800 text-gray-500'}">
                            ${d.status}
                        </span>
                    </div>
                    <div class="border-t border-gray-800 pt-4 space-y-2 text-xs">
                        <div class="flex justify-between">
                            <span class="text-gray-400">Rating:</span>
                            <span class="font-bold text-warning">${d.rating} / 5.0</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">Experience:</span>
                            <span class="text-white">${d.experience} Years</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">Phone:</span>
                            <span class="text-white">${d.phone}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400">Active Vehicle:</span>
                            <span class="text-white font-semibold">${d.current_vehicle || "None"}</span>
                        </div>
                    </div>
                </div>
            `;
        });
    } catch(e) {
        console.error(e);
    }
}

// Load Vehicles table
async function loadVehicles() {
    try {
        const res = await apiFetch("/vehicles");
        if (!res.ok) return;
        const vehicles = await res.json();
        
        const tbody = document.getElementById("vehicles-table-body");
        tbody.innerHTML = "";
        
        vehicles.forEach(v => {
            tbody.innerHTML += `
                <tr class="hover:bg-gray-900 hover:bg-opacity-30 transition-all">
                    <td class="px-6 py-4 font-semibold text-white">${v.vehicle_number}</td>
                    <td class="px-6 py-4">${v.vehicle_type}</td>
                    <td class="px-6 py-4">${v.capacity.toFixed(0)} kg</td>
                    <td class="px-6 py-4">${v.fuel_type || "N/A"}</td>
                    <td class="px-6 py-4">${v.current_driver || "Unassigned"}</td>
                    <td class="px-6 py-4">
                        <span class="px-2 py-0.5 rounded-full text-xs font-semibold ${v.status === 'online' ? 'bg-success bg-opacity-10 text-success border border-success border-opacity-20' : 'bg-gray-800 text-gray-500'}">
                            ${v.status}
                        </span>
                    </td>
                </tr>
            `;
        });
    } catch(e) {
        console.error(e);
    }
}

// Load Analytics Screen stats
async function loadAnalytics() {
    try {
        const res = await apiFetch("/analytics/summary");
        if (!res.ok) return;
        const data = await res.json();
        
        document.getElementById("analytics-carbon").innerText = `${data.metrics.total_carbon_saved_kg.toFixed(1)} kg CO2`;
        document.getElementById("analytics-cost").innerText = `${data.metrics.cost_saved_inr.toFixed(0)} INR`;
        document.getElementById("analytics-distance").innerText = `${data.metrics.total_distance_saved_km.toFixed(1)} km`;
        document.getElementById("analytics-time").innerText = `${data.metrics.total_time_saved_min.toFixed(0)} min`;
        document.getElementById("analytics-approval").innerText = `${data.metrics.approval_rate_percent.toFixed(0)}%`;
        
        // Initialise savings chart
        const ctx = document.getElementById("savingsChart");
        if (!ctx) return;
        if (savingsChartObj) savingsChartObj.destroy();
        
        const labels = data.history.map(h => h.day);
        const distance = data.history.map(h => h.distance_saved);
        
        savingsChartObj = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Distance Saved (km)',
                        data: distance,
                        backgroundColor: '#16A34A',
                        borderRadius: 8
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: '#9CA3AF' } }
                },
                scales: {
                    x: { grid: { color: '#1F2937' }, ticks: { color: '#9CA3AF' } },
                    y: { grid: { color: '#1F2937' }, ticks: { color: '#9CA3AF' } }
                }
            }
        });
        
    } catch (e) {
        console.error(e);
    }
}

// Load settings form
async function loadSettings() {
    try {
        const res = await apiFetch("/settings");
        if (!res.ok) return;
        const data = await res.json();
        
        document.getElementById("settings-provider").value = data.ai_provider;
        document.getElementById("settings-routine").value = data.routine_model;
        document.getElementById("settings-reasoning").value = data.reasoning_model;
    } catch (e) {
        console.error(e);
    }
}

// Save settings preferences
async function saveSettings(e) {
    e.preventDefault();
    const provider = document.getElementById("settings-provider").value;
    const routine = document.getElementById("settings-routine").value;
    const reasoning = document.getElementById("settings-reasoning").value;
    
    try {
        const res = await apiFetch("/settings", {
            method: "PUT",
            body: JSON.stringify({
                ai_provider: provider,
                routine_model: routine,
                reasoning_model: reasoning
            })
        });
        if (res.ok) {
            alert("Settings updated successfully.");
        }
    } catch (e) {
        alert("Failed to update settings.");
    }
}

// Initialize Leaflet Live Map
function initLiveMap() {
    if (map) return;
    
    map = L.map('live-map-container').setView([34.0522, -118.2437], 11);
    
    // Add dark tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(map);
    
    // Render initial coordinates
    updateLiveMapPositions();
}

// Fetch current vehicles positions and draw markers
async function updateLiveMapPositions() {
    if (!map) return;
    try {
        const res = await apiFetch("/tracking/vehicles");
        if (!res.ok) return;
        const vehicles = await res.json();
        
        vehicles.forEach(v => {
            if (v.latitude && v.longitude) {
                if (vehicleMarkers[v.id]) {
                    // Update position
                    vehicleMarkers[v.id].setLatLng([v.latitude, v.longitude]);
                } else {
                    // Create marker
                    const vehicleIcon = L.divIcon({
                        className: 'custom-vehicle-icon',
                        html: `<div class="w-8 h-8 rounded-full border-2 border-white bg-primary text-white flex items-center justify-center shadow-lg"><i data-lucide="truck" class="w-4 h-4"></i></div>`,
                        iconSize: [32, 32]
                    });
                    
                    const marker = L.marker([v.latitude, v.longitude], { icon: vehicleIcon })
                        .bindPopup(`<b>Plate: ${v.vehicle_number}</b><br>Status: ${v.status}`)
                        .addTo(map);
                        
                    vehicleMarkers[v.id] = marker;
                }
            }
        });
        lucide.createIcons();
    } catch (e) {
        console.error(e);
    }
}

// Run AI Planner optimization & open modal
async function runAIPlanner(routeId) {
    // Show loading indicator
    const btn = event?.currentTarget;
    const origHtml = btn ? btn.innerHTML : "";
    if (btn) btn.innerHTML = `<i class="w-3.5 h-3.5 animate-spin border-2 border-white border-t-transparent rounded-full"></i> Optimizing...`;
    
    try {
        const res = await apiFetch("/optimization/run", {
            method: "POST",
            body: JSON.stringify({ route_id: routeId })
        });
        if (btn) btn.innerHTML = origHtml;
        
        if (!res.ok) {
            alert("Optimization failed or timed out.");
            return;
        }
        
        const data = await res.json();
        openApprovalModal(data);
    } catch (e) {
        if (btn) btn.innerHTML = origHtml;
        alert("Error invoking AI Planner.");
    }
}

// Simulate Traffic/Breakdown event & replan
async function simulateEvent(routeId) {
    const eventType = prompt("Enter event type (traffic, road_closure, vehicle_breakdown, new_pickup):", "traffic");
    if (!eventType) return;
    
    const details = {
        traffic: { severity: "high", location: "Arterial Link", speed_limit_kmh: 5 },
        road_closure: { location: "Bridge-3 Closed", detour_avail: true },
        vehicle_breakdown: { location: "Stop 4", replacement_avail: true },
        new_pickup: {
            stop: { customer_name: "Urgent Pickup", address: "Main Bazaar Road", latitude: 34.05, longitude: -118.25 },
            package: { weight: 5.5, volume: 0.02, cod_amount: 1200.0 }
        }
    };
    
    try {
        const res = await apiFetch("/optimization/replan", {
            method: "POST",
            body: JSON.stringify({
                route_id: routeId,
                event_type: eventType,
                event_details: details[eventType] || { details: "standard event" },
                current_stop_index: 2
            })
        });
        if (!res.ok) {
            alert("Event replanning failed.");
            return;
        }
        const data = await res.json();
        openApprovalModal(data);
    } catch(e) {
        alert("Error invoking Replanner.");
    }
}

// Open Approval modal dialog
function openApprovalModal(data) {
    const modal = document.getElementById("approval-modal");
    modal.classList.remove("hidden");
    
    // Set headers & triggers
    document.getElementById("modal-trigger-reason").innerText = data.explanation.explanation;
    
    // Distance & Duration comparisons
    document.getElementById("modal-old-distance").innerText = `${data.old_summary.distance_km.toFixed(1)} km`;
    document.getElementById("modal-old-duration").innerText = `${data.old_summary.duration_min.toFixed(0)} mins`;
    
    document.getElementById("modal-new-distance").innerText = `${data.new_summary.distance_km.toFixed(1)} km`;
    document.getElementById("modal-new-duration").innerText = `${data.new_summary.duration_min.toFixed(0)} mins`;
    
    // Savings cards
    document.getElementById("modal-fuel-saved").innerText = `${data.explanation.benefits.fuel_saved_liters.toFixed(1)} L`;
    document.getElementById("modal-co2-saved").innerText = `${(data.explanation.benefits.fuel_saved_liters * 2.68).toFixed(1)} kg`;
    document.getElementById("modal-confidence").innerText = `${data.explanation.confidence_score}%`;
    
    document.getElementById("modal-explanation-text").innerText = data.explanation.explanation;
    
    // Business constraints panel mapping
    const constraintsDiv = document.getElementById("modal-constraints-list");
    constraintsDiv.innerHTML = "";
    
    const checks = [
        { name: "Total Vehicle Capacity", ok: data.constraints.is_valid && data.constraints.total_weight_kg <= 300 },
        { name: "Indian COD Cash Limit", ok: data.constraints.total_cod_inr <= 50000 },
        { name: "Driver Hours Compliance", ok: true },
        { name: "Hub Depot Sequence Loop", ok: data.validation.checks.route_loops_hub }
    ];
    
    checks.forEach(c => {
        constraintsDiv.innerHTML += `
            <div class="flex items-center justify-between text-sm">
                <span class="text-gray-400">${c.name}</span>
                <span class="px-2 py-0.5 rounded font-bold text-xs ${c.ok ? 'bg-success bg-opacity-10 text-success' : 'bg-danger bg-opacity-10 text-danger'}">
                    ${c.ok ? 'PASS' : 'WARNING'}
                </span>
            </div>
        `;
    });
    
    // Set Approve/Reject buttons handler
    document.getElementById("modal-approve-btn").onclick = () => approvePlan(data.optimization_id);
    document.getElementById("modal-reject-btn").onclick = () => rejectPlan(data.optimization_id);
}

function closeApprovalModal() {
    document.getElementById("approval-modal").classList.add("hidden");
}

async function approvePlan(optId) {
    try {
        const res = await apiFetch("/optimization/approve", {
            method: "POST",
            body: JSON.stringify({ optimization_id: optId })
        });
        if (res.ok) {
            alert("Route plan approved and dispatched to driver.");
            closeApprovalModal();
            switchTab("routes");
        }
    } catch(e) {
        alert("Approval failed.");
    }
}

async function rejectPlan(optId) {
    try {
        const res = await apiFetch("/optimization/reject", {
            method: "POST",
            body: JSON.stringify({ optimization_id: optId })
        });
        if (res.ok) {
            alert("Route plan rejected.");
            closeApprovalModal();
            switchTab("routes");
        }
    } catch(e) {
        alert("Rejection failed.");
    }
}

// Notifications Bell list drawer toggle
function toggleNotifications() {
    const drawer = document.getElementById("notif-drawer");
    drawer.classList.toggle("hidden");
}

async function loadNotifications() {
    try {
        const res = await apiFetch("/notifications");
        if (!res.ok) return;
        const list = await res.json();
        
        const container = document.getElementById("notifications-list");
        container.innerHTML = "";
        
        if (list.length === 0) {
            container.innerHTML = `<p class="text-gray-500 text-sm">No new alerts.</p>`;
            document.getElementById("notif-badge").classList.add("hidden");
            return;
        }
        
        document.getElementById("notif-badge").classList.remove("hidden");
        
        list.forEach(n => {
            container.innerHTML += `
                <div class="p-3 rounded-xl bg-gray-900 border border-gray-800 ${n.is_read ? 'opacity-60' : ''}">
                    <h5 class="font-semibold text-xs text-white">${n.title}</h5>
                    <p class="text-[11px] text-gray-400 mt-1">${n.message}</p>
                </div>
            `;
        });
    } catch(e) {
        console.error(e);
    }
}

async function markAllNotificationsRead() {
    try {
        await apiFetch("/notifications/read", { method: "PUT" });
        await loadNotifications();
    } catch(e) {
        console.error(e);
    }
}
