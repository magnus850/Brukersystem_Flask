<script>
  import { goto } from "$app/navigation";

  let brukernavn = "";
  let passord = "";
  let tillatelse = "";
  let suksess = false;

  async function logg_inn() {
    const respons = await fetch("http://127.0.0.1:5000/inputdata", {
      method: "POST",
      body: JSON.stringify({ brukernavn, passord }),
      headers: { "Content-Type": "application/json" },
    });
    const data = await respons.json();
    tillatelse = data.tillatelse;
    suksess = data.suksess;
    if (suksess) {
      goto("/admin");
    }
  }
</script>

<h1>Logg inn</h1>
<label for="brukernavn">Brukernavn:</label>
<input type="text" id="brukernavn" bind:value={brukernavn} />
<br />
<label for="passord">Passord:</label>
<input type="text" id="passord" bind:value={passord} />

<button on:click={logg_inn}>Logg inn</button>
<br />
<a href="/">Hjem</a>
<br />
<a href="/registrering">Registrer deg</a>
