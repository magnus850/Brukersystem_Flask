<script>
  import { goto } from "$app/navigation";

  const max_br_lengde = 15;
  const min_br_lengde = 5;
  const max_pa_lengde = 24;
  const min_pa_lengde = 8;
  let brukernavn = "";
  let passord = "";
  let tillatelse = "";
  let melding = "";
  let id = "";

  async function registrering() {
    const respons = await fetch("http://127.0.0.1:5000/regdata", {
      method: "POST",
      body: JSON.stringify({ brukernavn, passord }),
      headers: { "Content-Type": "application/json" },
    });
    const data = await respons.json();
    melding = data.melding;
    if (melding == "Brukernavn er tatt, velg et annet") {
      string1 = melding;
      return;
    }
    tillatelse = data.tillatelse;
    id = data.id;
    if (tillatelse == "admin") {
      goto(
        `/admin?brukernavn=${encodeURIComponent(brukernavn)}&tillatelse=${encodeURIComponent(tillatelse)}&id=${encodeURIComponent(id)}`,
      );
    } else if (tillatelse == "bruker") {
      goto(
        `/bruker?brukernavn=${encodeURIComponent(brukernavn)}&tillatelse=${encodeURIComponent(tillatelse)}&id=${encodeURIComponent(id)}`,
      );
    }
  }

  let string1 = "";
  let string2 = "";
  function sjekk_lengde() {
    string1 = "";
    string2 = "";
    if (
      brukernavn_lengde > max_br_lengde ||
      brukernavn_lengde < min_br_lengde
    ) {
      string1 = `Hold brukernavnlengde innen 5-15 tegn`;
    }
    if (passord_lengde > max_pa_lengde || passord_lengde < min_pa_lengde) {
      string2 = `Hold passordlengde innen 8-24 tegn`;
      return;
    }
    if (!string1 && !string2) {
      registrering();
    }
  }
  let brukernavn_text = "";
  $: brukernavn_lengde = brukernavn_text.length;
  $: brukernavn_text = brukernavn;

  let passord_text = "";
  $: passord_lengde = passord_text.length;
  $: passord_text = passord;
</script>

<h1>Registrer deg</h1>
<label for="brukernavn">Brukernavn:</label>
<input type="text" id="brukernavn" bind:value={brukernavn} />
<br />
<label for="passord">Passord:</label>
<input type="password" id="passord" bind:value={passord} />

<button on:click={sjekk_lengde}>Registrer</button>
<br />
{#if string1}
  <p class="message">{@html string1}</p>
{/if}
{#if string2}
  <p class="message">{@html string2}</p>
{/if}
