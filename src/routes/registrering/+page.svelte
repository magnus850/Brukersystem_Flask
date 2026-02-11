<script>
  const max_br_lengde = 15;
  const min_br_lengde = 5;
  const max_pa_lengde = 24;
  const min_pa_lengde = 8;
  let brukernavn = "";
  let passord = "";

  async function registrering() {
    const respons = await fetch("http://127.0.0.1:5000/regdata", {
      method: "POST",
      body: JSON.stringify({ brukernavn, passord }),
      headers: { "Content-Type": "application/json" },
    });
    const text = await respons.text();
    console.log("Respons: ", { text });
  }
  let brukernavn_text = "";
  $: brukernavn_lengde = brukernavn_text.length;
  $: brukernavn_text = brukernavn;

  let passord_text;
  $: passord_lengde = passord_text.length;
  $: passord_text = passord;

  function sjekk_lengde() {
    if (
      brukernavn_lengde > max_br_lengde ||
      brukernavn_lengde < min_br_lengde
    ) {
      console.log("Hold brukernavnlengde innen 5-15 tegn");
    }
    if (passord_lengde > max_pa_lengde || passord_lengde < min_pa_lengde) {
      console.log("Hold passordlengde innen 8-24 tegn");
    } else registrering();
  }
</script>

<h1>Registrer deg</h1>
<label for="brukernavn">Brukernavn:</label>
<input type="text" id="brukernavn" bind:value={brukernavn} />
<br />
<label for="passord">Passord:</label>
<input type="text" id="passord" bind:value={passord} />

<button on:click={sjekk_lengde}>Registrer</button>
<br />
<a href="/">Hjem</a>
<br />
<a href="/innlogging">Logg inn</a>
