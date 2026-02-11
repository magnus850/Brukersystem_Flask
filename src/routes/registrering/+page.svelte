<script>
  const max_br_lengde = 15;
  const min_br_lengde = 5;
  const max_pa_lengde = 24;
  const min_pa_lengde = 8;
  let brukernavn = "";
  let passord = "";
  async function logg_inn() {
    const respons = await fetch("http://127.0.0.1:5000/inputdata", {
      method: "POST",
      body: JSON.stringify({ brukernavn, passord }),
      headers: { "Content-Type": "application/json" },
    });
    const text = await respons.text();
    console.log("Respons: ", { text });
  }
  let text = "";
  $: lengde = text.length;
  $: text = brukernavn;
  function print_input() {
    console.log(brukernavn);
    console.log(passord);
    console.log(lengde);
  }
</script>

<h1>Registrer deg</h1>
<label for="brukernavn">Brukernavn:</label>
<input
  type="text"
  id="brukernavn"
  bind:value={brukernavn}
  on:blur={print_input}
/>
<br />
<label for="passord">Passord:</label>
<input type="text" id="passord" bind:value={passord} on:blur={print_input} />

<button on:click={logg_inn}>Registrer</button>
<br />
<a href="/">Hjem</a>
<br />
<a href="/innlogging">Logg inn</a>
