/* ============================================================
   RANDOM GALLERY ENGINE — shared across all 8 pages
   Implements: local random sampling, per-section slideshow,
   49-image popup, and explicit Hero-main exclusion rule.
   No backticks, var + concat only, safe pattern matching project rules.
   ============================================================ */
(function(){
  'use strict';

  function pickRandom(arr, n){
    var pool = arr.slice();
    var result = [];
    var count = Math.min(n, pool.length);
    for(var i=0;i<count;i++){
      var idx = Math.floor(Math.random()*pool.length);
      result.push(pool[idx]);
      pool.splice(idx,1);
    }
    // If fewer real images than needed, cycle to fill the slideshow visually
    while(result.length < n && arr.length){
      result.push(arr[result.length % arr.length]);
    }
    return result;
  }

  // ---- SLIDESHOW BUILDER ----
  // hostEl: container element; imagePool: array of urls; isMainHero: disables all interaction
  function buildSlideshow(hostEl, imagePool, isMainHero){
    if(!hostEl || !imagePool || !imagePool.length) return null;
    var chosen = pickRandom(imagePool, 7);
    var idx = 0;
    var imgEl = document.createElement('div');
    imgEl.className = 'rge-slide-img';
    imgEl.style.backgroundImage = "url('" + chosen[0] + "')";
    imgEl.style.backgroundSize = 'cover';
    imgEl.style.backgroundPosition = 'center';
    imgEl.style.width = '100%';
    imgEl.style.height = '100%';
    imgEl.style.transition = 'opacity .6s ease';
    hostEl.appendChild(imgEl);

    var timer = setInterval(function(){
      idx = (idx + 1) % chosen.length;
      imgEl.style.opacity = '0';
      setTimeout(function(){
        imgEl.style.backgroundImage = "url('" + chosen[idx] + "')";
        imgEl.style.opacity = '1';
      }, 350);
    }, 4200);

    if(isMainHero){
      // RULE: main artist Hero never responds to click/hover/popup — autoplay only
      return { chosen: chosen, timer: timer, interactive: false };
    }
    return { chosen: chosen, timer: timer, interactive: true };
  }

  // ---- POPUP BUILDER (49 images for a single section) ----
  function openSectionPopup(sectionImages, titleEn, titleAr){
    var overlay = document.createElement('div');
    overlay.className = 'rge-popup-overlay';
    overlay.style.cssText = 'position:fixed;inset:0;z-index:9000;background:rgba(5,5,4,.92);display:flex;flex-direction:column;align-items:center;padding:2rem 1rem;overflow-y:auto;backdrop-filter:blur(6px)';

    var closeBtn = document.createElement('button');
    closeBtn.textContent = '\u2715';
    closeBtn.style.cssText = 'position:fixed;top:1.5rem;left:1.5rem;width:42px;height:42px;border-radius:50%;background:rgba(255,255,255,.06);border:1px solid rgba(200,169,110,.3);color:#F0EBE1;font-size:1.1rem;cursor:pointer;z-index:9001';
    closeBtn.onclick = function(){ overlay.remove(); };

    var title = document.createElement('div');
    title.style.cssText = 'font-family:Cormorant Garamond,serif;font-size:1.6rem;font-style:italic;color:#C8A96E;margin-bottom:1.8rem;text-align:center';
    title.textContent = titleEn;

    var grid = document.createElement('div');
    grid.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:.8rem;max-width:1300px;width:100%';

    for(var i=0;i<sectionImages.length;i++){
      var cell = document.createElement('div');
      cell.style.cssText = 'aspect-ratio:4/3;border-radius:8px;overflow:hidden;background:#0a0a09';
      var img = document.createElement('img');
      img.src = sectionImages[i];
      img.loading = 'lazy';
      img.style.cssText = 'width:100%;height:100%;object-fit:cover;filter:grayscale(.3) brightness(.85);transition:filter .4s ease';
      img.onmouseenter = function(){ this.style.filter = 'grayscale(0) brightness(1)'; };
      img.onmouseleave = function(){ this.style.filter = 'grayscale(.3) brightness(.85)'; };
      cell.appendChild(img);
      grid.appendChild(cell);
    }

    overlay.appendChild(closeBtn);
    overlay.appendChild(title);
    overlay.appendChild(grid);
    document.body.appendChild(overlay);

    overlay.addEventListener('click', function(e){
      if(e.target === overlay) overlay.remove();
    });
  }

  // Expose globally
  window.RGE = {
    pickRandom: pickRandom,
    buildSlideshow: buildSlideshow,
    openSectionPopup: openSectionPopup
  };
})();
