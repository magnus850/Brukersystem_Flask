<script>
  import { goto } from "$app/navigation";

  let brukernavn = "";
  let passord = "";
  let tillatelse = "";
  let id = "";
  let suksess = false;
  let string = "";

  async function logg_inn() {
    const respons = await fetch("http://127.0.0.1:5000/inputdata", {
      method: "POST",
      body: JSON.stringify({ brukernavn, passord }),
      headers: { "Content-Type": "application/json" },
    });
    const data = await respons.json();
    tillatelse = data.tillatelse;
    suksess = data.suksess;
    id = data.id;
    if (suksess && tillatelse == "admin") {
      goto(
        `/admin?brukernavn=${encodeURIComponent(brukernavn)}&tillatelse=${encodeURIComponent(tillatelse)}&id=${encodeURIComponent(id)}`,
      );
    } else if (suksess && tillatelse == "bruker") {
      goto(
        `/bruker?brukernavn=${encodeURIComponent(brukernavn)}&tillatelse=${encodeURIComponent(tillatelse)}&id=${encodeURIComponent(id)}`,
      );
    } else if (suksess == false) {
      string = "Feil brukernavn og/eller passord";
    }
  }
</script>

<h1>Logg inn</h1>
<label for="brukernavn">Brukernavn:</label>
<input type="text" id="brukernavn" bind:value={brukernavn} />
<br />
<label for="passord">Passord:</label>
<input type="password" id="passord" bind:value={passord} />

<button on:click={logg_inn}>Logg inn</button>
{#if string}
  <p class="message">{@html string}</p>
{/if}
