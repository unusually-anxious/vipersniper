const API_BASE = "http://127.0.0.1:8000";

const state = {
  listings: [],
  filteredListings: [],
  watchlist: [],
  alerts: [],
  filters: {
    search: "",
    bidType: "all",
    score: "all",
    source: "all",
    sort: "highest"
  }
};

function money(v){ return `$${Number(v||0).toLocaleString()}` }
function safe(v){ return v==null?"—":String(v) }

function isZeroBid(item){ return Number(item.bid||0)===0 }

function isEndingSoon(item){
  if(!item.end_time) return false
  const diff=new Date(item.end_time)-new Date()
  return diff>0 && diff<1800000
}

function normalize(t){ return String(t||"").toLowerCase() }

function matchesSearch(item,s){
  if(!s) return true
  const hay=[
    item.title,item.vin,item.make,item.model,item.location,item.source_name
  ].map(normalize).join(" ")
  return hay.includes(normalize(s))
}

function matchesFilters(item){
  const f=state.filters
  if(!matchesSearch(item,f.search)) return false
  if(f.bidType==="zero" && !isZeroBid(item)) return false
  if(f.bidType==="nonzero" && isZeroBid(item)) return false
  if(f.bidType==="ending" && !isEndingSoon(item)) return false
  if(f.score==="70plus" && Number(item.score||0)<70) return false
  if(f.score==="50plus" && Number(item.score||0)<50) return false
  if(f.source!=="all" && normalize(item.source_name)!==normalize(f.source)) return false
  return true
}

function sortListings(items){
  const s=[...items]
  switch(state.filters.sort){
    case "highest": s.sort((a,b)=>b.score-a.score); break
    case "lowest-bid": s.sort((a,b)=>a.bid-b.bid); break
    case "ending-soon":
      s.sort((a,b)=>{
        const A=a.end_time?new Date(a.end_time).getTime():Infinity
        const B=b.end_time?new Date(b.end_time).getTime():Infinity
        return A-B
      })
      break
    case "newest": s.sort((a,b)=>b.id-a.id); break
  }
  return s
}

function applyFilters(){
  state.filteredListings=sortListings(state.listings.filter(matchesFilters))
}

async function fetchListings(){
  const r=await fetch(`${API_BASE}/listings`)
  const j=await r.json()
  return j.items||[]
}

async function loadWatchlist(){
  const r=await fetch(`${API_BASE}/watchlist`)
  const j=await r.json()
  state.watchlist=j.items||[]
}

async function loadAlerts(){
  const r=await fetch(`${API_BASE}/alerts`)
  const j=await r.json()
  state.alerts=j.items||[]
}

function isWatched(id){
  return state.watchlist.some(x=>String(x.id)===String(id))
}

async function toggleWatch(item){
  const exists=isWatched(item.id)

  if(exists){
    await fetch(`${API_BASE}/watchlist/${item.id}`,{method:"DELETE"})
    state.watchlist=state.watchlist.filter(x=>String(x.id)!==String(item.id))
    return false
  }

  await fetch(`${API_BASE}/watchlist`,{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({listing_id:item.id})
  })

  state.watchlist=[item,...state.watchlist]
  return true
}

async function createAlert(item){
  await fetch(`${API_BASE}/alerts`,{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      listing_id:item.id,
      keyword:item.make||item.model||item.title,
      source_name:item.source_name,
      min_score:item.score||0,
      bid_type:isZeroBid(item)?"zero":"all"
    })
  })

  await loadAlerts()
}

function showToast(msg){
  let t=document.getElementById("toast")
  if(!t){
    t=document.createElement("div")
    t.id="toast"
    t.style.position="fixed"
    t.style.bottom="120px"
    t.style.left="50%"
    t.style.transform="translateX(-50%)"
    t.style.padding="12px 18px"
    t.style.background="#111"
    t.style.borderRadius="999px"
    t.style.color="#fff"
    t.style.zIndex="9999"
    document.body.appendChild(t)
  }
  t.textContent=msg
  setTimeout(()=>t.remove(),1800)
}

function renderCard(item){
  const watched=isWatched(item.id)

  return `
  <article class="listing-card">
    <div class="listing-media">
      <img src="${safe(item.image_url||"https://images.unsplash.com/photo-1492144534655-ae79c964c9d7")}" />
      <div class="listing-badges">
        <span class="badge">${safe(item.source_name)}</span>
        ${isZeroBid(item)?'<span class="badge success">Zero Bid</span>':""}
        ${isEndingSoon(item)?'<span class="badge urgent">Ending Soon</span>':""}
        <span class="badge score">Score ${safe(item.score)}</span>
      </div>
    </div>

    <div class="listing-body">
      <div class="listing-head">
        <div>
          <h3>${safe(item.title)}</h3>
          <p>${safe(item.location)}</p>
        </div>
        <div class="listing-price">
          <span>Current Bid</span>
          <strong>${money(item.bid)}</strong>
        </div>
      </div>

      <div class="listing-grid">
        <div class="data-pill"><span>Year</span><strong>${safe(item.year)}</strong></div>
        <div class="data-pill"><span>Make / Model</span><strong>${safe(item.make)} ${safe(item.model)}</strong></div>
        <div class="data-pill"><span>VIN</span><strong>${safe(item.vin)}</strong></div>
        <div class="data-pill"><span>Damage</span><strong>${safe(item.damage)}</strong></div>
      </div>

      <div class="card-actions listing-actions-3">
        <a class="btn btn-primary" href="${safe(item.url||"#")}" target="_blank">Open Auction</a>
        <button class="btn btn-secondary js-watch" data-id="${item.id}">${watched?"Watching":"Watch"}</button>
        <button class="btn btn-secondary js-alert" data-id="${item.id}">Alert</button>
      </div>
    </div>
  </article>
  `
}

function attachEvents(items){
  document.querySelectorAll(".js-watch").forEach(b=>{
    b.onclick=async()=>{
      const item=items.find(x=>String(x.id)===b.dataset.id)
      const watching=await toggleWatch(item)
      b.textContent=watching?"Watching":"Watch"
      showToast(watching?"Added to watchlist":"Removed from watchlist")
    }
  })

  document.querySelectorAll(".js-alert").forEach(b=>{
    b.onclick=async()=>{
      const item=items.find(x=>String(x.id)===b.dataset.id)
      await createAlert(item)
      showToast("Alert saved")
    }
  })
}

function renderHunter(){
  const el=document.getElementById("hunter-results")
  if(!el) return

  el.innerHTML=state.filteredListings.map(renderCard).join("")
  attachEvents(state.filteredListings)

  const c=document.getElementById("hunter-count")
  if(c) c.textContent=state.filteredListings.length
}

function renderWatchlist(){
  const el=document.getElementById("watch-list")
  if(!el) return

  el.innerHTML=state.watchlist.map(renderCard).join("")
  attachEvents(state.watchlist)

  const c=document.getElementById("watch-count")
  if(c) c.textContent=state.watchlist.length
}

function renderAlerts(){
  const el=document.getElementById("alerts-list")
  if(!el) return

  el.innerHTML=state.alerts.map(a=>`
    <article class="glass-card alert-item">
      <div class="alert-row">
        <div>
          <h3>${safe(a.keyword)}</h3>
          <p>Source: ${safe(a.source_name)}</p>
          <p>Score: ${safe(a.min_score)}</p>
        </div>
        <span class="badge success">Live</span>
      </div>
    </article>
  `).join("")

  const c=document.getElementById("alerts-count")
  if(c) c.textContent=state.alerts.length
}

async function init(){
  state.listings=await fetchListings()
  await loadWatchlist()
  await loadAlerts()

  applyFilters()

  const page=document.body.dataset.page

  if(page==="hunter") renderHunter()
  if(page==="watchlist") renderWatchlist()
  if(page==="alerts") renderAlerts()
}

document.addEventListener("DOMContentLoaded",init)
