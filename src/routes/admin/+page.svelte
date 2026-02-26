<script>
  //@ts-nocheck
  import { goto } from "$app/navigation";
  export let data;
  let brukere = "";
  let brukernavn = data.brukernavn;
  let id = data.id;
  console.log(id);
  async function hent_brukere() {
    const respons = await fetch("http://127.0.0.1:5000/brukerdb", {
      method: "POST",
      body: JSON.stringify({ brukernavn }),
      headers: { "Content-Type": "application/json" },
    });
    const data = await respons.json();
    brukere = data.brukere;
    return brukere;
  }

  async function slett_bruker(bruker) {
    const svar = confirm(
      `Er du sikker på at du vil slette bruker ${bruker[1]}?`,
    );
    if (svar) {
      let id = bruker[0];
      const respons = await fetch("http://127.0.0.1:5000/slettbruker", {
        method: "POST",
        body: JSON.stringify({ id }),
        headers: { "Content-Type": "application/json" },
      });
      hent_brukere();
    } else {
      return;
    }
  }
  async function slett_egen_bruker(id) {
    const svar = confirm(
      `Er du sikker på at du vil slette bruker din egen bruker?`,
    );
    if (svar) {
      const respons = await fetch("http://127.0.0.1:5000/slettbruker", {
        method: "POST",
        body: JSON.stringify({ id }),
        headers: { "Content-Type": "application/json" },
      });
      goto(`/`);
    } else {
      return;
    }
  }
  hent_brukere();
</script>

<h1>Hei {data.tillatelse} {brukernavn}</h1>
<h2>Brukerdatabase</h2>
<table>
  <thead>
    <tr>
      <th>ID</th>
      <th>Brukernavn</th>
      <th>Tilgang</th>
      <th>Rediger</th>
    </tr>
  </thead>
  {#each brukere as bruker}
    <tbody>
      <tr>
        <th>{bruker[0]}</th>
        <th>{bruker[1]}</th>
        <th>{bruker[2]}</th>
        <th><button on:click={() => slett_bruker(bruker)}>Slett</button></th>
      </tr>
    </tbody>
  {/each}
</table>
<br />
<button on:click={() => slett_egen_bruker(id)}>Slett egen bruker</button>
