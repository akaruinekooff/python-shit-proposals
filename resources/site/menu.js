// fetch PSP list json and populate nav dynamically
fetch('psp_list.json')
  .then(res => res.json())
  .then(pspList => {
    const nav = document.querySelector("nav ul");
    const searchInput = document.createElement('input');
    searchInput.placeholder = "Search PSP...";
    searchInput.style.marginBottom = "12px";
    nav.parentNode.insertBefore(searchInput, nav);

    function render(filter = "") {
      nav.innerHTML = "";
      const filtered = pspList.filter(psp =>
        psp.title.toLowerCase().includes(filter.toLowerCase())
      );
      filtered.forEach(psp => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = psp.file;
        a.textContent = psp.title;
        li.appendChild(a);
        nav.appendChild(li);
      });

      // highlight current link
      nav.querySelectorAll('a').forEach(a=>{
        if(a.getAttribute('href')===location.pathname.split("/").pop()) a.classList.add('active');
      });
    }

    searchInput.addEventListener('input', e => render(e.target.value));
    render(); // initial render
  });
