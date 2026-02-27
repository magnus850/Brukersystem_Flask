<script>
  //@ts-nocheck
  import { goto } from "$app/navigation";
  export let data;
  let brukere = "";
  let brukernavn = data.brukernavn;
  let id = data.id;
  let melding = "";
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
    const svar = confirm(`Er du sikker på at du vil slette din egen bruker?`);
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

  async function endre_passord(id, nytt_passord) {
    const respons = await fetch("http://127.0.0.1:5000/endrepassord", {
      method: "POST",
      body: JSON.stringify({ id, nytt_passord }),
      headers: { "Content-Type": "application/json" },
    });
    const data = await respons.json();
    melding = data.passordendret;
    if (melding == true) {
      string = "Passord endret";
    } else if (melding == false) {
      string = "Endre til et annet passord enn ditt gamle";
      passord = "";
      return;
    }
  }
  function sjekk_lengde() {
    string = "";
    if (passord_lengde > max_pa_lengde || passord_lengde < min_pa_lengde) {
      string = `Hold passordlengde innen 8-24 tegn`;
      return;
    }
    if (!string) {
      endre_passord(id, passord);
    }
  }
  const max_pa_lengde = 24;
  const min_pa_lengde = 8;
  let string = "";
  let passord = "";
  let passord_text = "";
  $: passord_lengde = passord_text.length;
  $: passord_text = passord;

  let vis_input = false;

  function logg_ut() {
    goto(`/`);
  }

  async function gi_bruker_admin(bruker) {
    const svar = confirm(
      `Er du sikker på at du vil gi bruker ${bruker[1]} admintilgang?`,
    );
    if (svar) {
      let id = bruker[0];
      const respons = await fetch("http://127.0.0.1:5000/tillatelseendring", {
        method: "POST",
        body: JSON.stringify({ id }),
        headers: { "Content-Type": "application/json" },
      });
      hent_brukere();
    } else {
      return;
    }
  }
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
        <td>{bruker[0]}</td>
        <td>{bruker[1]}</td>
        <td>{bruker[2]}</td>
        <td class="table-actions">
          {#if bruker[2] === "bruker"}
            <button on:click={() => slett_bruker(bruker)}>Slett</button>
            <button on:click={() => gi_bruker_admin(bruker)}>Gi admin</button>
          {/if}
        </td>
      </tr>
    </tbody>
  {/each}
</table>
<br />
<button on:click={() => slett_egen_bruker(id)}>Slett egen bruker</button>
<button on:click={() => (vis_input = !vis_input)}>Endre passord</button>
<button on:click={() => logg_ut()}>Logg ut</button>
{#if vis_input}
  <label for="passord">Nytt passord:</label>
  <input type="password" id="passord" bind:value={passord} />
  <button on:click={() => sjekk_lengde()}>Bekreft</button>
{/if}
{#if string}
  <p class="message">{@html string}</p>
{/if}
